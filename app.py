from agents.planner import run_syllabus_planner
from agents.executor import run_assessment_executor

def main():
    target_exam = "Azure Developer Associate AZ-204"
    print(f"Initializing Modular Cloud Multi-Agent Pipeline for {target_exam}...")
    
    try:
        print("\n[Invoking Agent 1] Executing Syllabus Planner module...")
        roadmap = run_syllabus_planner(target_exam)
        
        print("\n==============================================")
        print("=== AGENT 1 (SYLLABUS PLANNER) RESPONDED ===")
        print("==============================================")
        print(roadmap)
        
        print("\n[Invoking Agent 2] Handing context over to Assessment Executor module...")
        practice_quiz = run_assessment_executor(roadmap)
        
        print("\n=================================================")
        print("=== AGENT 2 (ASSESSMENT EXECUTOR) RESPONDED ===")
        print("=================================================")
        print(practice_quiz)
        
        print("\nModular system run clean. Pipeline shutdown pristine.")
        
    except Exception as error_log:
        print(f"\nPipeline Execution Failed: {error_log}")

if __name__ == "__main__":
    main()