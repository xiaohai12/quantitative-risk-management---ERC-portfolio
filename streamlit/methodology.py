import streamlit as st
import utils.web_util as wu
from statics import IMG_DIR

st.set_page_config(page_title="Strategy Overview", page_icon="🔶", layout="wide", initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()
# Nav bar
wu.render_navbar(IMG_DIR)

# Enhanced CSS for this page
st.markdown("""
    <style>
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #CC6600 0%, #FF8C42 100%);
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
        border-left: 5px solid #CC6600;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .section-title {
        color: #CC6600;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 15px;
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
        background: linear-gradient(135deg, #FFE5B4 0%, #FFCC99 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        transition: transform 0.3s ease;
        border: 2px solid #CC6600;
    }

    .asset-card:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(204, 102, 0, 0.3);
    }

    .asset-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }

    .asset-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #CC6600;
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

    /* Benefits section */
    .benefit-card {
        text-align: center;
        padding: 20px;
    }

    .benefit-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }

    .benefit-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #CC6600;
        margin-bottom: 10px;
    }

    /* CTA section */
    .cta-section {
        background: linear-gradient(135deg, #CC6600 0%, #FFCC99 100%);
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
        color: #CC6600;
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
        <h1 class="hero-title">ERC-Optimized Multi-Asset Strategy</h1>
        <p class="hero-subtitle">A two-stage approach that first constructs equal risk contribution portfolios 
        within each asset class, then optimally combines these risk-balanced building blocks through mean-variance optimization tailored to specific risk tolerance levels</p>
    </div>
""", unsafe_allow_html=True)

# What is ERC Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title">What Is Equal Risk Contribution?</h2>
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
        <strong>Equal Risk Contribution:</strong> Each asset contributes equally to the portfolio’s total risk.
    </div>
    <div class="feature-box">
        <strong>Volatility Protection:</strong> Avoids concentration in high-volatility assets
    </div>
    <div class="feature-box">
        <strong>Dynamic Adaptation:</strong> Naturally adjusts to changing market conditions
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Why ERC Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title">Why We Use ERC</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="benefit-card"><div class="benefit-icon">🛡️</div><div class="benefit-title">Risk-Based</div><p>Diversification by risk, not capital</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="benefit-card"><div class="benefit-icon">📈</div><div class="benefit-title">Stable Returns</div><p>Consistent performance in volatility</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="benefit-card"><div class="benefit-icon">🎲</div><div class="benefit-title">Tail-Risk</div><p>Reduced exposure to extreme losses</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="benefit-card"><div class="benefit-icon">🔍</div><div class="benefit-title">Transparent</div><p>Clear and intuitive methodology</p></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Data Description Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title">Multi-Asset Data Universe</h2>
    </div>
""", unsafe_allow_html=True)

st.write("Our ERC system leverages a comprehensive dataset from **Yahoo Finance** covering four major asset classes:")

# Asset Cards
st.markdown("""
    <div class="asset-grid">
        <div class="asset-card">
            <div class="asset-icon">📈</div>
            <div class="asset-title">Equities</div>
            <div class="asset-description">US large-cap equities via S&P 500 for core portfolio growth</div>
        </div>
        <div class="asset-card">
            <div class="asset-icon">🏆</div>
            <div class="asset-title">Commodities</div>
            <div class="asset-description">Gold, Oil, Soybeans... for inflation and supply-shock hedging</div>
        </div>
        <div class="asset-card">
            <div class="asset-icon">🏦</div>
            <div class="asset-title">Bonds</div>
            <div class="asset-description">US Aggregate Bond Index for diversified fixed income and portfolio stability</div>
        </div>
        <div class="asset-card">
            <div class="asset-icon">₿</div>
            <div class="asset-title">Crypto</div>
            <div class="asset-description">BTC, ETH... for high-volatility, high-growth potential</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Data collected
with st.expander("View Detailed Data Collection"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Price Data**")
        st.write("• Daily OHLC prices")
        st.write("• Adjusted Close")
        st.write("• Trading Volume")

    with col2:
        st.markdown("**Risk Metrics**")
        st.write("• Percentage returns")
        st.write("• Volatility patterns")
        st.write("• Cross-asset correlations")

st.markdown("<br>", unsafe_allow_html=True)

# ESG Section
st.markdown("""
    <div class="section-card">
        <h2 class="section-title">ESG Integration</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    st.write("""
    We derive the investable universe from the constituents of multiple certified green funds. We take the intersection of the
    selected green funds' constituent lists and exclude any firm that is not present
    in all of them. This enforces a conservative green-screen: only firms consistently
    included across the chosen green funds remain investable.
    """)

    st.markdown("**Key features:**")
    st.write("• Source constituents from several certified green funds or ETFs.")
    st.write("• Compute the intersection of constituents — firms absent from any selected fund are excluded.")
    st.write("• Sector‑aware replacement logic ensures coverage if exclusions create gaps.")
    st.write("• Transparent reporting: list of excluded firms and percentage of the universe removed.")
with col2:
    st.success("♻️ Green‑Fund Filter")
    st.write("Exclude firms not present in all selected green funds")
    st.metric("Filter Method", "Intersection of selected funds")
st.markdown("<br>", unsafe_allow_html=True)

# --- Portfolio construction explanation (multi-asset, risk-aversion, MVO) ---
st.markdown("""
    <div class="section-card">
        <h2 class="section-title">How We Construct Multi‑Asset Portfolios</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.write("""
    We combine bonds, commodities, equities and crypto into a single, transparent
    mean–variance optimization (MVO) framework. The process is driven by a client‑specific
    risk level score which controls the trade‑off between expected return and portfolio risk.
    """)
    st.write("Key ideas:")
    st.write("• Inputs: expected returns per asset class and a covariance matrix capturing volatilities and correlations.")
    st.write("• Risk level score (γ): a single scalar—lower γ is more conservative, higher γ is more aggressive, it will convert into risk aversion score for MVO framework.")
    st.write("• Optimization: MVO finds weights that balance return vs risk and then enforces practical constraints (sum-to-one, bounds, etc.).")
    st.write("• Robustness: we apply covariance shrinkage, regularization, box constraints and turnover penalties to produce implementable allocations across assets with very different risk profiles (e.g. bonds vs crypto).")
with col2:
    st.info("Risk Level Score (γ)\n\n0 — Conservative\n\n5 — Balanced\n\n10 — Aggressive")

st.markdown("""
    <div class="feature-box">
        <strong>Practical Adjustments:</strong> Regularization, covariance shrinkage, and convex solvers ensure stable allocations and control turnover.
    </div>
    <div class="feature-box">
        <strong>Why this helps:</strong> Centralizing risk control through γ enables consistent behaviour across asset classes while letting the optimizer exploit expected return signals and cross‑asset diversification.
    </div>
""", unsafe_allow_html=True)

# CTA Section
st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Ready to Build Your Portfolio?</h2>
        <p style="color: white; font-size: 1.1rem; margin-bottom: 30px;">
            Experience our interactive ERC optimization tool and create your personalized investment strategy
        </p>
        <a href="https://xiaohai12-quantitative-risk-manag-streamlitstreamlit-app-w9wlfm.streamlit.app/~/+/ERC_portfolio" 
           class="cta-button" target="_blank">
            Launch ERC Portfolio Builder
        </a>
    </div>
""", unsafe_allow_html=True)
