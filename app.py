import os
from dotenv import load_dotenv
from openai import OpenAI

# Pull our verified environment credentials
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
model_engine = os.environ.get("MODEL_TARGET", "llama3-70b-8192")

if not api_key or "PASTE_YOUR" in api_key:
    raise ValueError("Error: Missing your valid GROQ_API_KEY inside your .env configuration file.")

print("Initializing Live Cloud Multi-Agent Processing Pipeline...")

try:
    # Initialize the core client pointing directly to the live cloud processing tier
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )

    print("\n[Client Route Connected] Invoking Agent 1: Syllabus Planner...")
    
    # Establish Agent 1 Identity and Tasking Instructions
    agent_1_persona = "You are an expert technical curriculum designer. Take the requested certification exam name, break its domain requirements down into explicit milestone sub-sections, and output a structured learning timeline."
    user_request_1 = "I need a study milestone timeline for the Azure Developer Associate AZ-204 certification."

    # Live Cloud Execution for Agent 1
    response_1 = client.chat.completions.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": agent_1_persona},
            {"role": "user", "content": user_request_1}
        ],
        temperature=0.5
    )

    # Capturing dynamic text generation payload from Agent 1
    planner_output = response_1.choices[0].message.content
    print("\n==============================================")
    print("=== AGENT 1 (SYLLABUS PLANNER) RESPONDED ===")
    print("==============================================")
    print(planner_output)

    print("\n[Context Handover] Invoking Agent 2: Assessment Executor...")
    
    # Establish Agent 2 Identity and pass data payload from Agent 1 directly into its context stream
    agent_2_persona = "You are an elite technical evaluator. Take the structured milestone sections passed to you by the planner and generate three realistic, challenging multiple-choice practice questions to test exam readiness."
    user_request_2 = f"Using this specific syllabus roadmap context, generate the practice exam questions now:\n{planner_output}"

    # Live Cloud Execution for Agent 2
    response_2 = client.chat.completions.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": agent_2_persona},
            {"role": "user", "content": user_request_2}
        ],
        temperature=0.5
    )

    print("\n=================================================")
    print("=== AGENT 2 (ASSESSMENT EXECUTOR) RESPONDED ===")
    print("=================================================")
    print(response_2.choices[0].message.content)
    
    print("\nSystem execution clean. Workspace pipeline pristine.")

except Exception as error_log:
    print(f"\nExecution Failed. Technical Trace Log: {error_log}")