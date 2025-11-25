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
    
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1,1])
    
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
        if st.button("Our Team"):
            st.switch_page("team.py")
    with col6:
        if st.button("Contact Us"):
            st.switch_page("Contact.py")
    
    st.markdown("""<hr style="margin-top:-2px; margin-bottom:15px;">""", unsafe_allow_html=True)

# Convert images
def image_to_base64(image_path: str) -> str:
    """Convert a local image file to a base64-encoded string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
