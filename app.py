import streamlit as st
from graph import graph

st.title("👨‍🍳 Chef Kuldip-Agent")

if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "user_id": "demo_user"
    }

user_input = st.chat_input("Ask Chef something...")

if user_input:
    st.session_state.state["messages"].append(
        {"role": "user", "content": user_input}
    )

    result = graph.invoke(st.session_state.state)

    for msg in result["messages"]:
        st.chat_message("assistant").write(msg["content"])