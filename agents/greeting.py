from llm import llm

def greeting_agent(state):

    messages = state.get("messages", [])
    user_id = state.get("user_id")

    system_prompt = """
You are Chef Kuldip.

Greet the user in ONE short sentence.
Ask what dish they want to cook.

Maximum 15 words.
"""

    response = llm.invoke(
        [{"role": "system", "content": system_prompt}] + messages
    )

    msg = response.content

    messages.append({
        "role": "assistant",
        "content": msg
    })

    # Save message in PostgreSQL

    state["messages"] = messages

    # Move workflow forward
    state["stage"] = "collect_preferences"

    return state