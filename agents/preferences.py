def preference_agent(state):

    messages = state.get("messages", [])
    user_input = messages[-1]["content"].lower()

    # 1️⃣ Number of people
    if not state.get("number_of_people"):
        if user_input.isdigit():
            state["number_of_people"] = int(user_input)
        else:
            messages.append({
                "role": "assistant",
                "content": "How many people are we cooking for?"
            })
            state["messages"] = messages
            return state

    # 2️⃣ Spice level
    if not state.get("spice_level"):
        if user_input in ["mild", "medium", "spicy"]:
            state["spice_level"] = user_input
        else:
            messages.append({
                "role": "assistant",
                "content": "How spicy should it be? (mild / medium / spicy)"
            })
            state["messages"] = messages
            return state

    # 3️⃣ Region preference
    if not state.get("region_preference"):
        if user_input in ["north", "south", "east", "west"]:
            state["region_preference"] = user_input
        else:
            messages.append({
                "role": "assistant",
                "content": "Which region cuisine do you prefer? (north / south / east / west)"
            })
            state["messages"] = messages
            return state

    # 4️⃣ Veg / Non-veg
    if not state.get("preference_type"):
        if user_input in ["veg", "vegetarian", "non veg", "non-veg"]:
            state["preference_type"] = user_input
        else:
            messages.append({
                "role": "assistant",
                "content": "Do you prefer veg or non-veg?"
            })
            state["messages"] = messages
            return state

    # 5️⃣ Allergies
    if not state.get("allergies"):
        state["allergies"] = user_input

        messages.append({
            "role": "assistant",
            "content": "Great! Let me prepare the perfect recipe for you."
        })

        state["stage"] = "generate_recipe"

    state["messages"] = messages
    return state