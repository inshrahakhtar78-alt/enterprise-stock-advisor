import streamlit as st

st.title("🤖 AI Chatbot")

q = st.text_input("Ask about stocks or investing")

if q:

    text = q.lower()

    if "buy" in text:
        st.success("Consider buying strong trend stocks.")

    elif "risk" in text:
        st.warning("Use stop-loss and diversify.")

    elif "portfolio" in text:
        st.info("Balanced portfolio: 60% stocks, 20% ETF, 20% cash.")

    else:
        st.write("Markets are dynamic. Analyze fundamentals + technicals.")
