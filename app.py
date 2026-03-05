import streamlit as st
from graph import graph

st.set_page_config(page_title="Chef Kuldip Agent", page_icon="👨‍🍳")

st.title("👨‍🍳 Chef Kuldip-Agent")

# Initialize state
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "user_id": "demo_user",

        "number_of_people": None,
        "spice_level": None,
        "region_preference": None,
        "preference_type": None,
        "allergies": None,

        "recipe": None,
        "steps": None,
        "current_step": 0,

        "rating": None
    }

# Display chat history
for msg in st.session_state.state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Ask Chef something...")

if user_input:

    print("User input received:", user_input)

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.state["messages"].append({
        "role": "user",
        "content": user_input
    })

    try:
        print("Invoking LangGraph...")
        updated_state = graph.invoke(st.session_state.state)
        print("Graph finished:", updated_state)

        st.session_state.state = updated_state

    except Exception as e:
        print("ERROR:", e)
        st.error(f"Something went wrong: {e}")

    st.rerun()