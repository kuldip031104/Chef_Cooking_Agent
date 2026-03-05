from llm import llm

def step_agent(state):

    messages = state.get("messages", [])
    recipe = state.get("recipe")

    # If steps not generated yet → ask LLM to generate them
    if not state.get("steps"):

        prompt = f"""
You are Chef Kuldip.

From the following recipe, extract clear step-by-step cooking instructions.

Recipe:
{recipe}

Return the steps as a numbered list.
"""

        response = llm.invoke(prompt)

        steps_text = response.content.split("\n")

        # Clean steps
        steps = [s.strip() for s in steps_text if s.strip()]

        state["steps"] = steps
        state["current_step"] = 0

    steps = state["steps"]
    current_step = state.get("current_step", 0)

    if current_step < len(steps):

        msg = steps[current_step]

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