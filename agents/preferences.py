def preference_agent(state):

    if not state["number_of_people"]:
        msg = "First tell me — how many people are we cooking for?"
    elif not state["spice_level"]:
        msg = "How spicy should the dish be? mild / medium / spicy"
    elif not state["region_preference"]:
        msg = "Which region do you prefer? north / south / east / west"
    elif not state["preference_type"]:
        msg = "Any dietary or cuisine preference?"
    else:
        msg = "Perfect! Let me craft a beautiful recipe for you."

    state["messages"].append({
        "role": "assistant",
        "content": msg
    })

    return state