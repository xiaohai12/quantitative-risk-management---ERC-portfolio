import streamlit as st
from streamlit import title

# Define the pages
home_page = st.Page("home_page.py", title="Home Page", icon="🎈")
ERC_portfolio_page = st.Page("ERC_portfolio.py", title="ERC portfolio", icon="❄️")
Contact_page = st.Page("Contact.py", title="Contact US", icon="🎉")
Risk_Preference = st.Page("risk_preference.py", title="Risk Preference", icon="🎲")
Our_Team = st.Page("team.py", title="Our Team", icon= "🤝")
ERC_strategy_information = st.Page("Strategy_information.py", title="ERC Strategy Information", icon="📊")
LLM = st.Page("LLM.py", title="LLM", icon="🤖")

# Set up navigation
pg = st.navigation([home_page, ERC_portfolio_page, Risk_Preference, Our_Team, Contact_page, ERC_strategy_information, LLM])

# Run the selected page
pg.run()