import streamlit as st
import requests

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

# 2. DATA CACHING (Critical for S23 Loading)
@st.cache_data(ttl=300)
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 200, "page": 1}
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=600)
def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        r = requests.get(url, timeout=5)
        return r.json().get('Data', [])[:8]
    except:
        return []

# 3. HEADER & MARKET LEADERS
st.title("💎 Altcoin Gem Scanner")

data = get_crypto_data()
news = get_crypto_news()

if data:
    # Market Leaders Title (White), Tokens ($ BITCOIN) in Yellow
    st.subheader("Market Leaders")
    m1, m2, m3 = st.columns(3)
    
    target_symbols = ['btc', 'eth', 'doge']
    cols = [m1, m2, m3]
    
    for i, sym in enumerate(target_symbols):
        coin = next((c for c in data if c['symbol'] == sym), None)
        if coin:
            with cols[i]:
                # Correct indentation for the metric
                st.metric(
                    label=f"$ {coin['name']}", 
                    value=f"${coin['current_price']:,}", 
                    delta=f"{round(coin['price_change_percentage_24h'], 2)}%"
                )

    st.write("---")

    # 4. GEMS & NEWS LAYOUT
    col_left, col_right = st.columns([1.8, 1.2])

    with col_left:
        # --- YOUR ROBINHOOD AD ---
        st.markdown("""
            <div class="rh-card">
                <h2 style="color:#00c805; margin:0;">🏹 Robinhood Gold</h2>
                <p style="color:white; margin:10px 0; font-size:1.1rem;">Sign up with my link and we'll both pick our own <b>Gift Stock</b> 🎁</p>
                <a href="https://join.robinhood.com/joser1057" target="_blank" class="rh-button">Claim Your Gift Stock →</a>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Small-Cap Gem Scanner")
        max_cap = st.slider("Max Market Cap (Millions $)", 1, 1000, 250)
        
        # Filter logic
        gems = [c for c in data if (c["market_cap"] / 1_000_000