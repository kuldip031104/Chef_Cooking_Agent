def guardrail_agent(state):

    state["messages"].append({
        "role": "assistant",
        "content": (
            "My friend, I can only help with cooking and cuisine topics."
        )
    })

    return state