from models import LearnerProfile

def get_validated_exam():
    """
    Displays a strict numeric menu for selecting a valid Azure certification,
    completely blocking arbitrary or invalid text input.
    """
    azure_certs = {
        1: "Azure Fundamentals (AZ-900)",
        2: "Azure Developer Associate (AZ-204)",
        3: "Azure Administrator Associate (AZ-104)",
        4: "Azure Solutions Architect Expert (AZ-305)",
        5: "Azure AI Engineer Associate (AI-102)",
        6: "Azure Data Engineer Associate (DP-203)"
    }
    
    while True:
        print("\nAvailable Azure Certifications:")
        for key, name in azure_certs.items():
            print(f"  {key}. {name}")
            
        user_choice = input("\nSelect a certification by entering its number (1-6): ").strip()
        
        try:
            choice_num = int(user_choice)
            if choice_num in azure_certs:
                selected_cert = azure_certs[choice_num]
                print(f"✅ Selected: {selected_cert}")
                return selected_cert
            else:
                print(f"❌ Selection out of bounds. Please pick a number from 1 to {len(azure_certs)}.")
        except ValueError:
            print("❌ Invalid input. Please enter a clean, whole number integer matching the menu options.")

def get_validated_number(prompt, min_val, max_val, unit_name):
    """
    Validates numeric console entries and forces inputs to match target constraints.
    """
    while True:
        raw_input = input(prompt).strip()
        try:
            value = int(raw_input)
            if min_val <= value <= max_val:
                return value
            print(f"❌ Outside logical range: Please enter a number between {min_val} and {max_val} for {unit_name}.")
        except ValueError:
            print("❌ Numeric mismatch: Please enter a clean, whole number integer.")

def get_study_duration_weeks():
    """
    Asks the user how many total weeks they want to finish their study plan within.
    """
    return get_validated_number(
        "In how many weeks do you want to complete this certification study plan? ", 
        1, 
        52, 
        "weeks"
    )

def gather_full_learner_profile():
    """
    Master collection wrapper. Gathers all user parameters, computes 
    the absolute time metrics, and instantiates the rigid Pydantic contract object.
    """
    selected_exam = get_validated_exam()
    days_per_week = get_validated_number("How many days a week can you dedicate to studying? ", 1, 7, "days")
    hours_per_day = get_validated_number("How many hours per day can you study on those days? ", 1, 24, "hours")
    target_weeks = get_study_duration_weeks()
    
    # Capture qualitative background for our new profiling agent pipeline
    print("\nOptional Profile Customization:")
    background_text = input("Describe your background experience or focus areas (or press enter to skip): ").strip()
    
    total_budget = days_per_week * hours_per_day * target_weeks
    
    profile = LearnerProfile(
        exam_target=selected_exam,
        days_per_week=days_per_week,
        hours_per_day=hours_per_day,
        target_weeks=target_weeks,
        total_hour_budget=total_budget
    )
    
    # Return both the profile contract and the raw background descriptive string to main
    return profile, background_text if background_text else None