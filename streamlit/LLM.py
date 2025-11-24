import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for ChatGPT-like styling
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
    st.error("⚠️ OpenRouter API key not found. Please configure it in `.streamlit/secrets.toml`")
    st.info("""
    **Setup Instructions:**

    1. Create a `.streamlit` folder in your project root
    2. Create a `secrets.toml` file inside it
    3. Add your API key:
    ```
    OPENROUTER_API_KEY = "your-api-key-here"
    ```
    4. Add `.streamlit/secrets.toml` to your `.gitignore`
    """)
    st.stop()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm here to provide general information about financial topics and markets. Please note that I provide educational information only, not personalized financial advice. Always consult with qualified financial advisors before making investment decisions. How can I assist you today?"
    })

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")

    model = st.selectbox(
        "Model",
        ["deepseek/deepseek-chat", "deepseek/deepseek-reasoner"],
        help="Select the DeepSeek model to use"
    )

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful financial information assistant. You provide general information about financial topics and markets. Always remind users that you provide educational information only, not personalized financial advice, and that they should consult with qualified financial advisors before making investment decisions.",
        height=150,
        help="Instructions for how the AI should behave"
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness in responses"
    )

    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
        help="Maximum length of the response"
    )

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("💬 AI Chat Assistant")

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
                "model": model,
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