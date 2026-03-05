def recipe_agent(state):

    recipe_text = """
Ahh! Paneer Butter Masala — a jewel of North Indian kitchens.

Legend says the dish was born in Delhi when leftover tandoori gravy
met butter and cream.

Ingredients:
- 250g paneer
- 2 tomatoes
- 1 onion
- butter
- cream
- garam masala

Chef Tip:
If you want a deeper flavor, roast the spices first.

Would you like step-by-step cooking guidance?
"""

    state["recipe"] = recipe_text

    state["messages"].append({
        "role": "assistant",
        "content": recipe_text
    })

    return state