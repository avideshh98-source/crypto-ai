import streamlit as st
import requests

st.title("📊 AI Crypto Scalp Tool (v2)")

symbol = st.text_input("Enter coin", "bitcoin")

def get_price(symbol):
    try:
        coin = symbol.replace("USDT", "").lower()

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()

        return float(data[coin]["usd"])
    except:
        return None
def simple_ai_analysis(price):
    # Simple rule-based demo logic

    if price > 50000:
        direction = "SHORT"
        confidence = 65
        reason = "Price is high zone → possible pullback"
    else:
        direction = "LONG"
        confidence = 60
        reason = "Price is lower zone → possible bounce"

    return direction, confidence, reason
if st.button("Analyze Trade"):
    price = get_price(symbol)

    if price is None:
        st.error("Failed to fetch market data. Try again.")
        st.stop()

    direction, confidence, reason = simple_ai_analysis(price)

    st.subheader("Market Data")
    st.write("Price:", price)

    st.subheader("AI Signal")
    st.write("Direction:", direction)
    st.write("Confidence:", confidence)
    st.write("Reason:", reason)
