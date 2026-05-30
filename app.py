import streamlit as st
import requests

st.title("📊 Crypto AI Scalp Tool")

symbol = st.text_input("Enter coin", "BTCUSDT")

def get_price(symbol):
    url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    return requests.get(url).json()

if st.button("Analyze"):
    data = get_price(symbol)
    st.write("Price:", data["price"])
    st.write("System working ✔")
