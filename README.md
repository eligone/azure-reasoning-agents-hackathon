# 🤖 My Personalized Multi Agent AI Certification Coach

**Track**: Battle #2 — Reasoning Agents with Microsoft Foundry

An intelligent data driven multi agent system optimized to construct balanced study paths for professional cloud certifications. By converting qualitative text descriptions into quantitative domain metrics, the system models personal timelines using deterministic math loops, runs quality reviews, and provides interactive tracking tools.

This application is built to run natively within the Azure AI Foundry ecosystem.

---

## 🛠️ System Overview and Architecture

Our application distributes processing responsibilities across an interconnected assembly line of specialized agents rather than relying on loose text handoffs.

```text
      [ User Inputs ] ==> [ input_validation.py ]
                                    │
                                    ▼ (Pydantic LearnerProfile)
                        ┌───────────────────────┐
                        │ agents/profiler.py    │ (Profiler Agent)
                        └───────────┬───────────┘
                                    ▼
       ┌────────────────────────────┴────────────────────────────┐
       │ (Parallel Fan Out via ThreadPoolExecutor)               │
       ▼                                                         ▼
┌───────────────────────┐                                 ┌───────────────────────┐
│ agents/planner.py     │ (Largest Remainder Math)        │ agents/curator.py     │ (Curator Agent)
└───────────┬───────────┘                                 └───────────┬───────────┘
            ▼                                                         ▼
            └───────────────────────┬─────────────────────────────────┘
                                    ▼ (Combined Context)
                        ┌───────────────────────┐
                        │ agents/executor.py    │ (Auditor and Quiz Agent)
                        └───────────┬───────────┘
                                    ▼
                        ┌───────────────────────┐
                        │ agents/reviewer.py    │ (Adaptive Coach Agent)
                        └───────────────────────┘
Advanced Engineering Highlights
Typed Data Contracts: Wipes out unstable string parsing at file boundaries by tracking data states inside secure Pydantic containers.

Proportional Hour Distribution: Uses the mathematical Largest Remainder Method to calculate study targets, preventing the cloud model from inventing random timelines.

Asynchronous Multi Threading: Fires off independent model actions simultaneously using parallel worker pools to cut down user wait times by up to fifty percent.

Burnout Safety Interceptors: A dedicated quality supervisor checks the calendar logic to protect user health with automated alert notifications.

⚙️ Environment Setup and Credentials
Step 1: Establish Azure Project Context
Ensure your local configurations are exported inside your workspace environment file to connect with Azure AI Foundry endpoints. Create a file named .env in this directory:

Code snippet
# Azure AI Foundry Connection Parameter
AZURE_AI_PROJECT_CONNECTION_STRING=your_connection_string_here

# Target Cloud Model Deployment Parameter
AZURE_AI_MODEL_DEPLOYMENT=gpt-4o
Step 2: Virtual Environment Configuration
Activate your virtual environment and install the verified project packages:

Bash
pip install streamlit pytest pydantic openai
🚀 Execution Guides
1. Launch the Web Interface Dashboard
To boot up the interactive graphical presentation layout, run this command:

Bash
streamlit run frontend/ui_app.py
2. Run the Command Line Version
To run the application architecture directly inside a standard console shell session, execute:

Bash
python app.py
🧪 Automated Testing Matrix
To protect the application orchestration modules from regressions or code drift, the repository is packed with robust automated tests covering math distributions and interface rendering.

Execute the test pipeline directly from your root folder location:

Bash
pytest
All seven verification tracks pass completely under three seconds using built in rule based mock fallbacks to shield your cloud token budgets during evaluation.
```
