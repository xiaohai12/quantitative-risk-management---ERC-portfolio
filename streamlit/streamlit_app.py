import streamlit as st

# Define the pages
home_page = st.Page("home_page.py", title="Home Page", icon="🎈")
ERC_portfolio_page = st.Page("ERC_portfolio.py", title="ERC portfolio", icon="❄️")
Contact_page = st.Page("Contact.py", title="Contact US", icon="🎉")

# Set up navigation
pg = st.navigation([home_page, ERC_portfolio_page, Contact_page])

# Run the selected page
pg.run()