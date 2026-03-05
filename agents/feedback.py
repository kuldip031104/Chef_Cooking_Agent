def feedback_agent(state):

    messages = state.get("messages", [])
    user_input = messages[-1]["content"].strip()

    # Check if rating is valid
    if user_input.isdigit():

        rating = int(user_input)

        if 1 <= rating <= 5:

            state["rating"] = rating

            messages.append({
                "role": "assistant",
                "content": f"Thank you for the {rating}⭐ rating! I'm glad you cooked with me today. 👨‍🍳"
            })

            state["stage"] = "regular_chat"

            state["messages"] = messages
            return state

    # If invalid rating
    messages.append({
        "role": "assistant",
        "content": "Please rate the recipe from 1–5."
    })

    state["messages"] = messages
    state["stage"] = "collect_feedback"

    return state