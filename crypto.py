import streamlit as st
import requests
import time

# 1. THEME & MOBILE OPTIMIZATION
st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Dark Mode Base */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Market Leaders: Yellow Token Names ($ BITCOIN) */
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
    
    /* Official Robinhood Green Ad Styling */
    .rh-card { 
        border: 2px solid #00c805; 
        background-color: #111b13; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        margin-bottom: 25px;
    }
    .rh-button {
        background-color: #00c805;
        color: black !important;
        padding: 12px 24px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 15px;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CACHED DATA FETCHING
@st.cache_data(ttl=300)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    # Fetch 150 coins so the slider always has gems to find
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 150, "page": 1}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
    except:
        return None

@st.cache_data(ttl=600)
def get_news_data():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('Data', [])[:6] # Limit to 6 stories for cleaner look
    except:
        return []

# Initialization
if 'data' not in st.session_state:
    st.session_state.data = get_market_data()
if 'news' not in st.session_state:
    st.session_state.news = get_news_data()

# 3. HEADER & MARKET LEADERS
# Layout for Title and the Bitcoin Image
col_logo, col_title = st.columns([1, 6])
with col_logo:
    # --- BITCOIN IMAGE ADDED HERE ---
    st.image("https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029", use_container_width=True)
with col_title:
    st.title("💎 Altcoin Gem Scanner")

data = st.session_state.data
news = st.session_state.news

if data:
    # Market Leaders
    st.subheader("Market Leaders")
    m1, m2, m3 = st.columns(3)
    target = ['btc', 'eth', 'doge']
    cols = [m1, m2, m3]
    for i, sym in enumerate(target):
        coin = next((c for c in data if c['symbol'] == sym), None)
        if coin:
            with cols[i]:
                st.metric(label=f"$ {coin['name']}", value=f"${coin['current_price']:,}", delta=f"{round(coin['price_change_percentage_24h'], 2)}%")

    st.write("---")

    # 4. GEMS & NEWS LAYOUT
    col_left, col_right = st.columns([1.8, 1.2])

    with col_left:
        # Robinhood Ad
        st.markdown(f"""
            <div class="rh-card">
                <h2 style="color:#00c805; margin:0;">🏹 Robinhood Gold</h2>
                <p style="color:white; margin:10px 0;">Sign up and we'll both pick our own <b>Gift Stock</b> 🎁</p>
                <a href="https://join.robinhood.com/joser1057" target="_blank" class="rh-button">Claim Your Gift Stock →</a>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Small-Cap Gem Scanner")
        
        # SLIDER: This is now connected to the code
        slider_input = st.slider("Max Market Cap (Millions $)", 1, 1000, 250, key="cap_slider")
        max_market_cap = slider_input * 1_000_000
        
        # GEM FINDER LOGIC: This uses the slider variable and skips top 10 giants
        gems = [c for c in data if c.get("market_cap") and (c["market_cap"] <= max_market_cap)]
        final_gems = gems[10:50] # Skips leaders
        
        if not final_gems:
            st.info("Searching for gems... try moving the slider to the right.")
        else:
            for coin in final_gems:
                change = round(coin.get("price_change_percentage_24h", 0) or 0, 2)
                mcap = round(coin['market_cap'] / 1_000_000, 1)
                text = f"**{coin['name']}** ({coin['symbol'].upper()}) | ${coin['current_price']} | ${mcap}M | {change}%"
                if change > 0: st.success(text)
                else: st.error(text)

    with col_right:
        # --- NEWS FEED: This is now active on the right column ---
        st.subheader("Latest News")
        if news:
            for n in news:
                n_col1, n_col2 = st.columns([1, 3])
                with n_col1:
                    # Headline image
                    st.image(n.get('imageurl'), use_container_width=True)
                with n_col2:
                    st.markdown(f"**[{n['title']}]({n['url']})**")
                    st.caption(f"Source: {n['source']}")
                st.write("---")
        else:
            st.warning("🔄 Fetching news... hit Sync Everything.")
else:
    st.error("⚠️ Data connection lost. Please click 'Sync Everything' below.")

# 5. SYNC
if st.button("🔄 Sync Everything"):
    # Clear session state to force a clean API call
    if 'data' in st.session_state: del st.session_state.data
    if 'news' in st.session_state: del st.session_state.news
    st.cache_data.clear()
    st.rerun()