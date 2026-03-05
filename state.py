from typing import TypedDict, List, Optional


class ChefState(TypedDict, total=False):

    # Conversation
    messages: List[dict]
    user_id: str

    # Workflow control
    stage: Optional[str]

    # Preferences
    number_of_people: Optional[int]
    spice_level: Optional[str]
    region_preference: Optional[str]
    preference_type: Optional[str]
    allergies: Optional[str]

    # Recipe
    recipe: Optional[dict]
    steps: Optional[List[str]]
    current_step: Optional[int]

    # Feedback
    rating: Optional[int]