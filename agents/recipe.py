from llm import llm

def recipe_agent(state):

    messages = state.get("messages", [])

    people = state.get("number_of_people")
    spice = state.get("spice_level")
    region = state.get("region_preference")
    preference = state.get("preference_type")

    prompt = f"""
You are Chef Kuldip.

Create a short Indian recipe.

Preferences:
People: {people}
Spice Level: {spice}
Region: {region}
Cuisine: {preference}

Rules:
- No story
- Maximum 6 ingredients
- Maximum 6 cooking steps
- Keep response under 150 words

Format:

Dish:
Ingredients:
Steps:
Chef Tip:
"""

    response = llm.invoke(
        messages + [{"role": "system", "content": prompt}]
    )

    recipe = response.content

    state["recipe"] = recipe

    messages.append({
        "role": "assistant",
        "content": recipe + "\n\nWould you like step-by-step cooking guidance?"
    })

    state["messages"] = messages
    state["stage"] = "step_mode"

    return state