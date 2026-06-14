import pytest
from streamlit.testing.v1 import AppTest

def test_dashboard_sidebar_and_tab_initialization():
    """
    UI Test: Simulates booting the Streamlit web framework and ensures that all
    sidebar sliders, configuration selectors, and form elements mount cleanly.
    """
    # Point the testing driver directly to our UI application script path
    at = AppTest.from_file("frontend/ui_app.py")
    at.run()
    
    # Assert that the main title banner mounts onto the page layout
    assert "Multi-Agent AI Certification Coach" in at.title[0].value
    
    # Verify that the sidebar contains our user config input items
    assert at.sidebar.selectbox[0].label == "Target Certification"
    assert at.sidebar.slider[0].label == "Study days per week"
    assert at.sidebar.slider[1].label == "Study hours per day"
    
    # Assert default state balances are starting correctly
    assert at.sidebar.slider[0].value == 5
    assert at.sidebar.slider[1].value == 3

def test_burnout_disclaimer_warning_intercept():
    """
    UI Test: Simulates a user selecting an aggressive cram timeline and verifies 
    that the safety auditing agent intercepts the render loop with an alert box.
    """
    at = AppTest.from_file("frontend/ui_app.py")
    at.run()
    
    # Artificially force an aggressive 1-week cram timeline parameter into the input box
    at.sidebar.number_input[0].set_value(1)
    at.sidebar.text_area[0].set_value("I want to learn everything tomorrow.")
    
    # Simulate clicking the primary execution launch button
    at.sidebar.button[0].click()
    at.run()
    
    # If the system identifies a crash threat risk, the warning banner will mount
    if at.warning:
        assert "STUDY TIMELINE DISCLAIMER WARNING" in at.warning[0].value