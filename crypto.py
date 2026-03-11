import streamlit as st
import requests
import time

# 1. Page Config - Forces Dark Mode and collapses the sidebar by default
st.set_page_config(
    page_title="Altcoin Gem Scanner", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Proper Dark Mode Styling (CSS)
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    /* Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
    }
    /* Success/Error blocks */
    div[data-testid="stNotification"] {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section (Totally original name)
st.markdown("# 💎 Altcoin Gem Scanner")
st.markdown("### Specialized Small-Cap Market Intelligence")
st.markdown("---")

# 4. Filters
col1, col2 = st.columns([2, 1])
with col1:
    max_cap = st.slider("Max Market Cap (Millions $)", 1, 500, 100)
with col2:
    st.markdown("#### 🔴 Down | 🟢 Up")

st.markdown("---")

# 5. The Scanner Logic
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd", 
    "order": "market_cap_desc", 
    "per_page": 250, 
    "page": 1, 
    "sparkline": False
}

try:
    response = requests.get(url, params=params)
    data = response.json()

    # Filtering for those small-cap "Gems"
    gems = [coin for coin in data if coin['market_cap'] and coin['market_cap'] < max_cap * 1000000]

    st.markdown(f"### Found {len(gems)} assets matching your filter")

    # 6. Displaying the results
    for coin in gems:
        name = coin['name']
        symbol = coin['symbol'].upper()
        price = coin['current_price']
        change = coin['price_change_percentage_24h'] or 0
        cap = round(coin['market_cap'] / 1000000, 2)
        
        display_text = f"**{name} ({symbol})** | Price: ${price:,.4f} | MCap: ${cap}M | 24h: {change:+.2f}%"
        
        if change > 0:
            st.success(display_text)
        else:
            st.error(display_text)

except Exception as e:
    st.warning("Connecting to secure data feed...")

# Auto-refresh every 60 seconds
time.sleep(60)
st.rerun()