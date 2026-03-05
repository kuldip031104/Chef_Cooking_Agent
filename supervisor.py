import json
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from llm import llm
from Prompts.supervisor_prompt import SUPERVISOR_PROMPT

load_dotenv()


class RouteDecision(BaseModel):
    thought: str
    action: Literal[
        "greeting",
        "collect_preferences",
        "generate_recipe",
        "step_mode",
        "collect_feedback",
        "regular_chat",
        "guardrail"
    ]


def supervisor_router(state):

    # If no messages → start conversation
    if not state.get("messages"):
        return "greeting"

    # Ensure stage exists
    stage = state.get("stage")

    # Deterministic routing first (prevents loops)
    if stage == "collect_preferences":
        return "collect_preferences"

    if stage == "generate_recipe":
        return "generate_recipe"

    if stage == "step_mode":
        return "step_mode"

    if stage == "collect_feedback":
        return "collect_feedback"

    # Otherwise let LLM decide
    user_input = state["messages"][-1]["content"]

    state_summary = f"""
    stage={state.get("stage")}
    people={state.get("number_of_people")}
    spice={state.get("spice_level")}
    region={state.get("region_preference")}
    recipe_generated={bool(state.get("recipe"))}
    step_mode={bool(state.get("steps"))}
    current_step={state.get("current_step")}
    rating={state.get("rating")}
    """

    full_prompt = (
        SUPERVISOR_PROMPT
        + "\n"
        + state_summary
        + f"\nUser: {user_input}"
    )

    try:
        result = llm.with_structured_output(RouteDecision).invoke(full_prompt)

        print(result)

        return result.action

    except Exception as e:
        print("Supervisor error:", e)

        # Safe fallback
        return "regular_chat"