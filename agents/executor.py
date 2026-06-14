from client_factory import get_cloud_client, get_model_target

def evaluate_study_plan(syllabus_context, days_per_week, hours_per_day):
    """
    Agent 2 checks if the generated timeline fits inside the user's time constraints.
    """
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

def run_assessment_executor(syllabus_context):
    """
    Generates practice questions once the plan is fully approved.
    """
    client = get_cloud_client()
    model = get_model_target()
    
    persona = "You are an elite technical evaluator. Take the approved milestone sections and generate three realistic multiple-choice practice questions."
    user_prompt = f"Generate the practice exam questions for this syllabus now:\n{syllabus_context}"
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content