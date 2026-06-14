from client_factory import get_cloud_client, get_model_target

def run_learning_curator(exam_target, domain_ratings):
    """
    Agent 5 Module: Compiles a targeted set of trusted MS Learn documentation 
    topics and references based on the calculated weak areas.
    """
    client = get_cloud_client()
    model = get_model_target()
    
    # Format a string summarizing our weakness areas for the model context
    weak_areas = [domain for domain, rating in domain_ratings.items() if rating <= 2]
    focus_context = ", ".join(weak_areas) if weak_areas else "All foundational core domains"
    
    persona = (
        "You are an expert technical curriculum curator. Your job is to provide exactly three highly specific "
        "topic modules or official reference concepts that the student must read on Microsoft Learn to pass their exam. "
        "Focus your suggestions primarily on these prioritized target weak areas: " + focus_context + ".\n\n"
        "Keep your output clean, brief, and formatted as a bulleted list with conceptual reference details."
    )
    
    user_prompt = f"Provide 3 critical structural Microsoft Learn topic areas for an engineer studying for the {exam_target}."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as err:
        return f"Learning Path Resource Curation temporarily offline: {err}"