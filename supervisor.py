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

    # conversation start
    if not state.get("messages"):
        return "greeting"

    user_input = state["messages"][-1]["content"]
    text = user_input.lower()
    stage = state.get("stage")

    # ---------- HARD INTERRUPTS ----------

    if "restart" in text or "new recipe" in text:
        state["stage"] = "collect_preferences"
        return "collect_preferences"

    if "next" in text or "continue" in text:
        return "step_mode"

    # ---------- STATE SUMMARY ----------

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

You are the supervisor of a multi-agent cooking assistant.

Available agents:

greeting → greet the user
collect_preferences → gather dish, people, spice level
generate_recipe → create full recipe
step_mode → guide cooking step-by-step
collect_feedback → ask for rating
regular_chat → casual conversation
guardrail → unsafe or irrelevant requests

Current state:
{state_summary}

User message:
{user_input}

Decide the best agent.
Return action only from the list.
"""

    try:

        result = llm.with_structured_output(RouteDecision).invoke(prompt)

        print("Supervisor decision:", result)

        return result.action

    except Exception as e:

        print("Supervisor error:", e)

        return "regular_chat"