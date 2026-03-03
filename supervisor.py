from pydantic import BaseModel
from typing import Literal
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from Prompts.supervisor_prompt import SUPERVISOR_PROMPT
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

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

def supervisor(state):
    user_input = state["messages"][-1]["content"]

    result = llm.with_structured_output(RouteDecision).invoke(
        SUPERVISOR_PROMPT + f"\nUser: {user_input}"
    )

    return result.action