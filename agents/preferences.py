def preference_agent(state):
    return {
        "messages": [{
            "role": "assistant",
            "content": "Tell me:\n- Number of people\n- Spice level\n- Region preference (north/south/east/west)\n- Any dietary preference?"
        }]
    }