import streamlit as st
import requests

# 1. THEME & PC/MOBILE FIXES
st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Dark Mode Base */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Market Leaders: Yellow Coin Names, Mint Green Prices */
    [data-testid="stMetricLabel"] { 
        color: #ffff00 !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important; 
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] { color: #00ffcc !important; }
    [data-testid="stMetric"] { 
        background-color: #1f2937; 
        padding: 15px; 
        border-radius: 12px; 
        border: 1px solid #374151; 
    }
    
    /* Title stays White */
    h2 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA CACHING (Fast Loading on S23)
@st.cache_data(ttl=300)
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 200, "page": 1}
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except: return None

@st.cache_data(ttl=600)
def get_crypto_news():
    # Fetch news with images
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        return requests.get(url, timeout=5).json().get('Data', [])[:8]
    except: return []

# 3. HEADER & MARKET LEADERS
st.title("💎 Altcoin Gem Scanner")

data = get_crypto_data()
news = get_crypto_news()

if data:
    # Title stays white, coin labels below are yellow
    st.subheader("Market Leaders")
    m1, m2, m3 = st.columns(3)
    
    # Adding $ sign inside the yellow label
    for i, sym in enumerate(['btc', 'eth', 'doge']):
        coin = next((c for c in data if c['symbol'] == sym), None)
        if coin:
            with [m1, m2, m3][i]:
                # Money sign added next to the yellow coin name
                st.metric(label=f"$ {coin['name']}", value=f"${coin['current_price']:,}", delta=f"{round(coin['price_change_percentage_24h'], 2)}%")

    st.write("---")

    # 4. GEMS & NEWS LAYOUT
    col_left, col_right = st.columns([1.8, 1.2])

    with col_left:
        st.subheader("Small-Cap Gem Scanner")
        max_cap = st.slider("Max Market Cap (Millions $)", 1, 1000, 250)
        
        # FILTER FIX: Logic to make sure gems actually show up
        gems = [c for c in data if c.get("market_cap") and (c["market_cap"] / 1_000_000) <= max_cap]
        
        # Filter out the top 10 so we only see true small-cap gems
        final_gems = gems[10:] if len(gems) > 10 else gems
        
        st.write(f"Found {len(final_gems)} gems below ${max_cap}M")

        for coin in final_gems:
            change = round(coin.get("price_change_percentage_24h", 0) or 0, 2)
            mcap = round(coin['market_cap'] / 1_000_000, 1)
            line = f"**{coin['name']}** ({coin['symbol'].upper()}) | ${coin['current_price']} | MCap: ${mcap}M | {change}%"
            if change > 0: st.success(line)
            else: st.error(line)

    with col_right:
        st.subheader("News Feed")
        if news:
            for n in news:
                n_col1, n_col2 = st.columns([1, 3])
                with n_col1:
                    # Images on the left side
                    st.image(n.get('imageurl'), use_container_width=True)
                with n_col2:
                    st.markdown(f"**[{n['title']}]({n['url']})**")
                    st.caption(f"Source: {n['source']}")
                st.write("---")
else:
    st.warning("🔄 Fetching data... please refresh in a minute.")

# 5. SYNC
if st.button("🔄 Sync Everything"):
    st.cache_data.clear()
    st.rerun()