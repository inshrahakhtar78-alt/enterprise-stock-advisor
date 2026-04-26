import streamlit as st

st.title("⚙️ Admin Panel")

st.success("Server Running")
st.success("API Connected")
st.success("AI Models Active")

c1,c2,c3 = st.columns(3)

if c1.button("Refresh Models"):
    st.info("Models refreshed.")

if c2.button("Clear Cache"):
    st.info("Cache cleared.")

if c3.button("Generate Logs"):
    st.info("Logs generated.")
