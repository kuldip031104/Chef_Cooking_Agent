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

    # Start conversation
    if not state.get("messages"):
        return "greeting"

    user_input = state["messages"][-1]["content"]

    stage = state.get("stage")

    # ---------- GLOBAL INTERRUPTS ----------

    text = user_input.lower()

    if "restart" in text or "new recipe" in text:
        state["stage"] = "collect_preferences"
        return "collect_preferences"

    if "next" in text or "continue" in text:
        return "step_mode"

    if text.isdigit() and stage == "collect_feedback":
        return "collect_feedback"

    # ---------- STATE SUMMARY ----------

    state_summary = f"""
stage={stage}
people={state.get("number_of_people")}
spice={state.get("spice_level")}
region={state.get("region_preference")}
recipe_generated={bool(state.get("recipe"))}
step_mode={bool(state.get("steps"))}
current_step={state.get("current_step")}
rating={state.get("rating")}
"""

    prompt = f"""
{SUPERVISOR_PROMPT}

Current state:
{state_summary}

User message:
{user_input}

Decide the best next agent.
"""

    try:

        result = llm.with_structured_output(RouteDecision).invoke(prompt)

        print("Supervisor decision:", result)

        return result.action

    except Exception as e:

        print("Supervisor error:", e)

        return "regular_chat"