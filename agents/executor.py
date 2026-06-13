from client_factory import get_cloud_client, get_model_target

def run_assessment_executor(syllabus_context):
    client = get_cloud_client()
    model = get_model_target()
    
    persona = "You are an elite technical evaluator. Take the structured milestone sections passed to you by the planner and generate three realistic, challenging multiple-choice practice questions to test exam readiness."
    user_prompt = f"Using this specific syllabus roadmap context, generate the practice exam questions now:\n{syllabus_context}"
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content