import streamlit as st
import requests
import time

# 1. Page Setup (Keep it simple for speed)
st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.title("💎 Altcoin Gem Scanner")

# 2. Sidebar Filter (Moving this to the sidebar makes the main page load faster)
max_cap = st.sidebar.slider("Max Market Cap (Millions $)", 10, 1000, 200)

# 3. API Call with Speed Optimization
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd", 
    "order": "volume_desc", 
    "per_page": 100, # Lowering this from 250 to 100 makes it MUCH faster
    "page": 1
}

try:
    # Adding a simple cache to avoid spamming the API
    response = requests.get(url, params=params, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        
        # Fast Filtering
        gems = [c for c in data if c.get("market_cap") and (c["market_cap"] / 1_000_000) < max_cap]

        st.subheader(f"📊 Found {len(gems)} Gems")

        # Display loop
        for coin in gems:
            change = coin.get("price_change_percentage_24h") or 0
            # Using a simple string for the fastest possible rendering
            line = f"**{coin['name']}** ({coin['symbol'].upper()}) | ${coin['current_price']} | MCap: ${round(coin['market_cap']/1_000_000, 1)}M | {round(change, 2)}%"
            
            if change > 0:
                st.success(line)
            else:
                st.error(line)
    
    elif response.status_code == 429:
        st.warning("⏱️ API is resting. Numbers will return in 60 seconds.")
        time.sleep(60) # Forces a pause if we are being too fast

except Exception as e:
    st.error("Connecting...")

# 4. Balanced Refresh (Don't set this lower than 60 for the free API)
time.sleep(60)
st.rerun()