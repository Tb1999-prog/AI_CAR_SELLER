import streamlit as st
import requests

st.set_page_config(page_title="AI Car Assistant", layout="wide")
st.title("🚗 AI Car-Buying Assistant")

# Session state to keep chat history and session ID
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Sidebar info
with st.sidebar:
    st.subheader("🛠️ Session Tools")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.session_id = None
        st.rerun()

    st.markdown("---")
    st.markdown("**Session ID**: " + str(st.session_state.session_id or "Not started"))

# Display full chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input at bottom
user_query = st.chat_input("Ask me anything about cars...")

if user_query:
    # Show user message immediately
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Show "Thinking..." while waiting
    with st.spinner("🤖 Thinking..."):
        try:
            res = requests.post(
                f"http://localhost:8000/generate/1234",
                json={"query": user_query, "session_id": st.session_state.session_id}
            )
            if res.status_code == 200:
                data = res.json()
                ai_response = data["response"]
                st.session_state.session_id = data["session_id"]

                # Display assistant response and store it
                st.chat_message("assistant").markdown(ai_response)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            else:
                st.chat_message("assistant").markdown("❌ Failed to get a valid response.")
        except Exception as e:
            st.chat_message("assistant").markdown(f"❌ Error: {e}")
