import streamlit as st

# Define the pages
st.write("# This is a placeholder for ERC portfolio page")

st.title("📈 Set Your Risk Level")
st.markdown("Use the slider below to set your risk tolerance level.")
st.markdown("---")

# Initialize session state for risk_score if it doesn't exist
if 'risk_score' not in st.session_state:
    st.session_state.risk_score = 5  # Default value

# Horizontal slider for risk scale with a unique key
risk_score = st.slider(
    "Select your risk level (0 = Conservative, 10 = Aggressive):",
    min_value=0,
    max_value=10,
    value=st.session_state.risk_score,
    step=1,
    format="%d",
    help="Drag the slider to set your risk tolerance level",
    key="risk_slider"  # Add a unique key
)

# Update session state whenever the slider changes
if risk_score != st.session_state.risk_score:
    st.session_state.risk_score = risk_score

# Display the selected score with visual feedback
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Determine profile based on score
    if st.session_state.risk_score <= 3:
        color = "🟢"
        profile = "Conservative"
    elif st.session_state.risk_score <= 6:
        color = "🟡"
        profile = "Moderate"
    elif st.session_state.risk_score <= 8:
        color = "🟠"
        profile = "Growth-Oriented"
    else:
        color = "🔴"
        profile = "Aggressive"

    # Store profile in session state
    st.session_state.risk_profile = profile

    st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{color}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Score: {st.session_state.risk_score}/10</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{profile}</h3>", unsafe_allow_html=True)

# Visual progress bar
st.markdown("### Risk Tolerance Scale")
st.progress(st.session_state.risk_score / 10)

# Info about the selection
if st.session_state.risk_score <= 3:
    st.info("💼 **Conservative**: You prefer stability and capital preservation. Low-risk investments suit you best.")
elif st.session_state.risk_score <= 6:
    st.info(
        "⚖️ **Moderate**: You seek balance between risk and return. Diversified portfolios align with your preferences.")
elif st.session_state.risk_score <= 8:
    st.warning(
        "📊 **Growth-Oriented**: You're comfortable with volatility for higher returns. Stock-heavy portfolios fit your profile.")
else:
    st.error(
        "🚀 **Aggressive**: You have high risk tolerance and seek maximum returns. You accept potential short-term losses.")

