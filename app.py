# app.py
# import streamlit as st
# import requests

# # 👉 Replace with your actual Groq API key
# GROQ_API_KEY = "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"

# # Streamlit app UI
# st.set_page_config(page_title="Free Chatbot with Groq", page_icon="🤖")
# st.title("🤖 GPT-Free Chatbot (Groq + Streamlit)")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# # Show chat history
# for msg in st.session_state.messages[1:]:  # skip system message
#     st.chat_message(msg["role"]).write(msg["content"])

# # User input
# prompt = st.chat_input("Type your message here...")

# if prompt:
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     # Show a spinner while thinking
#     with st.spinner("Thinking..."):
#         response = requests.post(
#             "https://api.groq.com/openai/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {GROQ_API_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "llama3-8b-8192",
#                 "messages": st.session_state.messages,
#                 "temperature": 0.7
#             }
#         )

#         if response.status_code == 200:
#             reply = response.json()["choices"][0]["message"]["content"]
#             st.session_state.messages.append({"role": "assistant", "content": reply})
#             st.chat_message("assistant").write(reply)
#         else:st.error(f"❌ Error from Groq API: {response.status_code} - {response.text}")



#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
import streamlit as st
import json
import os
from groq import Groq

# ---------------- Page Config ---------------- #
st.set_page_config(page_title="🤖 GPT-Free Chatbot", layout="centered")
st.title("🤖 GPT-Free Chatbot")

# -------------- Load/Save Chat History -------------- #
def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as file:
            return json.load(file)
    return []

def save_chat_history(messages):
    with open("chat_history.json", "w") as file:
        json.dump(messages, file, indent=2)

# ---------------- Session Setup ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# ---------------- Sidebar ---------------- #
with st.sidebar:
    st.header("🛠️ Settings")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        save_chat_history([])
        st.rerun()

# ---------------- Display Chat History ---------------- #
def format_message(role, content):
    if role == "user":
        return f"""
        <div style="background-color:#e0f7fa; padding: 10px; border-radius: 10px; margin-bottom:10px;">
            <b>👤 You:</b><br>{content}
        </div>
        """
    else:
        return f"""
        <div style="background-color:#f1f8e9; padding: 10px; border-radius: 10px; margin-bottom:10px;">
            <b>🤖 Assistant:</b><br>{content}
        </div>
        """

for msg in st.session_state.messages:
    st.markdown(format_message(msg["role"], msg["content"]), unsafe_allow_html=True)

# ---------------- Handle New User Input ---------------- #
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat_history(st.session_state.messages)

    try:
        # Setup Groq API
        client = Groq(api_key="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")

        # API call
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_chat_history(st.session_state.messages)

    except Exception as e:
        reply = f"❌ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_chat_history(st.session_state.messages)

    st.rerun()
