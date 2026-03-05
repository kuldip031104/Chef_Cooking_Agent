from llm import llm

def recipe_agent(state):

    messages = state.get("messages", [])

    people = state.get("number_of_people")
    spice = state.get("spice_level")
    region = state.get("region_preference")
    preference = state.get("preference_type")

    prompt = f"""
You are Chef Kuldip, a master Indian chef with 30 years of experience.

Create a recipe based on these preferences:

People: {people}
Spice Level: {spice}
Region: {region}
Cuisine Preference: {preference}

Include:
- cultural story
- ingredients
- cooking method
- chef tips
"""

    response = llm.invoke(prompt)

    recipe = response.content

    state["recipe"] = recipe

    messages.append({
        "role": "assistant",
        "content": recipe + "\n\nWould you like step-by-step cooking guidance?"
    })

    state["messages"] = messages

    # Move workflow forward
    state["stage"] = "step_mode"

    return state