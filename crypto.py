import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh # ✅ correct spelling

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(
    page_title="Altcoin Gem Scanner",
    page_icon="💎",
    layout="wide"
)

# Auto-refresh every 10 seconds
st_autorefresh(interval=10000, key="datarefresh")

st.title("💎 Altcoin Gem Scanner")
st.subheader("Find the next big altcoin before it pumps")
st.markdown("---")

# ---------------------------
# FILTER SETTINGS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    max_cap = st.slider(
        "Max Market Cap (Millions $)",
        min_value=10,
        max_value=500,
        value=100
    )

with col2:
    st.markdown("#### 🔴 Red = Dropping | 🟢 Green = Pumping")

st.markdown("---")

# ---------------------------
# API SETTINGS
#