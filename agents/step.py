def step_agent(state):

    step_index = state.get("current_step", 0)
    steps = state["steps"]

    if step_index >= len(steps):
        return {
            "messages": [{
                "role": "assistant",
                "content": "We are done! Shall I take your feedback?"
            }]
        }

    return {
        "current_step": step_index + 1,
        "messages": [{
            "role": "assistant",
            "content": f"Step {step_index+1}: {steps[step_index]}"
        }]
    }