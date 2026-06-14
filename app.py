from input_validation import get_validated_exam, get_validated_number, get_study_duration_weeks
from agents.planner import run_syllabus_planner
from agents.executor import evaluate_study_plan, run_assessment_executor

def main():
    print("==================================================")
    print("   Welcome to Your Personalized Multi-Agent Coach")
    print("==================================================")
    
    target_exam = get_validated_exam()
    days_per_week = get_validated_number("How many days a week can you dedicate to studying? ", 1, 7, "days")
    hours_per_day = get_validated_number("How many hours per day can you study on those days? ", 1, 24, "hours")
    target_weeks = get_study_duration_weeks()
    
    print(f"\nInitializing interactive pipeline for {target_exam} target window: {target_weeks} weeks...")
    
    feedback = f"CRITICAL REQUIREMENT: The final schedule must fit completely within a maximum duration of EXACTLY {target_weeks} calendar weeks. Adjust topic density to ensure it fits."
    attempts = 0
    max_revisions = 3
    final_roadmap = ""
    
    try:
        while attempts < max_revisions:
            attempts += 1
            print(f"\n[Iteration {attempts}] Agent 1 is drafting your customized roadmap...")
            final_roadmap = run_syllabus_planner(target_exam, days_per_week, hours_per_day, feedback)
            
            print(f"[Iteration {attempts}] Passing draft to Agent 2 for quality control audit...")
            audit_result = evaluate_study_plan(final_roadmap, days_per_week, hours_per_day)
            
            # Check if Agent 2 rejected it or if the text generation mentions it exceeded the week count
            if audit_result.startswith("REJECT") or f"{target_weeks} weeks" not in final_roadmap.lower():
                print(f"\n❌ Agent 2 Warning: This material is heavy to compress into just {target_weeks} weeks under your daily hourly constraints.")
                feedback = f"{audit_result} \nReminder: MUST FIT IN {target_weeks} WEEKS."
            else:
                print("\n✅ Agent 2 APPROVED the study timeline layout!")
                feedback = None
                break
        
        # Disclaimer Check Trigger: If we ran out of loop iterations, it means the timeline is too aggressive
        if feedback is not None:
            print("\n======================================================================")
            print("⚠️  MULTI-AGENT SYSTEM NOTICE: STUDY TIMELINE DISCLAIMER WARNING")
            print("======================================================================")
            print(f"Our auditing agent notes that trying to master all domains for '{target_exam}'")
            print(f"within {target_weeks} weeks under your current hourly availability profile is highly discouraged.")
            print("The schedule will feel severely crammed, and you risk hitting immediate burnout.")
            print("----------------------------------------------------------------------")
            
            bypass_choice = input("Do you wish to override this warning and construct the rush cram plan anyway? (yes/no): ").strip().lower()
            if bypass_choice not in ["yes", "y"]:
                print("\nSession aborted cleanly. Try increasing your target week window size or daily hours next run!")
                return
            print("\nBypass confirmed. Compiling your high-intensity cram roadmap...")

        # Print whatever layout consensus version we landed on
        print("\n==============================================")
        print("===        FINAL CERTIFICATION PLAN        ===")
        print("==============================================")
        print(final_roadmap)
        
        print("\n[Invoking Agent 2] Constructing your customized test simulation questions...")
        practice_quiz = run_assessment_executor(final_roadmap)
        
        print("\n=================================================")
        print("===        YOUR CUSTOM PRACTICE QUIZ          ===")
        print("=================================================")
        print(practice_quiz)
        
        print("\nInteractive pipeline execution clean. Personal session closed.")
        
    except Exception as error_log:
        print(f"\nPipeline Execution Failed: {error_log}")

if __name__ == "__main__":
    main()