import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="NBA Chatbot", page_icon="🏀")
st.title("🏀 NBA Chatbot (Powered by Gemini)")
st.markdown("Ask anything about NBA teams. This assistant remembers your conversation and responds like an NBA analyst.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something about NBA teams...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        prompt = "You are a helpful and knowledgeable NBA analyst.\n"
        for msg in st.session_state.messages:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        prompt += "Assistant:"

        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)
        reply = response.text.strip()

    except Exception as e:
        reply = f"⚠️ Sorry, something went wrong with Gemini: {e}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
