from llm import llm
from tools.recipe_api import fetch_recipe


def recipe_agent(state):

    messages = state.get("messages", [])

    people = state.get("number_of_people")
    spice = state.get("spice_level")
    region = state.get("region_preference")
    preference = state.get("preference_type")

    # ---------- TOOL CALL ----------
    try:
        tool_result = fetch_recipe.invoke({"dish": preference or "Indian dish"})
        dish_name = tool_result.get("title", "Indian Recipe") if isinstance(tool_result, dict) else "Indian Recipe"
    except Exception:
        dish_name = "Indian Recipe"

    # ---------- LLM PROMPT ----------
    prompt = f"""
You are Chef Kuldip.

Create a short Indian recipe.

Dish: {dish_name}

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
1.
2.
3.
Chef Tip:
"""

    response = llm.invoke(
        messages + [{"role": "system", "content": prompt}]
    )

    recipe = response.content

    # ---------- EXTRACT STEPS ----------
    steps = []

    for line in recipe.split("\n"):
        line = line.strip()

        if line and line[0].isdigit():
            steps.append(line)

    state["recipe"] = recipe
    state["steps"] = steps
    state["current_step"] = 0

    # ---------- RESPONSE ----------
    messages.append({
        "role": "assistant",
        "content": recipe + "\n\nType **next** if you'd like step-by-step cooking guidance."
    })

    state["messages"] = messages
    state["stage"] = "step_mode"

    return state