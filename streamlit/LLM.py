import streamlit as st
import requests
import utils.web_util as wu
from statics import IMG_DIR
# Define the pages

# Page configuration
st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="wide"
)

# ---- Hide the sidebar completely ----
hide_sidebar_style = """
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    .css-1d391kg {display: none;} /* older streamlit versions */
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Custom style
wu.apply_custom_css()

# Override the horizontal padding for this page only
st.markdown("""
    <style>
    /* Hero section for title */
    .hero-assessment {
        background: linear-gradient(135deg, #CC6600 0%, #FF8C42 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
     </style>
""", unsafe_allow_html=True)

# Nav bar
wu.render_navbar(IMG_DIR)

# Hero section
st.markdown("""
    <div class="hero-assessment">
        <h1>💬 Amber AI Chat Assistant</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .stChatInputContainer {
        padding: 1rem;
    }
    div[data-testid="stChatMessageContent"] {
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Get API key from Streamlit secrets
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ OpenRouter API key not found.")
    st.stop()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting message
    st.session_state.messages.append({
        "role": "assistant",
        "content": """Hi! I’m Amber from Amber Quant 👋 
How can I help you explore your options today?  
*Note: This is educational only. Please always consult a financial advisor (we would be happy to meet you!) or do your own research, before investing.*"""
    })

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value = """You are Amber, a concise educational assistant from Amber Quant.
Available investments:
• Stocks (ESG-compliant option available)
• Commodities (ESG-compliant option available)
• Bonds (standard only, NO ESG version)
• Cryptocurrencies (standard only, NO ESG version)

Rules (strict):
- Keep every reply very short (2–4 sentences max).
- Only mention ESG for Stocks and Commodities. Never say or imply ESG exists for Bonds or Crypto.
- Never recommend specific products, amounts, or timing.
- NEVER give personalized advice.
- EVERY single reply MUST include this exact sentence (or very close variation):
  “
  *Note: This is educational only. Please always consult a financial advisor (we would be happy to meet you!) or do your own research before investing.*”

Example of correct reply:
“Conservative investors often look at bonds or ESG commodities. ESG options are only available for stocks and commodities. 
*Note: This is educational only. Please always consult a financial advisor (we would be happy to meet you!) or do your own research before investing.*”""",
        height=150,
        help="Instructions for how the AI should behave"
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.6,
        step=0.1,
        help="Controls randomness in responses"
    )

    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=1000,
        value=500,
        step=100,
        help="Maximum length of the response"
    )

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # Format messages for the API
            api_messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Add conversation history (skip the initial greeting for API)
            for msg in st.session_state.messages:
                # Skip the initial assistant greeting from being sent to API
                if msg == st.session_state.messages[0] and msg["role"] == "assistant":
                    continue
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            data = {
                "model": "deepseek/deepseek-chat",
                "messages": api_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Show loading spinner
            with st.spinner("Thinking..."):
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )

            if response.status_code == 200:
                result = response.json()
                assistant_message = result["choices"][0]["message"]["content"]

                # Display the response
                message_placeholder.markdown(assistant_message)

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                message_placeholder.error(error_msg)

        except requests.exceptions.Timeout:
            message_placeholder.error("⏱️ Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            message_placeholder.error(f"❌ Request failed: {str(e)}")
        except Exception as e:
            message_placeholder.error(f"❌ An error occurred: {str(e)}")

# Footer
st.divider()
st.caption("Powered by DeepSeek")