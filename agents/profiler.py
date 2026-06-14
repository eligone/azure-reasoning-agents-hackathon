import json
from client_factory import get_cloud_client, get_model_target

def run_learner_profiler(exam_target, free_text_background=None):
    """
    Agent 4 Module: Evaluates loose background text and converts it into 
    quantitative, exam-specific capability score ratings.
    """
    client = get_cloud_client()
    model = get_model_target()
    
    persona = (
        "You are an elite technical career profiling analyst. Your job is to assess a user's technical background "
        "and determine their experience level for core topics relevant to their target certification exam.\n\n"
        "CRITICAL: You must return your response as a valid JSON object. Do not wrap it in markdown code blocks. "
        "The JSON must contain a single key 'domain_ratings' which maps key certification subjects to a score from 1 to 5 "
        "(1 being completely new, 5 being highly experienced).\n\n"
        "Example format:\n"
        '{"domain_ratings": {"Core Infrastructure": 2, "Security Design": 4}}'
    )
    
    background_context = free_text_background if free_text_background else "No background provided. Assume baseline beginner settings."
    user_prompt = f"Analyze this background profile for someone taking the {exam_target} certification:\n{background_context}"
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        
        cleaned_text = response.choices[0].message.content.strip()
        # Strip out any lazy markdown formatting wrappers if the model includes them
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        ratings_data = json.loads(cleaned_text.strip())
        return ratings_data.get("domain_ratings", {})
    except Exception:
        # Fallback safe dictionary if a network error logs during profiling
        return {"General Core Domains": 3}