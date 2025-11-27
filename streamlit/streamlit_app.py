import streamlit as st
from streamlit import title

# Define the pages
home_page = st.Page("home_page.py", title="Home Page")

Contact_page = st.Page("Contact.py", title="Contact US")
Risk_Preference = st.Page("risk_preference.py", title="Risk Preference")
Our_Team = st.Page("team.py", title="Our Team")
Methodology = st.Page("methodology.py", title="Methodology")
LLM = st.Page("LLM.py", title="LLM")

# Set up navigation
pg = st.navigation([home_page, Risk_Preference, ERC_portfolio_page, Our_Team, Contact_page, Methodology, LLM])

# Run the selected page
pg.run()