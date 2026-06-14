from input_validation import get_validated_exam, get_validated_number, get_study_duration_weeks
from agents.planner import run_syllabus_planner
from agents.executor import evaluate_study_plan, run_assessment_executor
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
        
        print("\n[Invoking Agent 2] Constructing your customized test simulation questions...")
        raw_quiz_text = run_assessment_executor(final_roadmap)
        
        # Call our clean, imported utility engine module
        run_interactive_quiz(raw_quiz_text)
        
        print("\nInteractive pipeline execution clean. Personal session closed.")
        
    except Exception as error_log:
        print(f"\nPipeline Execution Failed: {error_log}")

if __name__ == "__main__":
    main()