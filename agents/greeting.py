def greeting_agent(state):

    state["messages"].append({
        "role": "assistant",
        "content": (
            "Namaste, my friend! I’m Chef Kuldip — "
            "30 years behind the stove, from the spice markets of Delhi "
            "to rustic kitchens of Tuscany.\n\n"
            "Tell me, what shall we cook today?"
        )
    })

    return state