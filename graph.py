from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from state import ChefState
from agents.greeting import greeting_agent
from agents.preferences import preference_agent
from agents.recipe import recipe_agent
from agents.step import step_agent
from agents.feedback import feedback_agent
from agents.regular_chat import regular_chat_agent
from agents.guardrail import guardrail_agent
from supervisor import supervisor_router

import psycopg_pool


builder = StateGraph(ChefState)

DB_URI = "postgresql://postgres:kuldip%40311@localhost:5432/chef_agent"

# connection pool
pool = psycopg_pool.ConnectionPool(DB_URI)

# LangGraph memory
memory = PostgresSaver(pool)


def supervisor_node(state):
    return state


builder.add_node("supervisor", supervisor_node)

builder.add_node("greeting", greeting_agent)
builder.add_node("collect_preferences", preference_agent)
builder.add_node("generate_recipe", recipe_agent)
builder.add_node("step_mode", step_agent)
builder.add_node("collect_feedback", feedback_agent)
builder.add_node("regular_chat", regular_chat_agent)
builder.add_node("guardrail", guardrail_agent)

builder.set_entry_point("supervisor")

builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "greeting": "greeting",
        "collect_preferences": "collect_preferences",
        "generate_recipe": "generate_recipe",
        "step_mode": "step_mode",
        "collect_feedback": "collect_feedback",
        "regular_chat": "regular_chat",
        "guardrail": "guardrail",
    }
)

builder.add_edge("greeting", END)
builder.add_edge("collect_preferences", END)
builder.add_edge("generate_recipe", END)
builder.add_edge("step_mode", END)
builder.add_edge("collect_feedback", END)
builder.add_edge("regular_chat", END)
builder.add_edge("guardrail", END)

graph = builder.compile(checkpointer=memory)