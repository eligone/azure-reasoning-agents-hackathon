from client_factory import get_cloud_client, get_model_target

def run_syllabus_planner(certification_name, days_per_week, hours_per_day, revision_feedback=None):
    client = get_cloud_client()
    model = get_model_target()
    
    persona = "You are an expert technical curriculum designer. Your job is to create a realistic, balanced study timeline based strictly on the user's weekly availability limits."
    
    user_prompt = f"I need a study roadmap for the {certification_name} certification. I can only study {hours_per_day} hours a day for {days_per_week} days a week."
    
    # If Agent 2 sent back critiques, force Agent 1 to read them and adjust
    if revision_feedback:
        user_prompt += f"\n\nYour previous draft was rejected by the reviewer. Please completely rewrite the timeline using their feedback: {revision_feedback}"
        
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content