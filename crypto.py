import streamlit as st
import requests

# 1. Performance & Theme Setup
st.set_page_config(
    page_title="Altcoin Gem Scanner",
    page_icon="💎",
    layout="wide"
)

# 2. Force Dark Mode (Direct CSS Injection)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Simple colored text for mobile speed */
    .pumping { color: #00ffcc; font-weight: bold; }
    .dropping { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Fast Data Loading (Caching)
# This saves the data for 120 seconds to prevent API lag
@st.cache_data(ttl=120)
def fetch_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": 80, # Reduced count for instant mobile loading
        "page": 1
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

# 4. Header Section
st.title("💎 Altcoin Gem Scanner")
st.write("---")

# 5. Filter Controls
max_cap = st.slider("Max Market Cap (Millions $)", 10, 500, 100)

# 6. Main Logic
data = fetch_market_data()

if data:
    # Quick Filter logic
    gems = [c for c in data if c.get("market_cap") and (c["market_cap"] / 1_000_000) < max_cap]
    
    st.subheader(f"📊 Tracking {len(gems)} Potential Gems")

    for coin in gems:
        name = coin["name"]
        symbol = coin["symbol"].upper()
        price = coin["current_price"]
        change = round(coin.get("price_change_percentage_24h", 0) or 0, 2)
        mcap = round(coin["market_cap"] / 1_000_000, 1)

        # Faster rendering for mobile: Simple color-coded lines
        if change > 0:
            st.markdown(f"🟢 **{name} ({symbol})** | ${price} | Cap: ${mcap}M | +{change}%")
        else:
            st.markdown(f"🔴 **{name} ({symbol})** | ${price} | Cap: ${mcap}M | {change}%")
else:
    st.warning("🔄 Fetching fresh market data... Try again in a few seconds.")

# 7. Manual Refresh (Saves Battery and Data)
if st.button("🔄 Check for New Pumps"):
    st.cache_data.clear()
    st.rerun()