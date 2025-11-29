import streamlit as st
import utils.web_util as wu
from statics import IMG_DIR

st.set_page_config(page_title="Strategy Overview", layout="wide", initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()
# Nav bar
wu.render_navbar(IMG_DIR)

# Enhanced CSS for this page
st.markdown("""
    <style>
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 40px;
        border-radius: 15px;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-align: center;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        text-align: center;
        opacity: 0.95;
    }

    /* Section cards */
    .section-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 30px;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .section-title {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .section-icon {
        font-size: 2.5rem;
    }

    /* Data asset cards */
    .asset-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .asset-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        transition: transform 0.3s ease;
    }

    .asset-card:hover {
        transform: scale(1.05);
    }

    .asset-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }

    .asset-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .asset-description {
        color: #555;
        font-size: 0.95rem;
    }

    /* Feature boxes */
    .feature-box {
        background: linear-gradient(135deg, #FFCC99 0%, #FFE5B4 100%);
        padding: 20px 25px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #CC6600;
    }

    .feature-box strong {
        color: #CC6600;
    }

    /* CTA section */
    .cta-section {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        padding: 50px;
        border-radius: 15px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }

    .cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
    }

    .cta-button {
        display: inline-block;
        padding: 15px 40px;
        background: white;
        color: #FF6B6B;
        text-decoration: none;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📊 Equal Risk Contribution Strategy</h1>
        <p class="hero-subtitle">A sophisticated portfolio optimization approach that balances risk across assets, not capital</p>
    </div>
""", unsafe_allow_html=True)

# What is ERC Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title"><span class="section-icon">🎯</span> What Is Equal Risk Contribution?</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("""
    Equal Risk Contribution (ERC) is a portfolio optimization method where each asset 
    contributes equally to total portfolio risk. Instead of allocating by capital 
    (weights) or expected return, ERC allocates by **risk parity**.
    """)
with col2:
    st.info("💡 **Key Insight**: Risk parity means equal risk, not equal money!")

st.markdown("""
    <div class="feature-box">
        <strong>✓ Equal Marginal Risk:</strong> Each asset's risk contribution is balanced
    </div>
    <div class="feature-box">
        <strong>✓ Volatility Protection:</strong> Avoids concentration in high-volatility assets
    </div>
    <div class="feature-box">
        <strong>✓ Dynamic Adaptation:</strong> Naturally adjusts to changing market conditions
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Why ERC Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title"><span class="section-icon">⚡</span> Why We Use ERC</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 🛡️")
    st.markdown("**Risk-Based**")
    st.write("Diversification by risk, not capital")
with col2:
    st.markdown("### 📈")
    st.markdown("**Stable Returns**")
    st.write("Consistent performance in volatility")
with col3:
    st.markdown("### 🎲")
    st.markdown("**Tail-Risk**")
    st.write("Reduced exposure to extreme losses")
with col4:
    st.markdown("### 🔍")
    st.markdown("**Transparent**")
    st.write("Clear and intuitive methodology")

st.markdown("<br><br>", unsafe_allow_html=True)

# Data Description Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title"><span class="section-icon">📦</span> Multi-Asset Data Universe</h2>
    </div>
""", unsafe_allow_html=True)

st.write("Our ERC system leverages a comprehensive dataset from **Yahoo Finance** covering four major asset classes:")

# Asset Cards
st.markdown("""
    <div class="asset-grid">
        <div class="asset-card">
            <div class="asset-icon">📈</div>
            <div class="asset-title">Equities</div>
            <div class="asset-description">S&P 500, NASDAQ, sector ETFs, and individual stocks for growth exposure</div>
        </div>
        <div class="asset-card">
            <div class="asset-icon">🏆</div>
            <div class="asset-title">Commodities</div>
            <div class="asset-description">Gold, Oil, Natural Gas for inflation and supply-shock hedging</div>
        </div>
        <div class="asset-card">
            <div class="asset-icon">🏦</div>
            <div class="asset-title">Bonds</div>
            <div class="asset-description">Treasury ETFs and corporate bonds for defensive stability</div>
        </div>
        <div class="asset-card">
            <div class="asset-icon">₿</div>
            <div class="asset-title">Crypto</div>
            <div class="asset-description">BTC, ETH for high-volatility, high-growth potential</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Data collected
with st.expander("📊 View Detailed Data Collection"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📈 Price Data**")
        st.write("• Daily OHLC prices")
        st.write("• Adjusted Close")
        st.write("• Trading Volume")

    with col2:
        st.markdown("**📉 Risk Metrics**")
        st.write("• Percentage returns")
        st.write("• Volatility patterns")
        st.write("• Cross-asset correlations")

st.markdown("<br>", unsafe_allow_html=True)

# ESG Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title"><span class="section-icon">🌱</span> ESG Integration</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    st.write("""
    We extend the ERC framework to incorporate **Environmental, Social, and Governance** metrics, 
    allowing you to build portfolios that align with sustainability goals without sacrificing returns.
    """)

    st.markdown("**Key ESG Features:**")
    st.write("• Carbon intensity tracking per company")
    st.write("• MSCI/Sustainalytics ESG scores")
    st.write("• Sector-level sustainability constraints")
    st.write("• Portfolio carbon reduction targets (e.g., –30%)")

with col2:
    st.success("🌍 **Sustainable Investing**")
    st.write("Compare traditional vs ESG-optimized portfolios")
    st.metric("Carbon Reduction Target", "30%", delta="-30%")

# CTA Section
st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Ready to Build Your Portfolio?</h2>
        <p style="color: white; font-size: 1.1rem; margin-bottom: 30px;">
            Experience our interactive ERC optimization tool and create your personalized investment strategy
        </p>
        <a href="https://xiaohai12-quantitative-risk-manag-streamlitstreamlit-app-w9wlfm.streamlit.app/~/+/ERC_portfolio" 
           class="cta-button" target="_blank">
            🚀 Launch ERC Portfolio Builder
        </a>
    </div>
""", unsafe_allow_html=True)