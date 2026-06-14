import streamlit as st
import json

def parse_question_and_options(raw_question_text):
    """
    Helper Utility: Automatically parses text blocks to isolate the core 
    question from its inline alphanumeric option strings (A, B, C, D).
    """
    text = raw_question_text
    options = ["A", "B", "C", "D"]
    parsed_options = {}
    
    # Locate the split markers dynamically inside the string payload
    idx_a = text.find("A)")
    idx_b = text.find("B)")
    idx_c = text.find("C)")
    idx_d = text.find("D)")
    
    # If standard text split markers exist, extract the clean substrings
    if idx_a != -1 and idx_b != -1 and idx_c != -1 and idx_d != -1:
        question_body = text[:idx_a].strip()
        parsed_options["A"] = text[idx_a:idx_b].replace("A)", "").strip()
        parsed_options["B"] = text[idx_b:idx_c].replace("B)", "").strip()
        parsed_options["C"] = text[idx_c:idx_d].replace("C)", "").strip()
        parsed_options["D"] = text[idx_d:].replace("D)", "").strip()
        
        # Format the display list to show the content option next to its target key bubble
        display_choices = [
            f"A: {parsed_options['A']}",
            f"B: {parsed_options['B']}",
            f"C: {parsed_options['C']}",
            f"D: {parsed_options['D']}"
        ]
        return question_body, display_choices
        
    # Standard fallback safety layout if the raw text is formatted unexpectedly
    return text, options

def render_interactive_quiz(raw_quiz_json_string):
    """
    Parses raw JSON strings from Agent 2 and renders them 
    as clickable, interactive radio button option modules.
    """
    if not raw_quiz_json_string:
        st.info("No assessment metrics generated yet. Click the button above to begin.")
        return

    try:
        cleaned_json = raw_quiz_json_string.replace('\\n', '\n').strip()
        questions_list = json.loads(cleaned_json, strict=False)
        
        st.subheader("📝 Active Competency Check")
            
        for index, item in enumerate(questions_list):
            raw_q_text = item.get("question", "Missing Question Text")
            correct_letter = item.get("correct_answer", "A").strip().upper()
            explanation = item.get("explanation", "")
            
            # Split our string metrics using our new custom parser function
            question_body, display_choices = parse_question_and_options(raw_q_text)
            
            st.write(f"**Question {index + 1}:** {question_body}")
            
            # Render the radio buttons with the text definitions cleanly attached next to each choice
            user_selection = st.radio(
                f"Choose your answer for Question {index + 1}:", 
                display_choices, 
                key=f"q_radio_{index}"
            )
            
            # Extract the raw starting option letter chosen by the user
            selected_letter = user_selection[0]
            
            if st.button(f"Submit Answer {index + 1}", key=f"q_btn_{index}"):
                if selected_letter == correct_letter:
                    st.success(f"🎉 CORRECT! \n\n**Details:** {explanation}")
                else:
                    st.error(f"❌ INCORRECT. The true target was option {correct_letter}. \n\n**Details:** {explanation}")
            st.write("---")
            
    except Exception as parse_error:
        st.error("Quiz Display System Offline")
        st.caption(f"Parsing Diagnostic Metrics: {parse_error}")
        st.text_area("Raw Data Source Output Frame", value=raw_quiz_json_string, height=150, disabled=True)