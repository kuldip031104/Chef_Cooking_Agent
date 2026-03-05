from llm import llm

def step_agent(state):

    messages = state.get("messages", [])
    recipe = state.get("recipe")

    # Generate steps if not created yet
    if not state.get("steps"):

        prompt = f"""
You are Chef Kuldip.

Extract clear cooking steps from this recipe.

Recipe:
{recipe}

Rules:
- Return numbered steps
- Maximum 8 steps
- One short sentence per step
"""

        response = llm.invoke(prompt)

        steps = [
            s.strip() for s in response.content.split("\n")
            if s.strip() and s[0].isdigit()
        ]

        state["steps"] = steps
        state["current_step"] = 0


    steps = state["steps"]
    current_step = state.get("current_step", 0)


    if current_step < len(steps):

        msg = f"Step : {steps[current_step]}"

        messages.append({
            "role": "assistant",
            "content": msg
        })

        state["current_step"] = current_step + 1
        state["stage"] = "step_mode"

    else:

        messages.append({
            "role": "assistant",
            "content": "Wonderful cooking! 👨‍🍳 How would you rate the recipe from 1–5?"
        })

        state["stage"] = "collect_feedback"

    state["messages"] = messages

    return state