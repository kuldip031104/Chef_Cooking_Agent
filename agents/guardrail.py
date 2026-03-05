def guardrail_agent(state):

    messages = state.get("messages", [])

    messages.append({
        "role": "assistant",
        "content": "My friend, I can only help with cooking and cuisine topics. 🍳 What would you like to cook today?"
    })

    state["messages"] = messages

    # Reset conversation flow
    state["stage"] = "greeting"

    return state