import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# PAGE SETUP
st.set_page_config(
    page_title="Altcoin Gem Scanner",
    page_icon="💎",
    layout="wide"
)

# AUTO REFRESH EVERY 10 SECONDS
st_autorefresh(interval=10000, key="datarefresh")

st.title("💎 Altcoin Gem Scanner")
st.subheader("Find the next big altcoin before it pumps")

st.markdown("---")

# SLIDER
col1, col2 = st.columns(2)

with col1:
    max_cap = st.slider(
        "Max Market Cap (Millions $)",
        min_value=10,
        max_value=500,
        value=100
    )

with col2:
    st.markdown("#### 🔴 Red = Dropping | 🟢 Green = Pumping")

st.markdown("---")

# API SETTINGS
url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "volume_desc",
    "per_page": 250,
    "page": 1,
    "sparkline": False
}

headers = {
    "accept": "application/json",
    "user-agent": "altcoin-gem-scanner"
}

try:

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:

        data = response.json()

        gems = [
            coin for coin in data
            if coin.get("market_cap") and coin["market_cap"] < max_cap * 1000000
        ]

        st.markdown(f"### Found {len(gems)} gems under ${max_cap}M market cap")

        for coin in gems:

            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = coin["current_price"]

            change = coin.get("price_change_percentage_24h", 0)
            if change is None:
                change = 0

            market_cap = round(coin["market_cap"] / 1000000, 2)
            change = round(change, 2)

            line = f"{name} ({symbol}) - ${price} | MCap: ${market_cap}M | 24h: {change}%"

            if change > 0:
                st.success(line)
            else:
                st.error(line)

    else:
        st.warning("⚠️ Market data temporarily unavailable. Refreshing...")

except:
    st.warning("⚠️ Market data loading...")