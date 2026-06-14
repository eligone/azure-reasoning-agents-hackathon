import json
import pytest
from unittest.mock import patch, MagicMock
from models import LearnerProfile
from agents.profiler import run_learner_profiler
from quiz_engine import run_interactive_quiz
from time_distributor import distribute_study_hours

def test_learner_profile_valid_bounds():
    """Verifies Pydantic contract instantiation with valid fields."""
    profile = LearnerProfile(
        exam_target="Azure Developer Associate (AZ-204)",
        days_per_week=4,
        hours_per_day=3,
        target_weeks=6,
        total_hour_budget=72,
        domain_ratings={"Compute": 3}
    )
    assert profile.days_per_week == 4
    assert profile.domain_ratings["Compute"] == 3

def test_learner_profile_invalid_day_bounds():
    """Ensures Pydantic blocks out-of-bounds metrics automatically."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        LearnerProfile(
            exam_target="Azure Fundamentals (AZ-900)",
            days_per_week=12,  # Maximum permitted is 7
            hours_per_day=5,
            target_weeks=4,
            total_hour_budget=240
        )

@patch('agents.profiler.get_cloud_client')
@patch('agents.profiler.get_model_target')
def test_agent4_profiler_json_parsing(mock_model, mock_client):
    """
    Simulates Agent 4's cloud environment response and ensures 
    the extraction wrapper converts the text to a clean dictionary object.
    """
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"domain_ratings": {"Cloud Storage": 2, "Databases": 5}}'
    mock_client.return_value.chat.completions.create.return_value = mock_response
    
    ratings = run_learner_profiler("Azure Data Engineer Associate (DP-203)", "I know SQL.")
    
    assert ratings["Cloud Storage"] == 2
    assert ratings["Databases"] == 5

def test_agent2_quiz_content_drift_guard():
    """
    Verifies that the content guardrail successfully passes clean, 
    production-level technical scenarios that are free from meta-text drift.
    """
    valid_ai_output = json.dumps([
        {
            "question": "Which service should you choose to achieve globally distributed, low-latency multi-model storage?",
            "correct_answer": "D",
            "explanation": "Azure Cosmos DB offers turnkey global distribution and multi-model APIs."
        }
    ])
    
    assert "week 1" not in valid_ai_output.lower(), "❌ Content Drift: Agent 2 is writing questions about the timeline text instead of cloud concepts!"
    assert "day 2" not in valid_ai_output.lower(), "❌ Content Drift: Agent 2 is writing questions about the timeline text instead of cloud concepts!"

def test_largest_remainder_distribution_math():
    """
    Verifies that the math module distributes hours inversely to capability profiles
    and avoids floating-point tracking errors.
    """
    mock_ratings = {
        "Weak Domain": 1,   # Needs more study time
        "Strong Domain": 4   # Needs less study time
    }
    
    hours_map = distribute_study_hours(
        domain_ratings=mock_ratings,
        total_weeks=5,
        days_per_week=4,
        hours_per_day=2
    )
    
    assert hours_map["Weak Domain"] > hours_map["Strong Domain"]
    assert sum(hours_map.values()) == 40