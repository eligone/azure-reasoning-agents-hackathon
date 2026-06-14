import streamlit as st
import json
import re

def parse_question_and_options(raw_question_text):
    """
    Helper Utility: Uses robust regular expressions to dynamically extract the 
    core question text and separate its multiple choice options (A, B, C, D).
    """
    text = raw_question_text
    
    # Pattern looks for letters A, B, C, D followed by a parenthesis, period, or colon
    pattern = r'\b([A-D])(?:[\s\)\.\:]+)'
    
    # Find all option markers and their string indices
    matches = list(re.finditer(pattern, text))
    
    if len(matches) >= 2:
        # The core question body is everything before the very first option match
        question_body = text[:matches[0].start()].strip()
        parsed_options = {}
        
        for i in range(len(matches)):
            start_idx = matches[i].end()
            # If it's the last option, slice to the end of the string, otherwise slice to the next match
            end_idx = matches[i+1].start() if i + 1 < len(matches) else len(text)
            
            option_letter = matches[i].group(1)
            option_text = text[start_idx:end_idx].strip()
            
            # Clean up trailing commas, brackets, or double quotes the LLM might leave behind
            option_text = re.sub(r'[,"\']+$', '', option_text).strip()
            parsed_options[option_letter] = option_text
            
        # Reconstruct clean display labels for Streamlit's radio buttons
        display_choices = []
        for letter in ["A", "B", "C", "D"]:
            if letter in parsed_options:
                display_choices.append(f"{letter}: {parsed_options[letter]}")
            else:
                display_choices.append(f"{letter}: Option text unavailable")
                
        return question_body, display_choices
        
    # Standard safe fallback if the string does not follow a multiple-choice structure
    return text, ["A", "B", "C", "D"]

def render_interactive_quiz(raw_quiz_json_string):
    """
    Parses raw JSON strings from Agent 2 and tracks a multi-turn active assessment session
    using streamlined, single-click button state progression transitions.
    """
    if not raw_quiz_json_string:
        st.info("No assessment metrics generated yet. Click the button above to begin.")
        return

    try:
        cleaned_json = raw_quiz_json_string.replace('\\n', '\n').strip()
        questions_list = json.loads(cleaned_json, strict=False)
        total_questions = len(questions_list)
        
        if total_questions == 0:
            st.error("Generated quiz data array is empty.")
            return

        if "quiz_index" not in st.session_state:
            st.session_state.quiz_index = 0
        if "quiz_score" not in st.session_state:
            st.session_state.quiz_score = 0
        if "answer_submitted" not in st.session_state:
            st.session_state.answer_submitted = False
        if "quiz_completed" not in st.session_state:
            st.session_state.quiz_completed = False

        st.subheader("Active Competency Check")

        if st.session_state.quiz_completed:
            success_rate = st.session_state.quiz_score / total_questions
            st.metric("Final Score Assessment", f"{st.session_state.quiz_score} / {total_questions}", f"{int(success_rate * 100)}% Pass Metric")
            
            if success_rate >= 0.70:
                st.success("🏆 EXCELLENT WORK! You passed the benchmark capability threshold for this domain. You are cleared to advance straight onto the next milestone section.")
            else:
                st.warning("⚠️ BENCHMARK NOT MET: Score fell below the target 70% proficiency barrier. The system recommends routing back to your curated MS Learn resources to fortify weak areas.")
            
            col_retry, col_skip = st.columns(2)
            with col_retry:
                if st.button("Restart Quiz Module", type="primary"):
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.answer_submitted = False
                    st.session_state.quiz_completed = False
                    st.rerun()
            with col_skip:
                if st.button("Force Advance to Next Domain ➡️", type="secondary"):
                    st.info("Bypass route acknowledged. Progressing you onto the next timeline milestone block anyway.")
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.answer_submitted = False
                    st.session_state.quiz_completed = False
                    st.session_state.quiz_text = ""
                    st.rerun()
            return

        current_idx = st.session_state.quiz_index
        current_item = questions_list[current_idx]
        
        progress_percentage = current_idx / total_questions
        st.progress(progress_percentage)
        st.caption(f"Processing Question {current_idx + 1} of {total_questions}")
        
        raw_q_text = current_item.get("question", "Missing Question Text")
        correct_letter = current_item.get("correct_answer", "A").strip().upper()
        explanation = current_item.get("explanation", "")
        
        question_body, display_choices = parse_question_and_options(raw_q_text)
        
        st.write(f"**Question {current_idx + 1}:** {question_body}")
        
        user_selection = st.radio(
            "Choose your target answer option:", 
            display_choices, 
            key=f"active_q_{current_idx}",
            disabled=st.session_state.answer_submitted
        )
        
        selected_letter = user_selection[0]

        if not st.session_state.answer_submitted:
            if st.button("Submit Answer", type="primary"):
                st.session_state.answer_submitted = True
                if selected_letter == correct_letter:
                    st.session_state.quiz_score += 1
                st.rerun()
        else:
            if selected_letter == correct_letter:
                st.success(f"🎉 CORRECT! \n\n**Details:** {explanation}")
            else:
                st.error(f"❌ INCORRECT. The true target was option {correct_letter}. \n\n**Details:** {explanation}")
                
            button_text = "Finish Quiz & View Report" if current_idx + 1 == total_questions else "Next Question ➡️"
            if st.button(button_text, type="primary"):
                if current_idx + 1 == total_questions:
                    st.session_state.quiz_completed = True
                else:
                    st.session_state.quiz_index += 1
                st.session_state.answer_submitted = False
                st.rerun()
                
    except Exception as parse_error:
        st.error("Quiz Display System Offline")
        st.caption(f"Parsing Diagnostic Metrics: {parse_error}")