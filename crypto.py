import streamlit as st
import requests

st.set_page_config(page_title="Altcoin Gem Scanner", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
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
    .fear-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.5rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 150, "page": 1}
    try:
        r = requests.get(url, params=params, timeout=15)
        return r.json() if r.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=600)
def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('Data', [])[:6]
    except:
        return []

@st.cache_data(ttl=300)
def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        d = r.json()['data'][0]
        return d['value'], d['value_classification']
    except:
        return None, None

@st.cache_data(ttl=300)
def get_trending():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=10)
        return r.json().get('coins', [])[:3]
    except:
        return []

col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("💎 Altcoin Gem Scanner")
    st.subheader("Market Leaders")
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg", width=160)

with st.spinner("Loading market data..."):
    data = get_crypto_data()
    news = get_crypto_news()
    fg_value, fg_label = get_fear_greed()
    trending = get_trending()

if data:
    m1, m2, m3 = st.columns(3)
    target_symbols = ['btc', 'eth', 'doge']
    cols = [m1, m2, m3]
    for i, sym in enumerate(target_symbols):
        coin = next((c for c in data if c['symbol'] == sym), None)
        if coin:
            with cols[i]:
                st.metric(
                    label=f"$ {coin['name']}", 
                    value=f"${coin['current_price']:,}", 
                    delta=f"{round(coin.get('price_change_percentage_24h', 0) or 0, 2)}%"
                )

    st.write("---")

    if fg_value:
        fg_int = int(fg_value)
        if fg_int >= 75:
            color = "#ff4444"
            emoji = "🔴 Extreme Greed"
        elif fg_int >= 55:
            color = "#ff8800"
            emoji = "🟠 Greed"
        elif fg_int >= 45:
            color = "#ffff00"
            emoji = "🟡 Neutral"
        elif fg_int >= 25:
            color = "#00aaff"
            emoji = "🔵 Fear"
        else:
            color = "#aa00ff"
            emoji = "🟣 Extreme Fear"
        
        st.markdown(f"""
            <div class="fear-box" style="background-color: {color}22; border: 2px solid {color};">
                Market Sentiment: {emoji} — Score: {fg_value}/100 ({fg_label})
            </div>
        """, unsafe_allow_html=True)

    if trending:
        st.markdown("### 🔥 Top 3 Trending Right Now")
        t1, t2, t3 = st.columns(3)
        tcols = [t1, t2, t3]
        for i, coin in enumerate(trending):
            with tcols[i]:
                item = coin['item']
                st.markdown(f"**#{i+1} {item['name']}** ({item['symbol']})")
                st.caption(f"Rank #{item['market_cap_rank']}")

    st.write("---")

    left_side, right_side = st.columns([1.8, 1.2])

    with left_side:
        st.markdown(f"""
            <div class="rh-card">
                <h2 style="color:#00c805; margin:0;">🏹 Robinhood Gold</h2>
                <p style="color:white; margin:10px 0; font-size:1.1rem;">Sign up with my link and we'll both pick our own <b>Gift Stock</b> 🎁</p>
                <a href="https://join.robinhood.com/joser1057" target="_blank" class="rh-button">Claim Your Gift Stock →</a>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("🔍 Search a Coin")
        search = st.text_input("Type a coin name or symbol (e.g. PEPE, SOL)")
        
        st.subheader("Small-Cap Gem Scanner")
        max_cap_m = st.slider("Max Market Cap (Millions $)", 1, 1000, 500)
        gems = [c for c in data if c.get("market_cap") and (c["market_cap"] / 1_000_000) <= max_cap_m]
        final_gems = [g for g in gems if g['symbol'] not in ['btc', 'eth', 'usdt', 'bnb', 'sol', 'xrp', 'doge']]

        if search:
            search_lower = search.lower()
            final_gems = [g for g in final_gems if search_lower in g['name'].lower() or search_lower in g['symbol'].lower()]

        if not final_gems:
            st.info("No coins found. Try adjusting the slider or search term.")
        else:
            for coin in final_gems[:15]:
                change = round(coin.get("price_change_percentage_24h", 0) or 0, 2)
                mcap = round(coin['market_cap'] / 1_000_000, 1)
                text = f"**{coin['name']}** ({coin['symbol'].upper()}) | ${coin['current_price']} | MCap: ${mcap}M | {change}%"
                if change <= -5:
                    st.error("🚨 DIP ALERT: " + text)
                elif change > 0:
                    st.success(text)
                else:
                    st.error(text)

    with right_side:
        st.subheader("Latest News")
        if news:
            for n in news:
                n_col1, n_col2 = st.columns([1, 3])
                with n_col1:
                    st.image(n.get('imageurl'), use_container_width=True)
                with n_col2:
                    st.markdown(f"**[{n['title']}]({n['url']})**")
                    st.caption(f"Source: {n['source']}")
                st.write("---")
        else:
            st.info("Fetching latest headlines...")

    if st.button("🔄 Sync Everything"):
        st.cache_data.clear()
        st.rerun()
else:
    st.warning("🔄 Fetching Market Data... Please wait 30 seconds.")
    st.rerun()