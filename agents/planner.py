from client_factory import get_cloud_client, get_model_target

def run_syllabus_planner(certification_name):
    client = get_cloud_client()
    model = get_model_target()
    
    persona = "You are an expert technical curriculum designer. Take the requested certification exam name, break its domain requirements down into explicit milestone sub-sections, and output a structured learning timeline."
    user_prompt = f"I need a study milestone timeline for the {certification_name} certification."
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content