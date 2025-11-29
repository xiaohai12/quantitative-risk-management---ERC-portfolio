import streamlit as st
import utils.web_util as wu
from statics import IMG_DIR

# Custom style
wu.apply_custom_css()

# Override the horizontal padding for this page only
st.markdown("""
    <style>
    .block-container {
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1200px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Nav bar
wu.render_navbar(IMG_DIR)

# ---- Hide the sidebar completely ----
hide_sidebar_style = """
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    .css-1d391kg {display: none;} /* older streamlit versions */
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)



# Page configuration
st.title("Risk Preference Assessment")
st.markdown("Answer the following questions to evaluate your risk tolerance profile.")
st.markdown("---")


# Initialize session state for storing answers
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Define questions with their options and scores
questions = [
    {
        "id": "q1",
        "question": "If you had $10,000 to invest, which option would you choose?",
        "type": "radio",
        "options": {
            "Keep it in a savings account with guaranteed 2% return": 0,
            "Invest in bonds with potential 4-5% return": 3,
            "Mix of stocks and bonds with potential 6-8% return": 6,
            "Aggressive stock portfolio with potential 10-15% return": 10
        }
    },
    {
        "id": "q2",
        "question": "How would you react if your investment lost 20% of its value in one month?",
        "type": "radio",
        "options": {
            "Sell immediately to prevent further losses": 0,
            "Sell some and keep some": 3,
            "Hold and wait for recovery": 7,
            "Buy more at the lower price": 10
        }
    },
    {
        "id": "q3",
        "question": "What is your investment time horizon?",
        "type": "radio",
        "options": {
            "Less than 1 year": 0,
            "1-3 years": 3,
            "3-7 years": 7,
            "More than 7 years": 10
        }
    },
    {
        "id": "q4",
        "question": "On a scale from 1-10, how comfortable are you with market volatility?",
        "type": "slider",
        "min": 1,
        "max": 10,
        "default": 5
    },
    {
        "id": "q5",
        "question": "Which statement best describes your financial situation?",
        "type": "radio",
        "options": {
            "I have no emergency fund and depend on every paycheck": 0,
            "I have some savings but limited financial cushion": 3,
            "I have a solid emergency fund (6+ months expenses)": 7,
            "I have substantial savings and multiple income sources": 10
        }
    },
    {
        "id": "q6",
        "question": "What percentage of your portfolio would you allocate to high-risk investments?",
        "type": "slider",
        "min": 0,
        "max": 100,
        "default": 20
    },
    {
        "id": "q7",
        "question": "You have a chance to invest in a startup. What do you do?",
        "type": "radio",
        "options": {
            "No way, too risky": 0,
            "Maybe invest a very small amount": 4,
            "Invest a moderate amount if I like the idea": 7,
            "I'd invest significantly if the opportunity looks good": 10
        }
    },
    {
        "id": "q8",
        "question": "How much investment experience do you have?",
        "type": "radio",
        "options": {
            "None, I'm just starting": 0,
            "Some experience with basic investments": 4,
            "Several years of active investing": 7,
            "Extensive experience across various asset classes": 10
        }
    }
]

# Display questions
for q in questions:
    st.markdown(f"### {q['question']}")

    if q['type'] == 'radio':
        answer = st.radio(
            "Select your answer:",
            options=list(q['options'].keys()),
            key=q['id'],
            label_visibility="collapsed"
        )
        st.session_state.answers[q['id']] = q['options'][answer]

    elif q['type'] == 'slider':
        if q['id'] == 'q6':
            answer = st.slider(
                "Slide to select percentage:",
                min_value=q['min'],
                max_value=q['max'],
                value=q['default'],
                key=q['id'],
                format="%d%%"
            )
            # Convert percentage to 0-10 scale
            st.session_state.answers[q['id']] = (answer / 10)
        else:
            answer = st.slider(
                "Slide to rate:",
                min_value=q['min'],
                max_value=q['max'],
                value=q['default'],
                key=q['id']
            )
            st.session_state.answers[q['id']] = answer

    st.markdown("---")

# Submit button
if st.button("Calculate My Risk Score", type="primary", use_container_width=True):
    st.session_state.submitted = True

# Calculate and display results
if st.session_state.submitted:
    # Calculate total score
    total_score = sum(st.session_state.answers.values())
    max_possible = 80  # Sum of all maximum scores

    # Normalize to 0-10 scale
    final_score = round((total_score / max_possible) * 10)

    # Store the final score in session state for access on other pages
    st.session_state.risk_score = final_score
    st.session_state.risk_profile = None  # Will be set below

    # Display results
    st.markdown("---")
    st.markdown("## 🎯 Your Risk Profile Results")

    # Score display with color
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if final_score <= 3:
            color = "🟢"
            profile = "Conservative"
            description = "You prefer stability and capital preservation over high returns. Low-risk investments like bonds and savings accounts suit you best."
        elif final_score <= 6:
            color = "🟡"
            profile = "Moderate"
            description = "You seek a balance between risk and return. A diversified portfolio with a mix of stocks and bonds aligns with your preferences."
        elif final_score <= 8:
            color = "🟠"
            profile = "Growth-Oriented"
            description = "You're comfortable with market volatility to pursue higher returns. A stock-heavy portfolio with some diversification fits your profile."
        else:
            color = "🔴"
            profile = "Aggressive"
            description = "You have high risk tolerance and seek maximum returns. You're comfortable with volatile investments and potential short-term losses."

        # Store profile in session state
        st.session_state.risk_profile = profile

        st.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{color}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>Score: {final_score}/10</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{profile} Investor</h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.info(f"**Profile Description:** {description}")

    # Progress bar visualization
    st.markdown("### Risk Tolerance Scale")
    st.progress(final_score / 10)

    # Breakdown
    with st.expander("📋 See Detailed Breakdown"):
        st.markdown("**Your Responses:**")
        for q in questions:
            st.write(f"- {q['question']}: **{st.session_state.answers[q['id']]:.1f}** points")
        st.write(f"\n**Total Raw Score:** {total_score:.1f}/{max_possible}")
        st.write(f"**Normalized Score:** {final_score}/10")

    # Reset button
    if st.button("🔄 Retake Assessment"):
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()