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

    # Normalize user input
    user_input = messages[-1]["content"].lower().strip()

    stage = state.get("stage")

    # Last few messages
    history = messages[-MAX_HISTORY:]

    chat_history = "\n".join(
        f"{m['role']}: {m['content']}" for m in history
    )

    # Clean structured state for LLM
    state_summary = f"""
stage: {stage}

preferences:
  number_of_people: {state.get("number_of_people")}
  spice_level: {state.get("spice_level")}
  region_preference: {state.get("region_preference")}
  preference_type: {state.get("preference_type")}
  allergies: {state.get("allergies")}

recipe_status:
  recipe_generated: {bool(state.get("recipe"))}
  steps_exist: {bool(state.get("steps"))}
  current_step: {state.get("current_step")}

feedback:
  rating: {state.get("rating")}
"""

    prompt = f"""
{SUPERVISOR_PROMPT}

### USER MESSAGE
{user_input}

### CONVERSATION HISTORY
{chat_history}

### CURRENT STATE
{state_summary}

Decide the next agent.
Return only JSON.
"""

    try:
        result = llm.with_structured_output(RouteDecision).invoke(prompt)

        
        print("User:", user_input)
        print("Stage:", stage)
        print("Decision:", result)
        

        return result.action

    except Exception as e:
        print("Supervisor error:", e)
        return "regular_chat"