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

# Display previous chat messages
for msg in st.session_state.state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input
user_input = st.chat_input("Ask Chef something...")

if user_input:

    # Show user message instantly
    with st.chat_message("user"):
        st.write(user_input)

    # Save user message
    st.session_state.state["messages"].append({
        "role": "user",
        "content": user_input
    })

    try:
        # Run LangGraph
        updated_state = graph.invoke(st.session_state.state)

        # Update session state
        st.session_state.state = updated_state

    except Exception as e:
        st.error(f"Something went wrong: {e}")

    # Refresh UI
    st.rerun()