import streamlit as st
import requests

# 1. THEME & PAGE SETUP
st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stMetric"] { background-color: #1f2937; padding: 15px; border-radius: 12px; border: 1px solid #374151; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA CACHING (Saves data for speed)
@st.cache_data(ttl=300)
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 100, "page": 1}
    try:
        return requests.get(url, params=params, timeout=5).json()
    except: return None

@st.cache_data(ttl=600)
def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        return requests.get(url, timeout=5).json().get('Data', [])[:5]
    except: return []

# 3. APP HEADER
st.title("💎 Altcoin Gem Scanner")
st.write("---")

data = get_crypto_data()
news = get_crypto_news()

if data:
    # --- BITCOIN & DOGE FIX ---
    # This section always shows the big coins regardless of the slider
    st.subheader("🚀 Market Leaders")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    # We find btc, eth, and doge specifically from the data list
    for i, symbol in enumerate(['btc', 'eth', 'doge']):
        coin = next((c for c in data if c['symbol'] == symbol), None)
        if coin:
            cols = [m_col1, m_col2, m_col3]
            with cols[i]:
                change = round(coin.get('price_change_percentage_24h', 0) or 0, 2)
                st.metric(label=coin['name'], value=f"${coin['current_price']:,}", delta=f"{change}%")

    st.write("---")

    # 4. GEMS & NEWS LAYOUT
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 Small-Cap Gem Scanner")
        max_cap = st.slider("Max Market Cap (Millions $)", 10, 1000, 100)
        
        # This filters out the big coins so you can find the gems
        gems = [c for c in data if c.get("market_cap") and (c["market_cap"] / 1_000_000) < max_cap]
        
        st.write(f"Displaying {len(gems)} tokens under ${max_cap}M")
        
        for coin in gems:
            change = round(coin.get("price_change_percentage_24h", 0) or 0, 2)
            mcap = round(coin['market_cap'] / 1_000_000, 1)
            line = f"**{coin['name']}** ({coin['symbol'].upper()}) | ${coin['current_price']} | MCap: ${mcap}M | {change}%"
            if change > 0: st.success(line)
            else: st.error(line)

    with col_right:
        st.subheader("📰 Latest Crypto News")
        if news:
            for article in news:
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.caption(f"Source: {article['source']} • [Read Story]({article['url']})")
                st.write("---")
        else:
            st.info("News feed refreshing...")

else:
    st.warning("⚠️ Connecting to secure data feeds...")

# 5. SYNC BUTTON
if st.button("🔄 Sync Market & News"):
    st.cache_data.clear()
    st.rerun()