from client_factory import get_cloud_client, get_model_target

def run_syllabus_planner(certification_name, days_per_week, hours_per_day, revision_feedback=None):
    client = get_cloud_client()
    model = get_model_target()
    
    persona = (
        "You are an expert technical curriculum designer. Your job is to create a realistic, balanced study timeline "
        "based strictly on the user's weekly availability limits.\n\n"
        "CRITICAL FORMATTING CONSTRAINT:\n"
        "Do not write day-by-day breakdowns. Never write 'Day 1, Day 2, Day 3' or list out 40 individual days. "
        "Instead, group the schedule strictly by 'Weeks' or multi-day theme blocks (e.g., 'Week 1: Focus on X', 'Days 1-3: Core Concepts'). "
        "Keep the document concise, high-level, and easy to skim."
    )
    
    user_prompt = f"I need a study roadmap for the {certification_name} certification. I can only study {hours_per_day} hours a day for {days_per_week} days a week."
    
    if revision_feedback:
        user_prompt += f"\n\nYour previous draft was flagged by the reviewer. Please adapt and shorten using their feedback: {revision_feedback}"
        
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content