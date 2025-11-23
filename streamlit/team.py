import streamlit as st
import utils.web_util as wu
from statics import IMG_DIR

st.set_page_config(page_title="Our Team", layout="wide",initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()
# Nav bar
wu.render_navbar(IMG_DIR)

# Page Header
st.title("🤝Our Team")
st.markdown("### Meet the Portfolio Management Team")
st.markdown("---")

# Team Introduction
st.markdown("""
We are a team of five dedicated finance students specializing in portfolio management and investment strategies. 
This project represents our collaborative effort to apply theoretical knowledge to practical portfolio optimization, 
combining quantitative analysis with risk management principles.
""")

st.markdown("---")

# Team Members Data
team_members = [
    {
    "name": "Yann Suttor",
    "role": "Asset Management Specialist",
    "bio": "Expert in optimizing investment portfolios and managing financial assets to maximize returns and mitigate risk. Provides strategic analysis for diverse asset classes.",
    "expertise": ["Asset Management", "Portfolio Optimization", "Strategic Financial Analysis"],
    "email": "yann.suttor@unil.ch"
    },
    {
        "name": "Marcus Rodriguez",
        "role": "Quantitative Analyst",
        "bio": "Expert in quantitative modeling and statistical analysis. Develops algorithms for portfolio optimization and performance measurement.",
        "expertise": ["Quantitative Modeling", "Statistical Analysis", "Python Programming"],
        "email": "marcus.rodriguez@university.edu"
    },
    {
        "name": "Shengzhao Lei",
        "role": "Quantitative strategist",
        "bio": "Focuses on developing and implementing quantitative strategies for portfolio optimization. Skilled in data analysis and financial modeling.",
        "expertise": ["Quantitative Strategies", "Data Analysis", "Financial Modeling"],
        "email": "shengzhao.lei@unil.ch"
    },
    {
        "name": "James Thompson",
        "role": "Market Research Analyst",
        "bio": "Conducts comprehensive market research and economic analysis. Provides insights on market trends and investment opportunities.",
        "expertise": ["Market Analysis", "Economic Research", "Sector Analysis"],
        "email": "james.thompson@university.edu"
    },
    {
        "name": "Priya Patel",
        "role": "Data Visualization & Reporting",
        "bio": "Creates intuitive dashboards and comprehensive reports. Transforms complex financial data into actionable insights through visualization.",
        "expertise": ["Data Visualization", "Dashboard Design", "Financial Reporting"],
        "email": "priya.patel@university.edu"
    }
]

# Display Team Members
for i, member in enumerate(team_members):
    # Create two columns for layout
    col1, col2 = st.columns([1, 3])

    with col1:
        # Placeholder for profile image (using emoji as placeholder)
        st.markdown(f"<div style='text-align: center; font-size: 80px;'>👤</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"### {member['name']}")
        st.markdown(f"**{member['role']}**")
        st.markdown(f"{member['bio']}")

        # Display expertise tags
        expertise_tags = " • ".join([f"`{skill}`" for skill in member['expertise']])
        st.markdown(f"**Expertise:** {expertise_tags}")

        st.markdown(f"📧 {member['email']}")

    # Add separator between team members
    if i < len(team_members) - 1:
        st.markdown("---")

# Project Information Section
st.markdown("---")
st.markdown("## About This Project")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Project Scope:**
    - Portfolio optimization strategies
    - Risk-return analysis
    - Asset allocation modeling
    - Performance measurement
    """)

with col2:
    st.markdown("""
    **Tools & Technologies:**
    - Python & Streamlit
    - Financial modeling libraries
    - Statistical analysis tools
    - Data visualization frameworks
    """)

# Contact Section
st.markdown("---")
st.markdown("## Get In Touch")
st.info(
    "For inquiries about our project or methodologies, please contact any team member via email. We welcome feedback and discussions about portfolio management strategies.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px;'>
    <p>Portfolio Management Academic Project | University Name | 2024-2025</p>
</div>
""", unsafe_allow_html=True)
