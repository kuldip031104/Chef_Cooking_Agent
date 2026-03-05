def step_agent(state):

    steps = [
        "Heat butter in a pan.",
        "Add onions and sauté until golden.",
        "Add tomato puree and spices.",
        "Add paneer cubes and simmer.",
        "Finish with cream and garnish."
    ]

    step_index = state["current_step"]

    if step_index < len(steps):

        msg = f"Step {step_index + 1}: {steps[step_index]}"

        state["messages"].append({
            "role": "assistant",
            "content": msg
        })

        state["current_step"] += 1

    else:

        state["messages"].append({
            "role": "assistant",
            "content": "Wonderful cooking! How would you rate the recipe from 1–5?"
        })

    return state