import streamlit as st
import requests

st.title("Option Pricer")

product_type = st.selectbox(
    "Product Type",
    ["European Option", "Binary Option", "Interest Rate Swap"]
)
spot = st.number_input("Spot", value=100.0)
strike = st.number_input("Strike", value=100.0)
maturity = st.number_input("Maturity (years)", value=1.0)
rate = st.number_input("Interest Rate", value=0.05)
dividend_yield = st.number_input("Dividend Yield", value=0.0)
volatility = st.number_input("Volatility", value=0.2)
option_type = st.selectbox("Option Type", ["call", "put"])

if st.button("Price Option"):

    payload = {
        "spot": spot,
        "strike": strike,
        "maturity": maturity,
        "rate": rate,
        "dividend_yield": dividend_yield,
        "volatility": volatility,
        "option_type": option_type
    }
    if product_type == "European":
        url = "http://localhost:8000/price"
    else:
        payout = st.number_input("Payout", value=1.0)
        payload["payout"] = payout
        url = "http://localhost:8000/price/binary"

    response = requests.post(url, json=payload)
    price = response.json()["price"]

    st.success(f"Option Price: {price:.4f}")