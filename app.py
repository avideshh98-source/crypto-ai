import streamlit as st
import requests

st.title("📊 AI Crypto Scalp Tool (v3 - Smart Signals)")

coin = st.text_input("Enter coin (bitcoin, ethereum, etc.)", "bitcoin")


# --- PRICE ---
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    r = requests.get(url, timeout=5)
    data = r.json()
    return float(data[coin]["usd"])


# --- RSI (simple version) ---
def fake_rsi(price):
    # simplified RSI-like logic (we upgrade later to real candles)
    return (price % 100)


# --- AI LOGIC ---
def analyze(price, rsi):
    if rsi > 70:
        return "SHORT", 70, "Overbought condition (RSI high)"
    elif rsi < 30:
        return "LONG", 65, "Oversold condition (RSI low)"
    else:
        return "NO TRADE", 50, "Market is sideways / unclear trend"


# --- MAIN ---
if st.button("Analyze Trade"):
    try:
        price = get_price(coin)
        rsi = fake_rsi(price)

        direction, confidence, reason = analyze(price, rsi)

        st.subheader("Market Data")
        st.write("Price:", price)
        st.write("RSI (simulated):", rsi)

        st.subheader("AI Signal")
        st.write("Direction:", direction)
        st.write("Confidence:", confidence)
        st.write("Reason:", reason)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
