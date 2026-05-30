import streamlit as st
import requests
import google.generativeai as genai

# ---------------- GEMINI SETUP ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

st.title("📊 AI Crypto Scalp Tool (Gemini AI)")

coin = st.text_input("Enter coin (bitcoin, ethereum, solana)", "bitcoin")


# ---------------- PRICE ----------------
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    r = requests.get(url)
    data = r.json()
    return float(data[coin]["usd"])


# ---------------- RSI ----------------
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

    return round(rsi, 2)


# ---------------- SIGNAL ----------------
def analyze(rsi):
    if rsi > 70:
        return "SHORT", 75, "Overbought market"
    elif rsi < 30:
        return "LONG", 75, "Oversold market"
    else:
        return "NO TRADE", 60, "Neutral market"


# ---------------- AI BRAIN (GEMINI) ----------------
def ai_brain(price, rsi, signal):
    prompt = f"""
You are a professional crypto trading assistant.

Analyze this data:

Price: {price}
RSI: {rsi}
Signal: {signal}

Return:
1. Market explanation
2. Trade decision (YES or NO)
3. Risk level (LOW / MEDIUM / HIGH)
4. Short reason
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------- MAIN ----------------
if st.button("Analyze Trade"):
    try:
        price = get_price(coin)
        rsi = get_rsi(coin)

        direction, confidence, reason = analyze(rsi)

        st.subheader("📊 Market Data")
        st.write("Price:", price)
        st.write("RSI:", rsi)

        st.subheader("📈 Signal")
        st.write("Direction:", direction)
        st.write("Confidence:", confidence)
        st.write("Reason:", reason)

        ai_result = ai_brain(price, rsi, direction)

        st.subheader("🧠 AI Brain")
        st.write(ai_result)

    except Exception as e:
        st.error(f"Error: {e}")
