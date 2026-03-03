def guardrail_agent(state):
    return {
        "messages": [{
            "role": "assistant",
            "content": "I can help with cooking only."
        }]
    }