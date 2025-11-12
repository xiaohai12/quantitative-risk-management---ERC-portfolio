import streamlit as st
from transformers import pipeline

st.title("Risk Tolerance Chatbot 🤖")

# Initialize lightweight model once
@st.cache_resource
def get_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = get_model()

# Conversation memory
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Answer the questions below:")

if st.button("Send"):
    st.session_state.history.append(f"User: {user_input}")

    # Build prompt for risk scoring
    prompt = (
        "You are a financial advisor. Based on the user's answers, "
        "give a risk tolerance score from 0 (very low) to 10 (very high) "
        "and a short explanation.\n"
        "Conversation so far:\n" + "\n".join(st.session_state.history)
    )

    response = generator(prompt, max_length=100)[0]['generated_text']
    st.session_state.history.append(f"Bot: {response}")

# Display chat
for msg in st.session_state.history:
    st.write(msg)
