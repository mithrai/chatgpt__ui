import streamlit as st
import requests

# Page config
st.set_page_config(page_title="ChatGPT Clone", page_icon="💬", layout="wide")

# Custom CSS for layout + dark mode
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        max-width: 70%;
    }
    .user {
        background-color: #1A73E8;
        color: white;
        margin-left: auto;
    }
    .bot {
        background-color: #262730;
        color: white;
        margin-right: auto;
    }
    .chat-container {
        height: 65vh;
        overflow-y: auto;
        padding: 10px;
        display: flex;
        flex-direction: column-reverse;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 ChatGPT Clone")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input at the bottom
with st.form("chat_form", clear_on_submit=True):
    user_prompt = st.text_input("You:", placeholder="Ask me anything...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

# If user submitted a prompt
if submitted and user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Send to FastAPI backend
    try:
        res = requests.post("http://127.0.0.1:8000/generate", json={"prompt": user_prompt})
        bot_response = res.json().get("response", "Sorry, I couldn't generate a response.")
    except:
        bot_response = "⚠️ Backend not available. Start FastAPI server!"

    # Add bot response
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat history in reverse (latest at bottom)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in reversed(st.session_state.messages):
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(f'<div class="message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
