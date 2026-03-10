def preference_agent(state):

    messages = state.get("messages", [])
    user_input = messages[-1]["content"].lower().strip()

    question = state.get("current_preference_question")

    import re

# 1️⃣ Ask number of people
    if not state.get("number_of_people"):

        match = re.search(r"\d+", user_input)

        if question == "people" and match:
            state["number_of_people"] = int(match.group())
            state["current_preference_question"] = None

        else:
            messages.append({
                "role": "assistant",
                "content": "How many people are we cooking for?"
            })
            state["current_preference_question"] = "people"
            state["messages"] = messages
            return state

    # 2️⃣ Spice level
    if not state.get("spice_level"):

        if question == "spice" and user_input in ["mild", "medium", "spicy"]:
            state["spice_level"] = user_input
            state["current_preference_question"] = None

        else:
            messages.append({
                "role": "assistant",
                "content": "How spicy should it be? (mild / medium / spicy)"
            })
            state["current_preference_question"] = "spice"
            state["messages"] = messages
            return state

    # 3️⃣ Region
    if not state.get("region_preference"):

        if question == "region" and user_input in ["north", "south", "east", "west"]:
            state["region_preference"] = user_input
            state["current_preference_question"] = None

        else:
            messages.append({
                "role": "assistant",
                "content": "Which region cuisine do you prefer? (north / south / east / west)"
            })
            state["current_preference_question"] = "region"
            state["messages"] = messages
            return state

    # 4️⃣ Veg / Non-veg
    if not state.get("preference_type"):

        if question == "type":

            if user_input in ["veg", "vegetarian"]:
                state["preference_type"] = "veg"

            elif user_input in ["non veg", "non-veg"]:
                state["preference_type"] = "non-veg"

            else:
                messages.append({
                    "role": "assistant",
                    "content": "Please answer veg or non-veg."
                })
                state["messages"] = messages
                return state

            state["current_preference_question"] = None

        else:
            messages.append({
                "role": "assistant",
                "content": "Do you prefer veg or non-veg?"
            })
            state["current_preference_question"] = "type"
            state["messages"] = messages
            return state

    # 5️⃣ Allergies
    if not state.get("allergies"):

        if question == "allergy":

            if user_input in ["none", "no", "no allergies"]:
                state["allergies"] = "none"
            else:
                state["allergies"] = user_input

            messages.append({
                "role": "assistant",
                "content": "Perfect! Let me prepare the best recipe for you."
            })

            state["stage"] = "generate_recipe"
            state["messages"] = messages
            return state

        else:
            messages.append({
                "role": "assistant",
                "content": "Do you have any food allergies? (type 'none' if not)"
            })

            state["current_preference_question"] = "allergy"
            state["messages"] = messages
            return state

    return state