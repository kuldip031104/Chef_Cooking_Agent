import json
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from llm import llm
from Prompts.supervisor_prompt import SUPERVISOR_PROMPT
from database import get_last_messages

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

    # If no messages yet
    if not state.get("messages"):
        return "greeting"

    user_input = state["messages"][-1]["content"]
    stage = state.get("stage")

    # ---------- Workflow Stage Lock ----------
    # If we are inside a workflow stage, continue that stage
    if stage in [
        "collect_preferences",
        "generate_recipe",
        "step_mode",
        "collect_feedback"
    ]:
        return stage

    # ---------- State Summary for LLM ----------
    state_summary = f"""
stage={stage}
people={state.get("number_of_people")}
spice={state.get("spice_level")}
region={state.get("region_preference")}
recipe_generated={bool(state.get("recipe"))}
steps_exist={bool(state.get("steps"))}
current_step={state.get("current_step")}
rating={state.get("rating")}
"""

    prompt = f"""
{SUPERVISOR_PROMPT}

Current state:
{state_summary}

User message:
{user_input}

Decide which agent should respond next.
Return JSON only.
"""

    try:
        result = llm.with_structured_output(RouteDecision).invoke(prompt)

        print("Supervisor decision:", result)

        return result.action

    except Exception as e:
        print("Supervisor error:", e)
        return "regular_chat"