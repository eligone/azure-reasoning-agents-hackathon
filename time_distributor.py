def distribute_study_hours(domain_ratings, total_weeks, days_per_week, hours_per_day):
    """
    Applies the Largest Remainder Method to distribute the total day budget 
    across exam domains inversely proportional to the learner's experience ratings.
    """
    total_days_allocated = total_weeks * days_per_week
    
    if not domain_ratings:
        return {}
        
    # Compute inverse weights (lower rating = higher need for study time)
    inverse_weights = {domain: 1.0 / (rating + 0.1) for domain, rating in domain_ratings.items()}
    total_weight = sum(inverse_weights.values())
    
    allocated_days = {}
    remainders = {}
    
    for domain, weight in inverse_weights.items():
        exact_target = (weight / total_weight) * total_days_allocated
        baseline_days = int(exact_target)
        allocated_days[domain] = max(1, baseline_days)
        remainders[domain] = exact_target - baseline_days
        
    current_total = sum(allocated_days.values())
    slack_days = total_days_allocated - current_total
    
    sorted_by_remainder = sorted(remainders.keys(), key=lambda k: remainders[k], reverse=True)
    
    for domain in sorted_by_remainder:
        if slack_days <= 0:
            break
        allocated_days[domain] += 1
        slack_days -= 1
        
    domain_hours_roadmap = {domain: days * hours_per_day for domain, days in allocated_days.items()}
    return domain_hours_roadmap