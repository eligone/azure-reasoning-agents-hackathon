from pydantic import BaseModel, Field
from typing import Dict

class LearnerProfile(BaseModel):
    exam_target: str
    days_per_week: int = Field(..., ge=1, le=7)
    hours_per_day: int = Field(..., ge=1, le=24)
    target_weeks: int = Field(..., ge=1)
    total_hour_budget: int
    domain_ratings: Dict[str, int] = Field(default_factory=dict) # Added slot container