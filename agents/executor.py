import json
from client_factory import get_cloud_client, get_model_target

def evaluate_study_plan(syllabus_context, days_per_week, hours_per_day):
    client = get_cloud_client()
    model = get_model_target()
    
    persona = "You are a tough technical mentor and auditor. Review the provided study timeline. If the amount of material suggested for a week looks impossible to finish in the given study hours, output 'REJECT: ' followed by explicit instructions on what to cut or slow down. If it looks balanced and perfectly reasonable, output 'APPROVED'."
    user_prompt = f"Review this plan: {syllabus_context}\n\nRemember, the student can only study {hours_per_day} hours a day, {days_per_week} days a week."
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def run_assessment_executor(syllabus_context, specific_topic=None):
    """
    Generates 5 realistic multiple-choice questions returning a strict JSON array string.
    """
    client = get_cloud_client()
    model = get_model_target()
    
    persona = (
        "You are an elite technical cloud architect evaluator writing practice questions for an advanced Microsoft certification.\n\n"
        "CRITICAL: You must return your response as a valid JSON array containing exactly 5 objects. Do not wrap it in markdown code blocks like ```json. Just return raw text.\n"
        "Each object must have these exact keys:\n"
        "- 'question': The text of the scenario question and options formatted cleanly with newlines.\n"
        "- 'correct_answer': A single capital letter ('A', 'B', 'C', or 'D').\n"
        "- 'explanation': An architectural description of why that option is correct.\n"
    )
    
    target = f"the initial foundational core concepts listed in this syllabus:\n{syllabus_context}"
    if specific_topic:
        target = f"a deep-dive retry session focused strictly on mastering the domain concept of: '{specific_topic}'"
        
    user_prompt = f"Review the requirements and generate 5 scenario questions for {target}"
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content