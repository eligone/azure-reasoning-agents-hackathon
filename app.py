from agents.planner import run_syllabus_planner
from agents.executor import evaluate_study_plan, run_assessment_executor

def main():
    print("==================================================")
    print("   Welcome to Your Personalized Multi-Agent Coach")
    print("==================================================")
    
    # Collect dynamic user preferences directly from the terminal console
    target_exam = input("What certification or exam are you practicing for? ")
    days_per_week = input("How many days a week can you dedicate to studying? ")
    hours_per_day = input("How many hours per day can you study on those days? ")
    
    print(f"\nInitializing interactive pipeline for {target_exam}...")
    
    feedback = None
    attempts = 0
    max_revisions = 3
    final_roadmap = ""
    
    try:
        # Agent Collaboration Loop
        while attempts < max_revisions:
            attempts += 1
            print(f"[Iteration {attempts}] Passing draft to Agent 2 for quality control audit...")
            final_roadmap = run_syllabus_planner(target_exam, days_per_week, hours_per_day, feedback)
            
            print("[Iteration {attempts}] Passing draft to Agent 2 for quality control audit...")
            audit_result = evaluate_study_plan(final_roadmap, days_per_week, hours_per_day)
            
            if audit_result.startswith("REJECT"):
                print("\n❌ Agent 2 REJECTED the plan! Sending revision notes back to Agent 1...")
                feedback = audit_result
            else:
                print("\n✅ Agent 2 APPROVED the study timeline layout!")
                break
        
        # Print the final consensus blueprint layout
        print("\n==============================================")
        print("===        FINAL APPROVED STUDY PLAN       ===")
        print("==============================================")
        print(final_roadmap)
        
        # Trigger the final evaluation step
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