from client_factory import get_cloud_client, get_model_target

def run_remediation_reviewer(topic_context, score, total):
    """
    Agent 3 Module: Analyzes weak points and generates custom tactical advice.
    """
    client = get_cloud_client()
    model = get_model_target()
    
    persona = (
        "You are an empathetic but highly precise technical remediation tutor. The student just scored poorly "
        "on a specialized cloud topic quiz. Your job is to analyze the topic area, write a highly encouraging, "
        "concise 3-sentence summary explaining the core concept they are missing, and give them a tactical tip "
        "on how to study it better before their next attempt."
    )
    
    user_prompt = f"The student scored {score}/{total} on the topic of '{topic_context}'. Provide your expert feedback summary."
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content