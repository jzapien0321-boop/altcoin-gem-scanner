import streamlit as st
import requests

st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.markdown("# 💎 Altcoin Gem Scanner")
st.markdown("### Find the next big altcoin before it pumps")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    max_cap = st.slider("Max Market Cap (Millions $)", 10, 500, 100)
with col2:
    st.markdown("#### 🔴 Red = Dropping | 🟢 Green = Pumping")

st.markdown("---")

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd", "order": "volume_desc", "per_page": 250, "page": 1, "sparkline": False}

response = requests.get(url, params=params)
data = response.json()

gems = [coin for coin in data if coin['market_cap'] and coin['market_cap'] < max_cap * 1000000]

st.markdown(f"### Found {len(gems)} gems under ${max_cap}M market cap")

for coin in gems:
    name = coin['name']
    symbol = coin['symbol'].upper()
    price = str(coin['current_price'])
    change = coin['price_change_percentage_24h']
    cap = round(coin['market_cap'] / 1000000, 2)
    change = round(change, 2)
    line = name + " (" + symbol + ") - $" + price + " | MCap: $" + str(cap) + "M | 24h: " + str(change) + "%"
    if change > 0:
        st.success(line)
    else:
        st.error(line)