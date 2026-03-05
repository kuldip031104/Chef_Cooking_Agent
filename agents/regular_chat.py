def regular_chat_agent(state):

    state["messages"].append({
        "role": "assistant",
        "content": (
            "Ah, great question! In my kitchen I always recommend "
            "freshly ground spices — they make all the difference."
        )
    })

    return state