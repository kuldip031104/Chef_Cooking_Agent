import json
from pydantic import BaseModel
from typing import Literal
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from Prompts.supervisor_prompt import SUPERVISOR_PROMPT
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

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

    if not state.get("messages"):
        return "greeting"

    user_input = state["messages"][-1]["content"]

    state_summary = f"""
    people={state.get("number_of_people")}
    spice={state.get("spice_level")}
    region={state.get("region_preference")}
    recipe={bool(state.get("recipe"))}
    steps={bool(state.get("steps"))}
    current_step={state.get("current_step")}
    rating={state.get("rating")}
    """

    full_prompt = (
        SUPERVISOR_PROMPT
        + "\n"
        + state_summary
        + f"\nUser: {user_input}"
    )

    result = llm.with_structured_output(RouteDecision).invoke(full_prompt)
    print(result)

    return result.action