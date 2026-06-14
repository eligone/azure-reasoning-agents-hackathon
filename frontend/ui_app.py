import sys
import os

# Append the absolute parent path workspace so Python can resolve our core module dependencies
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import concurrent.futures
from models import LearnerProfile
from agents.profiler import run_learner_profiler
from agents.planner import run_syllabus_planner
from agents.curator import run_learning_curator
from agents.executor import evaluate_study_plan, run_assessment_executor
from time_distributor import distribute_study_hours

# Import our custom frontend component module
from frontend.quiz_component import render_interactive_quiz

st.set_page_config(page_title="Multi-Agent AI Coach", page_icon="🤖", layout="wide")

st.title("🤖 My Personalized Multi-Agent AI Certification Coach")
st.write("Construct data-driven, algorithmically balanced study plans optimized to your exact technical background.")

if "pipeline_ready" not in st.session_state:
    st.session_state.pipeline_ready = False
if "warning_triggered" not in st.session_state:
    st.session_state.warning_triggered = False
if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""
if "resources" not in st.session_state:
    st.session_state.resources = ""
if "hours_allocation" not in st.session_state:
    st.session_state.hours_allocation = {}
if "quiz_text" not in st.session_state:
    st.session_state.quiz_text = ""
if "active_profile" not in st.session_state:
    st.session_state.active_profile = None

# Initialize persistent progress tracking structures
if "completed_milestones" not in st.session_state:
    st.session_state.completed_milestones = set()

with st.sidebar:
    st.header("Plan Configurations")
    cert_options = [
        "Azure Fundamentals (AZ-900)",
        "Azure Developer Associate (AZ-204)",
        "Azure Administrator Associate (AZ-104)",
        "Azure Solutions Architect Expert (AZ-305)",
        "Azure AI Engineer Associate (AI-102)",
        "Azure Data Engineer Associate (DP-203)"
    ]
    selected_cert = st.selectbox("Target Certification", cert_options)
    
    days_per_week = st.slider("Study days per week", min_value=1, max_value=7, value=5)
    hours_per_day = st.slider("Study hours per day", min_value=1, max_value=24, value=3)
    target_weeks = st.number_input("Target timeline duration (weeks)", min_value=1, max_value=52, value=4)
    
    st.write("---")
    st.subheader("Experience Customization")
    background_input = st.text_area(
        "Describe your technical background:",
        placeholder="e.g., I understand SQL and data concepts, but I am entirely new to stream processing tools."
    )
    
    generate_clicked = st.button("Generate Smart Study Pipeline", type="primary")

if generate_clicked:
    st.session_state.pipeline_ready = False
    st.session_state.warning_triggered = False
    st.session_state.quiz_text = ""  # Reset quiz on a new profile run
    st.session_state.completed_milestones = set()  # Reset completed tracking logs
    
    # Flush out old multi-turn quiz tracking states to allow a fresh evaluation session
    if "quiz_index" in st.session_state: del st.session_state.quiz_index
    if "quiz_score" in st.session_state: del st.session_state.quiz_score
    if "answer_submitted" in st.session_state: del st.session_state.answer_submitted
    if "quiz_completed" in st.session_state: del st.session_state.quiz_completed
    
    with st.spinner("Invoking multi-agent pipeline layers..."):
        total_budget = days_per_week * hours_per_day * target_weeks
        
        profile = LearnerProfile(
            exam_target=selected_cert,
            days_per_week=days_per_week,
            hours_per_day=hours_per_day,
            target_weeks=target_weeks,
            total_hour_budget=total_budget
        )
        
        calculated_ratings = run_learner_profiler(profile.exam_target, background_input)
        profile.domain_ratings = calculated_ratings
        st.session_state.active_profile = profile
        
        hours_map = distribute_study_hours(
            profile.domain_ratings,
            profile.target_weeks,
            profile.days_per_week,
            profile.hours_per_day
        )
        st.session_state.hours_allocation = hours_map
        
        hours_breakdown_str = ", ".join([f"Spend exactly {h} hours on {d}" for d, h in hours_map.items()])
        feedback_constraints = f"MUST FIT IN EXACTLY {target_weeks} WEEKS. Constraints: {hours_breakdown_str}"
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_plan = executor.submit(
                run_syllabus_planner, 
                profile.exam_target, 
                profile.days_per_week, 
                profile.hours_per_day, 
                feedback_constraints
            )
            future_resources = executor.submit(
                run_learning_curator, 
                profile.exam_target, 
                profile.domain_ratings
            )
            
            st.session_state.roadmap = future_plan.result()
            st.session_state.resources = future_resources.result()

        audit_result = evaluate_study_plan(st.session_state.roadmap, profile.days_per_week, profile.hours_per_day)
        
        if audit_result.startswith("REJECT") or f"{target_weeks} weeks" not in st.session_state.roadmap.lower():
            st.session_state.warning_triggered = True
        else:
            st.session_state.pipeline_ready = True

if st.session_state.warning_triggered and not st.session_state.pipeline_ready:
    st.warning("⚠️ MULTI-AGENT SYSTEM NOTICE: STUDY TIMELINE DISCLAIMER WARNING")
    st.write(
        f"Our auditing agent notes that trying to master all domains for your selected certification "
        f"within {st.session_state.active_profile.target_weeks} weeks under your current availability profile is highly discouraged."
    )
    st.write("The schedule will feel severely crammed, and you risk hitting immediate burnout.")
    
    col_force, col_abort = st.columns(2)
    with col_force:
        if st.button("Override Warning & Build Anyway", type="secondary"):
            st.session_state.pipeline_ready = True
            st.rerun()
    with col_abort:
        if st.button("Abort Session", type="primary"):
            st.session_state.warning_triggered = False
            st.session_state.active_profile = None
            st.rerun()

if st.session_state.pipeline_ready:
    dashboard_tabs = st.tabs(["📋 Syllabus & Resources", "🧠 Interactive Domain Quiz"])
    
    with dashboard_tabs[0]:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.header("📝 Custom Certification Roadmap")
            
            # Interactive Progress Tracking Checklist Panel
            st.subheader("🏁 Track Your Progress Below")
            st.write("Check off your completed segments to watch your dashboard chart update live.")
            
            # Draw individual checklist nodes matching the planned timeline
            total_weeks_planned = st.session_state.active_profile.target_weeks
            for w in range(1, total_weeks_planned + 1):
                milestone_key = f"Week {w}"
                is_checked = milestone_key in st.session_state.completed_milestones
                
                if st.checkbox(f"Mark {milestone_key} Milestone as Fully Complete", value=is_checked, key=f"check_{w}"):
                    st.session_state.completed_milestones.add(milestone_key)
                else:
                    st.session_state.completed_milestones.discard(milestone_key)
            
            st.write("---")
            st.markdown(st.session_state.roadmap)
            
        with col2:
            st.header("📊 Algorithmic Hours Allocation")
            
            # Dynamically compute remaining study targets to pass to the graphic visualizer
            completed_count = len(st.session_state.completed_milestones)
            completion_factor = max(0.0, 1.0 - (completed_count / total_weeks_planned))
            
            # Scale down the displayed bar values based on user completion ticks
            live_chart_data = {domain: int(hours * completion_factor) for domain, hours in st.session_state.hours_allocation.items()}
            
            st.bar_chart(live_chart_data)
            
            # Display tracking feedback labels
            if completed_count == total_weeks_planned:
                st.success("🎉 All objectives met! You are 100% prepared to sit your certification exam.")
            else:
                st.metric("Timeline Milestone Progress", f"{completed_count} / {total_weeks_planned} Weeks", f"{int((completed_count/total_weeks_planned)*100)}% Complete")
            
            st.write("---")
            for domain, target_hours in st.session_state.hours_allocation.items():
                st.info(f"**{domain}**: {target_hours} total hours allocated")
                
            st.header("📚 Recommended MS Learn Resources")
            st.markdown(st.session_state.resources)
            
    with dashboard_tabs[1]:
        st.header("🧠 Domain Knowledge Check")
        st.write("Evaluate your comprehension metrics against your generated study targets below.")
        
        if st.button("Generate Domain Practice Questions"):
            with st.spinner("Invoking Agent 2 to design technical assessment queries..."):
                weak_areas = [d for d, r in st.session_state.active_profile.domain_ratings.items() if r <= 3]
                focus_topics = ", ".join(weak_areas) if weak_areas else "Core Fundamentals"
                
                st.session_state.quiz_text = run_assessment_executor(
                    st.session_state.active_profile.exam_target,
                    specific_topic=f"Focus deeply on these technical sub-domains: {focus_topics}"
                )
        
        if st.session_state.quiz_text:
            render_interactive_quiz(st.session_state.quiz_text)