def feedback_agent(state):

    state["messages"].append({
        "role": "assistant",
        "content": "Please rate the recipe from 1–5 and share any feedback."
    })

    # Update stage so supervisor doesn't loop
    state["stage"] = "end"

    return state