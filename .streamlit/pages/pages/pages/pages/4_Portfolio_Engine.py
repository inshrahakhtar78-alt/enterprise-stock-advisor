import streamlit as st
import pandas as pd

st.title("💼 Portfolio Engine")

capital = st.number_input(
    "Investment Amount",
    min_value=1000,
    max_value=10000000,
    value=10000
)

df = pd.DataFrame({
    "Stock":["AAPL","MSFT","GOOGL","TSLA","Cash"],
    "Allocation %":[35,25,20,10,10]
})

df["Investment"] = df["Allocation %"] * capital / 100

st.dataframe(df, use_container_width=True)

st.success("Optimized portfolio generated.")
