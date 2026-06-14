def get_validated_exam():
    """
    Displays a strict numeric menu for selecting a valid Azure certification,
    completely blocking arbitrary or invalid text input.
    """
    # Explicitly mapped certifications to guarantee valid targets
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