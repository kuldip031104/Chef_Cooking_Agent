def preference_agent(state):

    messages = state.get("messages", [])
    user_input = messages[-1]["content"].lower()

    # Extract number of people
    if not state.get("number_of_people"):

        if user_input.isdigit():
            state["number_of_people"] = int(user_input)
        else:
            messages.append({
                "role": "assistant",
                "content": "First tell me — how many people are we cooking for?"
            })
            state["messages"] = messages
            return state

    # Ask spice level
    if not state.get("spice_level"):

        if user_input in ["mild", "medium", "spicy"]:
            state["spice_level"] = user_input
        else:
            messages.append({
                "role": "assistant",
                "content": "How spicy should the dish be? mild / medium / spicy"
            })
            state["messages"] = messages
            return state

    # Ask region
    if not state.get("region_preference"):

        if user_input in ["north", "south", "east", "west"]:
            state["region_preference"] = user_input
        else:
            messages.append({
                "role": "assistant",
                "content": "Which region do you prefer? north / south / east / west"
            })
            state["messages"] = messages
            return state

    # Ask cuisine preference
    if not state.get("preference_type"):

        state["preference_type"] = user_input
        messages.append({
            "role": "assistant",
            "content": "Perfect! Let me craft a beautiful recipe for you."
        })

        state["stage"] = "generate_recipe"

    state["messages"] = messages

    return state