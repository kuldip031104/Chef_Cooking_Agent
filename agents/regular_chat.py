from llm import llm

def regular_chat_agent(state):

    messages = state.get("messages", [])

    user_input = messages[-1]["content"]

    prompt = f"""
You are Chef Kuldip, a friendly Indian chef.

Respond to the user's cooking-related question in a helpful and conversational way.

User question:
{user_input}
"""

    response = llm.invoke(prompt)

    messages.append({
        "role": "assistant",
        "content": response.content
    })

    state["messages"] = messages

    # After casual chat, return to preference collection
    state["stage"] = "collect_preferences"

    return state