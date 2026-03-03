def feedback_agent(state):
    return {
        "messages": [{
            "role": "assistant",
            "content": "On a scale of 1–5, how was the recipe?"
        }]
    }