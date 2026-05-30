import streamlit as st
import requests
import pandas as pd
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📊 AI Crypto Scalp Tool (v4 - Real RSI)")


coin = st.text_input("Enter coin (bitcoin, ethereum, solana)", "bitcoin")


# ---------------- PRICE ----------------
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    r = requests.get(url)
    data = r.json()
    return float(data[coin]["usd"])


# ---------------- REAL RSI ----------------
def get_rsi(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1"
    r = requests.get(url)
    data = r.json()

    prices = [p[1] for p in data["prices"]]

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# ---------------- AI LOGIC ----------------
def analyze(price, rsi):
    if rsi > 70:
        return "SHORT", 75, "Real RSI overbought → possible pullback"
    elif rsi < 30:
        return "LONG", 75, "Real RSI oversold → possible bounce"
    else:
        return "NO TRADE", 60, "Market neutral zone"


# ---------------- MAIN ----------------
if st.button("Analyze Trade"):
    try:
        price = get_price(coin)
        rsi = get_rsi(coin)

        direction, confidence, reason = analyze(price, rsi)

        st.subheader("Market Data")
        st.write("Price:", price)
        st.write("RSI:", round(rsi, 2))

        st.subheader("AI Signal")
        st.write("Direction:", direction)
        st.write("Confidence:", confidence)
        st.write("Reason:", reason)

    except Exception as e:
        st.error(f"Error: {e}")
