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


MAX_HISTORY = 6

def supervisor_router(state):

    messages = state.get("messages", [])

    if not messages:
        return "greeting"

    user_input = messages[-1]["content"]
    stage = state.get("stage")

    # last few messages
    history = messages[-MAX_HISTORY:]

    chat_history = "\n".join(
        f"{m['role']}: {m['content']}" for m in history
    )

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

Conversation history:
{chat_history}

Current state:
{state_summary}

"""

    try:
        result = llm.with_structured_output(RouteDecision).invoke(prompt)
        print("Supervisor decision:", result)
        return result.action

    except Exception as e:
        print("Supervisor error:", e)
        return "regular_chat"