def run_interactive_quiz(raw_quiz_text):
    """
    Parses the structured delimiter blocks from Agent 2 and executes an interactive 
    testing simulation inside the console terminal workspace.
    """
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