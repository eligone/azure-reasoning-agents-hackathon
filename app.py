from input_validation import get_validated_exam, get_validated_number, get_study_duration_weeks
from agents.planner import run_syllabus_planner
from agents.executor import evaluate_study_plan, run_assessment_executor

def run_interactive_quiz(raw_quiz_text):
    segments = raw_quiz_text.split("[Q]")
    questions_compiled = []
    
    for segment in segments:
        if not segment.strip():
            continue
        try:
            q_part, rest = segment.split("[ANS]")
            ans_part, exp_part = rest.split("[EXP]")
            questions_compiled.append({
                "question": q_part.strip(),
                "correct_answer": ans_part.strip().upper(),
                "explanation": exp_part.strip()
            })
        except ValueError:
            continue

    if not questions_compiled:
        print("\n⚠️  Quiz formatting parsing error. Fallback raw print stream:")
        print(raw_quiz_text)
        return

    print("\n=================================================")
    print("===      STARTING INTERACTIVE PRACTICE QUIZ   ===")
    print("=================================================")
    
    score = 0
    for idx, item in enumerate(questions_compiled, 1):
        print(f"\n--- QUESTION {idx} ---")
        print(item["question"])
        
        while True:
            user_guess = input("\nYour Answer (A, B, C, or D): ").strip().upper()
            if user_guess in ["A", "B", "C", "D"]:
                break
            print("❌ Invalid entry. Please choose exactly A, B, C, or D.")
            
        if user_guess == item["correct_answer"]:
            print("\n🎉 CORRECT!")
            score += 1
        else:
            print(f"\n❌ INCORRECT. (The correct answer was {item['correct_answer']})")
            
        print(f"Explanation: {item['explanation']}")
        print("-" * 40)
        
    print(f"\n=================================================")
    print(f"🎉 QUIZ COMPLETE! Final Score: {score}/{len(questions_compiled)}")
    print("=================================================")

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
            # Run the generation quietly behind the scenes
            final_roadmap = run_syllabus_planner(target_exam, days_per_week, hours_per_day, feedback)
            audit_result = evaluate_study_plan(final_roadmap, days_per_week, hours_per_day)
            
            if audit_result.startswith("REJECT") or f"{target_weeks} weeks" not in final_roadmap.lower():
                feedback = f"{audit_result} \nReminder: MUST FIT IN {target_weeks} WEEKS."
                is_cram_needed = True
            else:
                is_cram_needed = False
                feedback = None
                break
        
        # Only show the disclaimer prompt block if we couldn't find an ideal timeline fit
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
        run_interactive_quiz(raw_quiz_text)
        
        print("\nInteractive pipeline execution clean. Personal session closed.")
        
    except Exception as error_log:
        print(f"\nPipeline Execution Failed: {error_log}")

if __name__ == "__main__":
    main()