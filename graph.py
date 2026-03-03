from langgraph.graph import StateGraph
from state import ChefState
from supervisor import supervisor
from agents.greeting import greeting_agent
from agents.preferences import preference_agent
from agents.recipe import recipe_agent
from agents.step import step_agent
from agents.feedback import feedback_agent
from agents.regular_chat import regular_chat_agent
from agents.guardrail import guardrail_agent

builder = StateGraph(ChefState)

builder.add_node("greeting", greeting_agent)
builder.add_node("collect_preferences", preference_agent)
builder.add_node("generate_recipe", recipe_agent)
builder.add_node("step_mode", step_agent)
builder.add_node("collect_feedback", feedback_agent)
builder.add_node("regular_chat", regular_chat_agent)
builder.add_node("guardrail", guardrail_agent)

builder.add_conditional_edges(
    "__start__",
    supervisor,
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

graph = builder.compile()