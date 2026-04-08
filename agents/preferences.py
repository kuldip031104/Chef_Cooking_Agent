def preference_agent(state):

    print("---- PREFERENCE AGENT START ----")
    print("STATE BEFORE:", state)

    messages = state.get("messages", [])
    user_input = messages[-1]["content"].lower().strip()
    question = state.get("current_preference_question")

    import re

    # ✅ NEW: If preferences already exist, skip questions
    if all([
        state.get("number_of_people"),
        state.get("spice_level"),
        state.get("region_preference"),
        state.get("preference_type"),
        state.get("allergies")
    ]):

        messages.append({
            "role": "assistant",
            "content": "Your preferences are already set. Generating your recipe now..."
        })

        state["stage"] = "generate_recipe"
        state["current_preference_question"] = None
        state["messages"] = messages

        print("STATE AFTER:", state)
        print("---- PREFERENCE AGENT END ----")

        return state


    # 1️⃣ Number of people
    if not state.get("number_of_people"):

        if question == "people":

            match = re.search(r"\d+", user_input)

            if match:
                state["number_of_people"] = int(match.group())
                state["current_preference_question"] = None
            else:
                messages.append({
                    "role": "assistant",
                    "content": "Please tell me the number of people (example: 2 or 4)."
                })
                state["messages"] = messages
                return state

        else:
            messages.append({
                "role": "assistant",
                "content": "How many people are we cooking for?"
            })
            state["current_preference_question"] = "people"
            state["stage"] = "collect_preferences"
            state["messages"] = messages
            return state


    # 2️⃣ Spice level
    if not state.get("spice_level"):

        if question == "spice":

            if "mild" in user_input:
                state["spice_level"] = "mild"

            elif "medium" in user_input:
                state["spice_level"] = "medium"

            elif "spicy" in user_input:
                state["spice_level"] = "spicy"

            else:
                messages.append({
                    "role": "assistant",
                    "content": "Please choose mild, medium, or spicy."
                })
                state["messages"] = messages
                return state

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

        if question == "region":

            regions = ["north", "south", "east", "west"]

            for r in regions:
                if r in user_input:
                    state["region_preference"] = r
                    break

            if not state.get("region_preference"):
                messages.append({
                    "role": "assistant",
                    "content": "Choose a region: north, south, east, or west."
                })
                state["messages"] = messages
                return state

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

            if "veg" in user_input:
                state["preference_type"] = "veg"

            elif "non" in user_input:
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

            if "none" in user_input or "no" in user_input:
                state["allergies"] = "none"
            else:
                state["allergies"] = user_input

            messages.append({
                "role": "assistant",
                "content": "Perfect! Generating your recipe now..."
            })

            state["current_preference_question"] = None
            state["stage"] = "generate_recipe"
            state["messages"] = messages

            print("STATE AFTER:", state)
            print("---- PREFERENCE AGENT END ----")

            return state

        else:
            messages.append({
                "role": "assistant",
                "content": "Do you have any food allergies? (type 'none' if not)"
            })
            state["current_preference_question"] = "allergy"
            state["messages"] = messages
            return state


    print("STATE AFTER:", state)
    print("---- PREFERENCE AGENT END ----")

    return state