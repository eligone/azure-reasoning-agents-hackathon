import concurrent.futures
from input_validation import gather_full_learner_profile
from agents.profiler import run_learner_profiler
from agents.planner import run_syllabus_planner
from agents.curator import run_learning_curator
from agents.executor import evaluate_study_plan, run_assessment_executor
from agents.reviewer import run_remediation_reviewer
from quiz_engine import run_interactive_quiz
from time_distributor import distribute_study_hours

def main():
    print("==================================================")
    print("   Welcome to Your Personalized Multi-Agent Coach")
    print("==================================================")
    
    # Gathers baseline tracking metrics and raw background strings
    user_profile, raw_background = gather_full_learner_profile()
    
    # Trigger Agent 4: The Learner Profiling Agent
    print("\n[Invoking Agent 4] Analyzing professional background text parameters...")
    calculated_ratings = run_learner_profiler(user_profile.exam_target, raw_background)
    
    # Save the calculated metrics directly into our secure data contract container
    user_profile.domain_ratings = calculated_ratings
    
    print("\n==============================================")
    print("📋      AGENT 4: INITIAL LEARNER PROFILE       ")
    print("==============================================")
    for domain, rating in user_profile.domain_ratings.items():
        print(f"  • {domain}: {rating}/5 Level")
    print("==============================================")
    
    # Compute algorithmic hour distributions using Largest Remainder Method
    print("\n[Running Time Distributor] Running Largest Remainder Algorithm calculations...")
    calculated_hours_map = distribute_study_hours(
        user_profile.domain_ratings,
        user_profile.target_weeks,
        user_profile.days_per_week,
        user_profile.hours_per_day
    )
    
    print("\n==============================================")
    print("📊    ALGORITHMIC TARGET HOURS ALLOCATION     ")
    print("==============================================")
    for domain, hours in calculated_hours_map.items():
        print(f"  • {domain}: {hours} Total Target Hours")
    print("==============================================")
    
    print(f"\nInitializing interactive pipeline for {user_profile.exam_target}...")
    
    # Inject exact mathematical breakdown constraints into the prompt context stream
    hours_breakdown_string = ", ".join([f"Spend exactly {h} hours on {d}" for d, h in calculated_hours_map.items()])
    feedback = (
        f"CRITICAL REQUIREMENT: The final schedule must fit completely within a maximum duration of EXACTLY {user_profile.target_weeks} calendar weeks. "
        f"You must strictly respect this exact algorithmic hour allocation breakdown: {hours_breakdown_string}."
    )
    
    attempts = 0
    max_revisions = 3
    final_roadmap = ""
    curated_resources = ""
    is_cram_needed = False
    
    try:
        print("\n[Invoking Concurrent Workers] Launching Planner and Curator agents in parallel threads...")
        
        # Execute independent cloud requests concurrently to minimize system latency
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_plan = executor.submit(
                run_syllabus_planner, 
                user_profile.exam_target, 
                user_profile.days_per_week, 
                user_profile.hours_per_day, 
                feedback
            )
            future_resources = executor.submit(
                run_learning_curator, 
                user_profile.exam_target, 
                user_profile.domain_ratings
            )
            
            # Reconverge parallel workers and harvest strings cleanly
            final_roadmap = future_plan.result()
            curated_resources = future_resources.result()

        # Execute our multi-agent quality auditing check loop
        while attempts < max_revisions:
            attempts += 1
            audit_result = evaluate_study_plan(
                final_roadmap, 
                user_profile.days_per_week, 
                user_profile.hours_per_day
            )
            
            if audit_result.startswith("REJECT") or f"{user_profile.target_weeks} weeks" not in final_roadmap.lower():
                feedback = f"{audit_result} \nReminder: MUST FIT IN {user_profile.target_weeks} WEEKS."
                is_cram_needed = True
                
                # Standalone sequential re-evaluation if the auditor triggers a reject event
                final_roadmap = run_syllabus_planner(
                    user_profile.exam_target, 
                    user_profile.days_per_week, 
                    user_profile.hours_per_day, 
                    feedback
                )
            else:
                is_cram_needed = False
                feedback = None
                break
        
        if is_cram_needed:
            print("\n======================================================================")
            print("⚠️  MULTI-AGENT SYSTEM NOTICE: STUDY TIMELINE DISCLAIMER WARNING")
            print("======================================================================")
            print(f"Our auditing agent notes that trying to master all domains for '{user_profile.exam_target}'")
            print(f"within {user_profile.target_weeks} weeks under your current hourly availability profile is highly discouraged.")
            print("The schedule will feel severely crammed, and you risk hitting immediate burnout.")
            print("----------------------------------------------------------------------")
            
            bypass_choice = input("Do you wish to override this warning and construct the rush cram plan anyway? (yes/no): ").strip().lower()
            if bypass_choice not in ["yes", "y"]:
                print("\nSession aborted cleanly.")
                return
            print("\nBypass confirmed. Compiling your high-intensity cram roadmap...")

        print("\n==============================================")
        print("===        FINAL CERTIFICATION PLAN        ===")
        print("==============================================")
        print(final_roadmap)
        
        print("\n==============================================")
        print("📚   CURATED MICROSOFT LEARN RECOMMENDATIONS   ")
        print("==============================================")
        print(curated_resources)
        print("==============================================")
        
        # Adaptive Multi-Turn Testing Block
        current_topic = "Core Fundamentals and Architecture Models"
        
        while True:
            print(f"\n[Invoking Agent 2] Constructing 5 specialized testing questions for: '{current_topic}'...")
            raw_quiz_text = run_assessment_executor(
                final_roadmap, 
                specific_topic=current_topic if current_topic != "Core Fundamentals and Architecture Models" else None
            )
            
            score, total_q = run_interactive_quiz(raw_quiz_text)
            
            passing_threshold = 0.70
            success_rate = score / total_q if total_q > 0 else 0
            
            if success_rate >= passing_threshold:
                print("\n🏆 EXCELLENT WORK! You passed the benchmark capability threshold for this domain.")
                print("The system recommends advancing straight onto the next milestone section.")
                
                choice = input("\nDo you wish to advance to the next topic or quit? (next/quit): ").strip().lower()
                if choice in ["next", "n"]:
                    current_topic = "Advanced Scalability, Networking, and Security Implementations"
                    print(f"\nRouting track advanced. Loading next domain module...")
                    continue
                else:
                    print("\nSession closed cleanly. Keep up the amazing study pace!")
                    break
            else:
                print("\n⚠️  BENCHMARK NOT MET: Score fell below the target 70% proficiency barrier.")
                print("[Invoking Agent 3] Routing session to Personalized Remediation Reviewer...")
                
                critique = run_remediation_reviewer(current_topic, score, total_q)
                print("\n======================================================================")
                print("💡  AGENT 3 COACHING INSIGHTS & STRATEGY REPORT")
                print("======================================================================")
                print(critique)
                print("======================================================================")
                
                retry_choice = input("\nWould you like to retry this domain, skip it, or quit? (retry/skip/quit): ").strip().lower()
                if retry_choice in ["quit", "q"]:
                    print("\nSession closed cleanly. See you next time!")
                    break
                elif retry_choice in ["skip", "s"]:
                    print("\nNo worries! Advancing you onto the next timeline milestone block anyway.")
                    current_topic = "Advanced Scalability, Networking, and Security Implementations"
                    continue
                else:
                    print(f"\nResetting module tracking. Invoking a new custom variant query loop for '{current_topic}'...")
                    continue
                    
    except Exception as error_log:
        print(f"\nPipeline Execution Failed: {error_log}")

if __name__ == "__main__":
    main()