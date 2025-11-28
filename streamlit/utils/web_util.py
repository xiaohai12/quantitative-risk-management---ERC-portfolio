import streamlit as st
import os
import base64


# Style
def apply_custom_css():
    """
    Applies the custom 'Fancy & Pure' aesthetic CSS to the Streamlit app.
    """

    st.markdown("""
        <style>
        /* Import nice font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Apply horizontal padding to the main content area */
        .block-container  {
            padding-left: 150px;  /* left empty space */
            padding-right: 150px; /* right empty space */
        }

        /* Hide Streamlit Header and Footer for cleaner look */
        #MainMenu {visibility: visible;}
        footer {visibility: visible;}
        header {visibility: visible;}

        /* Custom Top Navbar Style */
        div.block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Button Styling to look like Nav Links */
        .stButton > button {
            width: 100%;
            border: none;
            background-color: transparent;
            color: #000;
            font-weight: 600;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            color: #000;
            background-color: #FFCC99;
            border-bottom: 3px solid transparent;
        }
        .stButton > button:focus,.stButton > button:active {
            color: #000 !important;
            border-bottom: 3px solid #CC6600!important;

        }

        /* Dropdown Menu Styling */
        .dropdown {
            position: relative;
            display: inline-block;
            padding-bottom: 20px;
            width: 100%;
        }

        .dropdown-button {
            width: 100%;
            padding: 8px 16px;
            background-color: transparent;
            color: #000;
            font-weight: 500;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            transition: all 0.3s ease;
            
        }

        .dropdown-button:hover {
            background-color: #FFCC99;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #ffffff;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1000 ;
            border-radius: 5px;
            margin-top: 5px;
        }

        .dropdown-content a {
            color: #000;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .dropdown-content a:hover {
            background-color: #FFCC99;
            border-radius: 5px;
        }

        .dropdown:hover .dropdown-content {
            display: block;
        }

        .dropdown:hover .dropdown-button {
            background-color: #FFCC99;
            border-bottom: 3px solid #CC6600;
        }

        /* Metric Cards Styling */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Section headers */
        .section-header {
            font-size: 2rem;
            font-weight: 600;
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #1a2a6c;
            padding-left: 15px;
        }
        </style>
    """, unsafe_allow_html=True)


# Navigation bar
def render_navbar(IMG_DIR):
    amber_path = os.path.join(IMG_DIR, "amber.png")

    amber_base64 = image_to_base64(amber_path)

    st.markdown(""" <hr style="margin-top:15px; margin-bottom:15px;"> """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])

    with col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{amber_base64}" 
                     style="height:35px; margin-right:10px; margin-top:-11px;">
                <h3 style="margin:0;margin-top:-5px;font-size:28px;font-weight:700;letter-spacing:0.8px;font-family: 'Trajan Pro', 'Playfair Display', serif;"><b>AMBER QUANT</b></h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button("Home"):
            st.switch_page("home_page.py")

    with col3:
        if st.button("Portfolios"):
            st.switch_page("ERC_portfolio.py")

    with col4:
        if st.button("Methodology"):
            st.switch_page("methodology.py")

    with col5:
        # Dropdown "Help"
        st.markdown("""
            <div class="dropdown">
                <button class="dropdown-button">Help ▼</button>
                <div class="dropdown-content">
                    <a href="?page=risk_profile">Risk Profile</a>
                    <a href="?page=ai_chat">AI Chat</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Handle navigation via query params
        query_params = st.query_params
        if "page" in query_params:
            if query_params["page"] == "risk_profile":
                st.switch_page("risk_preference.py")
            elif query_params["page"] == "ai_chat":
                st.switch_page("LLM.py")

    with col6:
        # Dropdown "About Us"
        st.markdown("""
            <div class="dropdown">
                <button class="dropdown-button">About Us ▼</button>
                <div class="dropdown-content">
                    <a href="?page=team">Our Team</a>
                    <a href="?page=contact">Contact Us</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Handle navigation via query params
        query_params = st.query_params
        if "page" in query_params:
            if query_params["page"] == "team":
                st.switch_page("team.py")
            elif query_params["page"] == "contact":
                st.switch_page("Contact.py")

    st.markdown("""<hr style="margin-top:-2px; margin-bottom:15px;">""", unsafe_allow_html=True)


# Convert images
def image_to_base64(image_path: str) -> str:
    """Convert a local image file to a base64-encoded string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
