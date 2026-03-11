import streamlit as st
import requests
import time

# 1. Page Config
st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

# 2. Force Dark Mode Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Altcoin Gem Scanner")
st.subheader("Find the next big altcoin before it pumps")
st.markdown("---")

# 3. Filters
col1, col2 = st.columns(2)
with col1:
    max_cap = st.slider("Max Market Cap (Millions $)", 10, 500, 100)
with col2:
    st.markdown("#### 🔴 Red = Dropping | 🟢 Green = Pumping")

st.markdown("---")

# 4. Data Fetching
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd", "order": "volume_desc", "per_page": 250, "page": 1}

try:
    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        gems = [c for c in data if c.get("market_cap") and (c["market_cap"] / 1_000_000) < max_cap]

        st.markdown(f"### Found {len(gems)} gems under ${max_cap}M market cap")

        for coin in gems:
            name, symbol = coin["name"], coin["symbol"].upper()
            price = coin["current_price"]
            change = round(coin.get("price_change_percentage_24h", 0) or 0, 2)
            cap = round(coin["market_cap"] / 1_000_000, 2)

            line = f"**{name} ({symbol})** - ${price} | MCap: ${cap}M | 24h: {change}%"
            if change > 0: st.success(line)
            else: st.error(line)
    else:
        st.warning("🔄 Refreshing market data...")
except:
    st.warning("🔄 Connecting to secure data feed...")

# 5. THE SAFE REFRESH (Better than while True)
time.sleep(60)
st.rerun()