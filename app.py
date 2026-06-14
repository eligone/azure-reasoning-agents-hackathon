from input_validation import get_validated_exam, get_validated_number, get_study_duration_weeks
from agents.planner import run_syllabus_planner
from agents.executor import evaluate_study_plan, run_assessment_executor
from agents.reviewer import run_remediation_reviewer
from quiz_engine import run_interactive_quiz

def main():
    print("==================================================")
    print("   Welcome to Your Personalized Multi-Agent Coach")
    print("==================================================")
    
    target_exam = get_validated_exam()
    days_per_week = get_validated_number("How many days a week can you dedicate to studying? ", 1, 7, "days")
    hours_per_day = get_validated_number("How many hours per day can you study on those days? ", 1, 24, "hours")
    target_weeks = get_study_duration_weeks()
    
    print(f"\nInitializing interactive pipeline for {target_exam}...")
    
    feedback = f"CRITICAL REQUIREMENT: The final schedule must fit completely within a maximum duration of EXACTLY {target_weeks} calendar weeks."
    attempts = 0
    max_revisions = 3
    final_roadmap = ""
    is_cram_needed = False
    
    try:
        while attempts < max_revisions:
            attempts += 1
            final_roadmap = run_syllabus_planner(target_exam, days_per_week, hours_per_day, feedback)
            audit_result = evaluate_study_plan(final_roadmap, days_per_week, hours_per_day)
            
            if audit_result.startswith("REJECT") or f"{target_weeks} weeks" not in final_roadmap.lower():
                feedback = f"{audit_result} \nReminder: MUST FIT IN {target_weeks} WEEKS."
                is_cram_needed = True
            else:
                is_cram_needed = False
                feedback = None
                break
        
        if is_cram_needed:
            print("\n======================================================================")
            print("⚠️  MULTI-AGENT SYSTEM NOTICE: STUDY TIMELINE DISCLAIMER WARNING")
            print("======================================================================")
            print(f"Our auditing agent notes that trying to master all domains for '{target_exam}'")
            print(f"within {target_weeks} weeks under your current hourly availability profile is highly discouraged.")
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
        
        
# Adaptive Multi-Turn Testing Block
        current_topic = "Core Fundamentals and Architecture Models"
        
        while True:
            print(f"\n[Invoking Agent 2] Constructing 5 specialized testing questions for: '{current_topic}'...")
            raw_quiz_text = run_assessment_executor(final_roadmap, specific_topic=current_topic if current_topic != "Core Fundamentals and Architecture Models" else None)
            
            score, total_q = run_interactive_quiz(raw_quiz_text)
            
            passing_threshold = 0.70
            success_rate = score / total_q if total_q > 0 else 0
            
            if success_rate >= passing_threshold:
                print("\n🏆 EXCELLENT WORK! You passed the benchmark capability threshold for this domain.")
                print("The system recommends advancing straight onto the next milestone section.")
                
                # Added an explicit quit option to the prompt entry line
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
                
                # Added an explicit quit option to the retry check block
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