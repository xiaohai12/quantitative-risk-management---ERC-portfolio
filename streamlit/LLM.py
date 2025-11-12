import streamlit as st
from transformers import pipeline

st.title("Risk Tolerance Advisor 🤖")

# User inputs
age = st.slider("Your age", 18, 70, 30)
horizon = st.slider("Investment horizon (years)", 1, 30, 10)
savings = st.number_input("Total savings ($)", min_value=0, value=10000)

# Button to generate suggestion
if st.button("Suggest Risk Tolerance"):
    # Build prompt for the model
    prompt = (
        f"My age is {age}, investment horizon is {horizon} years, "
        f"and I have ${savings} in savings. Suggest an appropriate risk tolerance "
        f"(Conservative, Moderate, or Aggressive) with a short explanation."
    )

    # Load a lightweight instruction-following model from Hugging Face
    generator = pipeline(
        "text-generation",
        model="tiiuae/falcon-7b-instruct",  # lightweight instruct model
        device=-1  # CPU; use device=0 for GPU
    )

    # Generate suggestion
    suggestion = generator(prompt, max_length=150, do_sample=True, temperature=0.7)
    st.write(suggestion[0]['generated_text'])
