import streamlit as st
import requests
from openai import OpenAI

# ---------------- OPENAI ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📊 AI Crypto Scalp Tool (v5 - AI Brain)")

coin = st.text_input(
    "Enter coin (bitcoin, ethereum, solana)",
    "bitcoin"
)

# ---------------- PRICE ----------------
def get_price(coin):
    url = (
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin}&vs_currencies=usd"
    )

    r = requests.get(url, timeout=10)
    data = r.json()

    return float(data[coin]["usd"])


# ---------------- RSI ----------------
def get_rsi(coin):
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin}"
        f"/market_chart?vs_currency=usd&days=1"
    )

    r = requests.get(url, timeout=10)
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

    return round(rsi, 2)


# ---------------- SIGNAL ----------------
def analyze(rsi):
    if rsi > 70:
        return "SHORT", 75, "RSI overbought"
    elif rsi < 30:
        return "LONG", 75, "RSI oversold"
    else:
        return "NO TRA
