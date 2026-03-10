def step_agent(state):

    messages = state.get("messages", [])
    steps = state.get("steps", [])
    current_step = state.get("current_step", 0)

    # Safety check
    if not steps:
        messages.append({
            "role": "assistant",
            "content": "I couldn't find the cooking steps. Let me regenerate the recipe."
        })

        state["stage"] = "generate_recipe"
        state["messages"] = messages
        return state


    # Show next step
    if current_step < len(steps):

        step_text = steps[current_step]

        messages.append({
            "role": "assistant",
            "content": f"👨‍🍳 {step_text}\n\nType **next** when you're ready for the next step."
        })

        state["current_step"] = current_step + 1
        state["stage"] = "step_mode"


    # Cooking finished
    else:

        messages.append({
            "role": "assistant",
            "content": "🎉 Wonderful cooking! 👨‍🍳\n\nHow would you rate the recipe from **1–5**?"
        })

        state["stage"] = "collect_feedback"


    state["messages"] = messages

    return state