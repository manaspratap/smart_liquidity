from enum import Enum

class Purpose(Enum):
    EMERGENCY = "emergency"
    PLANNED_PURCHASE = "planned_purchase"
    LOAN_REPAYMENT = "loan_repayment"
    OTHER = "other"

class Timeline(Enum):
    IMMEDIATE = "immediate"
    WITHIN_WEEK = "within_week"
    ONE_TO_FOUR_WEEKS = "1-4_weeks"
    NO_URGENCY = "no_urgency"

class SEBIRiskCategory(Enum):
    LOW = "low"
    MODERATELY_LOW = "moderately_low"
    MODERATE = "moderate"
    MODERATELY_HIGH = "moderately_high"
    HIGH = "high"
    VERY_HIGH = "very_high" 