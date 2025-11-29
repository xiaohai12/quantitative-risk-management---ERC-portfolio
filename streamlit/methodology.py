import streamlit as st
import utils.web_util as wu
from statics import IMG_DIR

st.set_page_config(page_title="Strategy overview", layout="wide",initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()
# Nav bar
wu.render_navbar(IMG_DIR)

st.title("Strategy overview")
st.markdown("---")

st.header("What Is Equal Risk Contribution (ERC)?")
st.write("""
Equal Risk Contribution (ERC) is a portfolio optimization method where each asset 
contributes equally to total portfolio risk. Instead of allocating by capital 
(weights) or expected return, ERC allocates by **risk parity**.

This means:
- Each asset’s marginal risk contribution is equal.
- The portfolio avoids concentration in high-volatility assets.
- It naturally adapts to changing market conditions.
""")

st.header("Why We Use ERC")
st.write("""
ERC is particularly attractive for multi-asset or multi-industry portfolios because:

- **Diversification by risk**, not by capital  
- **Stable performance in volatile markets**  
- **Reduced tail-risk exposure**  
- **Transparent and intuitive**  
""")

st.header("Data Description")
st.write("""
Our ERC system uses a multi-asset dataset collected directly from **Yahoo Finance** 
via the `yfinance` API. The dataset covers four major asset classes, allowing us 
to build a diversified and realistic portfolio.

### **1. Equity Data**
We extract historical data for:
- Major equity indices (S&P 500, NASDAQ, Euro Stoxx 50, etc.)
- Sector ETFs (Technology, Energy, Utilities, Financials, etc.)
- Selected individual stocks (optional)

For each equity instrument, we collect:
- Daily Open / High / Low / Close prices  
- Adjusted Close  
- Volume  
- Percentage returns  

Equities provide growth exposure and serve as the main return driver.

---

### **2. Commodity Data**
We include macro-relevant commodities such as:
- Gold (GC=F)
- Crude Oil (CL=F)
- Natural Gas (NG=F)
- Agricultural benchmark ETFs (optional)

Commodities help diversify inflation cycles and supply-shock risks.

---

### **3. Bond Data**
We incorporate fixed-income ETFs and treasury benchmarks, such as:
- US 10-year Treasury (TNX)
- Aggregate bond ETFs (AGG)
- Corporate bond indices (LQD)

Bond assets provide **defensive characteristics**, reducing portfolio volatility.

---

### **4. Cryptocurrency Data**
Crypto instruments (e.g., BTC-USD, ETH-USD) are included to reflect 
high-volatility, high-growth exposures.

We extract:
- Daily Close prices  
- Volatility patterns  
- Correlation vs traditional assets  

Crypto helps analyze the ERC model under extreme-volatility conditions.
""")

st.header("ESG Integration")
st.write("""
We extend the ERC framework to incorporate **carbon intensity** and **ESG metrics**, such as:

- Carbon footprint per company  
- ESG scores (MSCI/Sustainalytics)  
- Sector-level sustainability constraints  

We provide:
- Carbon-adjusted minimum-variance portfolios  
- ERC portfolios under carbon reduction targets (e.g., –30%)  
- Comparison between unconstrained vs ESG-constrained portfolios  
""")

st.markdown("---")
st.subheader("Want to Explore?")
st.markdown(
    'Navigate to **<a href="https://xiaohai12-quantitative-risk-manag-streamlitstreamlit-app-w9wlfm.streamlit.app/~/+/ERC_portfolio" target="_blank">ERC Portfolio</a>** to interact with the optimization tool.',
    unsafe_allow_html=True
)