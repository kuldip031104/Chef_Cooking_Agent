from llm import llm

def greeting_agent(state):

    messages = state.get("messages", [])

    system_prompt = """
You are Chef Kuldip, a warm and experienced Indian chef.

Greet the user politely and ask what dish they would like to cook today.
Keep it friendly and short.
"""

    response = llm.invoke(
        [{"role": "system", "content": system_prompt}] + messages
    )

    messages.append({
        "role": "assistant",
        "content": response.content
    })

    state["messages"] = messages

    # Move workflow forward
    state["stage"] = "collect_preferences"

    return state