# 🤖 AI Certification Coach — Your Personal Multi-Agent Study Planner

**Hackathon Track**: Battle #2 — Reasoning Agents with Microsoft Foundry

Studying for a cloud certification is overwhelming. You've got a stack of objectives to cover, a job and a life eating into your free time, and no real way to know if you're spending your hours on the right things. **AI Certification Coach** fixes that.

Tell it which exam you're targeting, how much time you realistically have, and a bit about your background — and a team of specialized AI agents goes to work building you a personalized, week-by-week study plan. Not a generic checklist copy-pasted from a blog, but a roadmap shaped around *your* schedule, *your* gaps, and *your* pace, complete with progress tracking and custom practice quizzes that adapt as you go.

Built natively on **Azure AI Foundry**, this isn't one AI model trying to do everything — it's a coordinated system of agents, each with a specific job, working together the way a real study coach, curriculum designer, and tutor might on a team.

---

## 🎥 Demo Video

Watch the full demo here: https://youtu.be/w72ZexuFnR4

---

## 💡 What Makes This Different

Most "AI study planners" are just a chatbot wrapper — you ask a question, it generates some text, and you hope the numbers add up. We took a different approach:

- **No made-up timelines.** Your study hours are calculated using real math (the Largest Remainder Method — the same proportional allocation logic used in elections and budgeting), not an AI's best guess at what "sounds reasonable."
- **Specialized agents, not one overloaded model.** A profiler figures out your skill gaps, a planner does the scheduling math, a curator finds the right learning resources, an examiner builds your quizzes, and a reviewer keeps the whole plan realistic and sustainable.
- **Built-in burnout protection.** The system actively checks whether your plan is realistic for a human being, not just mathematically possible, and flags it if you're scheduling yourself into the ground.
- **Live progress tracking.** Check off completed weeks and watch your remaining workload automatically rebalance in real time.

---

## 🛠️ How It Works: The Agent Pipeline

Think of this less like "asking ChatGPT a question" and more like an assembly line, where each station is a specialist agent with one job to do well.

```text
      [ User Inputs ] ==> [ input_validation.py ]
                                    │
                                    ▼ (Pydantic LearnerProfile)
                        ┌───────────────────────┐
                        │ agents/profiler.py    │ (Profiler Agent)
                        └───────────┬───────────┘
                                    ▼
       ┌────────────────────────────┴────────────────────────────┐
       │ (Parallel Fan Out via ThreadPoolExecutor)                │
       ▼                                                          ▼
┌───────────────────────┐                                 ┌───────────────────────┐
│ agents/planner.py     │ (Largest Remainder Math)        │ agents/curator.py     │ (Curator Agent)
└───────────┬───────────┘                                 └───────────┬───────────┘
            ▼                                                          ▼
            └───────────────────────┬──────────────────────────────────┘
                                    ▼ (Combined Context)
                        ┌───────────────────────┐
                        │ agents/executor.py    │ (Auditor and Quiz Agent)
                        └───────────┬───────────┘
                                    ▼
                        ┌───────────────────────┐
                        │ agents/reviewer.py    │ (Adaptive Coach Agent)
                        └───────────────────────┘
```

**Summarized breakdown:**

1. **You** tell the system your target certification, available study time, and background.
2. The **Profiler Agent** reads your background and figures out where your knowledge gaps are relative to the exam objectives.
3. Two agents run **in parallel** (at the same time, to save you wait time):
   - The **Planner Agent** crunches the numbers — turning your available hours into a precise, proportionally-balanced weekly schedule using deterministic math, not AI guesswork.
   - The **Curator Agent** matches your gaps to relevant study materials and learning paths.
4. The **Executor Agent** combines everything, audits the plan for quality, and generates custom practice quizzes targeting your weak spots.
5. The **Reviewer Agent** does a final sanity check — making sure the plan is realistic, sustainable, and won't burn you out — before handing you the finished study path.

---

## ⚙️ Advanced Engineering Highlights

For the technical reviewers — here's what's under the hood:

- **Typed Data Contracts**: All data passed between agents flows through strict Pydantic models, eliminating fragile string-parsing at module boundaries and catching malformed data before it ever reaches the cloud model.
- **Proportional Hour Distribution**: Study hours are allocated using the Largest Remainder Method, a deterministic apportionment algorithm — guaranteeing your time budget always sums correctly and is distributed fairly across domains, with zero AI hallucination involved in the math.
- **Asynchronous Multi-Threading**: Independent agent calls (Planner and Curator) are fired concurrently via a `ThreadPoolExecutor`, cutting end-to-end latency by up to 50% compared to sequential calls.
- **Burnout Safety Interceptors**: A dedicated review pass checks the generated calendar against healthy study-load heuristics and surfaces automated alerts if the plan looks unsustainable.

---

## ⚙️ Environment Setup and Credentials

### Step 1: Establish Azure Project Context

Create a file named `.env` in this directory and add your Azure AI Foundry connection details:
Azure AI Foundry Connection Parameter
AZURE_AI_PROJECT_CONNECTION_STRING=your_connection_string_here
Target Cloud Model Deployment Parameter
AZURE_AI_MODEL_DEPLOYMENT=gpt-4o

### Step 2: Virtual Environment Configuration

Activate your virtual environment and install the required packages:

```bash
pip install streamlit pytest pydantic openai
```

---

## 🚀 Try It Yourself

### 1. Launch the Web Dashboard

For the full interactive experience:

```bash
streamlit run frontend/ui_app.py
```

### 2. Run the Command-Line Version

For a lightweight, terminal-based run:

```bash
python app.py
```

---

## 🧪 Automated Testing Matrix

The repository ships with a full automated test suite covering the math distribution logic and UI rendering, so the core orchestration stays reliable as the codebase evolves.

Run the full suite from the project root:

```bash
pytest
```

All seven verification tracks pass in under three seconds, using built-in rule-based mock fallbacks so testing never burns your cloud token budget.
