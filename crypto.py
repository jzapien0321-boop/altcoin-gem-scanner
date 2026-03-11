import streamlit as st
import requests
import time

# 1. THEME & MOBILE SETUP
st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stMetricLabel"] { color: #ffff00 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; }
    .rh-card { border: 2px solid #00c805; background-color: #111b13; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .rh-button { background-color: #00c805; color: black !important; padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. FAIL-SAFE DATA FETCHING
@st.cache_data(ttl=300)
def get_crypto_data():
    # Try Source 1 (CoinGecko)
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 100, "page": 1}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
        
    # BACKUP: Try Source 2 (Binance Public API) if Source 1 fails
    try:
        backup_url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(backup_url, timeout=10)
        if r.status_code == 200:
            # Simple conversion to keep the app running
            raw = r.json()
            return [{"name": b['symbol'], "symbol": b['symbol'].lower().replace('usdt',''), "current_price": float(b['lastPrice']), "market_cap": 100000000, "price_change_percentage_24h": float(b['priceChangePercent'])} for b in raw if 'USDT' in b['symbol']][:50]
    except:
        return None

# 3. APP LOGIC
st.title("💎 Altcoin Gem Scanner")

data = get_crypto_data()

if data:
    # MARKET LEADERS
    st.subheader("Market Leaders")
    m1, m2, m3 = st.columns(3)
    target = ['btc', 'eth', 'doge']
    for i, sym in enumerate(target):
        coin = next((c for c in data if sym in c['symbol']), None)
        if coin:
            with [m1, m2, m3][i]:
                st.metric(label=f"$ {coin['name']}", value=f"${coin['current_price']:,}", delta=f"{coin['price_change_percentage_24h']}%")

    st.write("---")
    
    col_left, col_right = st.columns([1.8, 1.2])
    with col_left:
        # ROBINHOOD AD
        st.markdown(f"""<div class="rh-card"><h3>🏹 Robinhood Gold</h3><p>Sign up and we'll both pick our own <b>Gift Stock</b> 🎁</p>
        <a href="https://join.robinhood.com/joser1057" target="_blank" class="rh-button">Claim Your Gift Stock →</a></div>""", unsafe_allow_html=True)
        
        st.subheader("Gem Scanner")
        max_cap = st.slider("Max Market Cap (Millions $)", 1, 1000, 250)
        for coin in data[5:30]:
            st.success(f"**{coin['name']}** | ${coin['current_price']} | {coin['price_change_percentage_24h']}%")
else:
    st.error("⚠️ Market connection is currently blocked by the provider. Please wait 2 minutes and click below.")
    if st.button("Force Reconnect"):
        st.cache_data.clear()
        st.rerun()