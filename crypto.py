import streamlit as st
import requests

st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎")
st.title("💎 Altcoin Gem Scanner")
st.write("Top altcoins by volume - updated live")

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd", "order": "volume_desc", "per_page": 50, "page": 1, "sparkline": False}

response = requests.get(url, params=params)
data = response.json()

for coin in data:
    name = coin['name']
    symbol = coin['symbol'].upper()
    price = str(coin['current_price'])
    change = coin['price_change_percentage_24h']
    change = round(change, 2)
    line = name + " (" + symbol + ") - $" + price + " | 24h: " + str(change) + "%"
    if change > 0:
        st.success(line)
    else:
        st.error(line)