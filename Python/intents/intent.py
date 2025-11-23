from enum import Enum

class Intent(Enum):
    """User intent types."""
    StaffLookup = "StaffLookup"
    CourseInfo = "CourseInfo"
    Policy = "Policy"
    Unknown = "Unknown"
