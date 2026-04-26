import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.title("📊 Stock Dashboard")

ticker = st.selectbox(
    "Select Stock",
    ["AAPL","MSFT","GOOGL","TSLA","META","AMZN"]
)

df = yf.download(ticker, period="1y", auto_adjust=True)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.reset_index()

current = round(float(df["Close"].values[-1]),2)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Current Price", f"${current}")
c2.metric("Predicted Price", f"${round(current*1.02,2)}")
c3.metric("Sentiment", "Positive")
c4.metric("Signal", "BUY")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df["Date"],
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"]
))

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Stock Summary")
st.write("Open:", round(float(df["Open"].values[-1]),2))
st.write("High:", round(float(df["High"].values[-1]),2))
st.write("Low:", round(float(df["Low"].values[-1]),2))
st.write("Volume:", int(df["Volume"].values[-1]))
