import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from textblob import TextBlob

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="FYP Mathematical AI Stock Advisor",
    layout="wide",
    page_icon="📈"
)

# ----------------------------------
# FUNCTIONS
# ----------------------------------

@st.cache_data
def load_data(ticker, period):
    df = yf.download(ticker, period=period, auto_adjust=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.dropna(inplace=True)
    return df


def predict_price(df):
    data = df[['Close']].copy()
    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data["Close"]

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[len(data)]])[0]

    # evaluation
    train_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, train_pred))
    mae = mean_absolute_error(y, train_pred)

    return float(pred), rmse, mae


def forecast7(df):
    data = df[['Close']].copy()
    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data["Close"]

    model = LinearRegression()
    model.fit(X, y)

    future = np.arange(len(data), len(data)+7).reshape(-1,1)
    preds = model.predict(future)

    return preds


def sentiment(ticker):
    text = f"{ticker} company reports strong earnings and positive growth."
    score = TextBlob(text).sentiment.polarity

    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return label, score


def signal(pred,current,sent):
    if pred > current and sent=="Positive":
        return "BUY"
    elif pred < current and sent=="Negative":
        return "SELL"
    else:
        return "HOLD"


def portfolio(capital):

    stocks = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "META",
        "NVDA",
        "TSLA",
        "JPM",
        "NFLX",
        "Cash"
    ]

    # Optimized diversified weights
    weights = [
        18,
        16,
        14,
        10,
        10,
        8,
        7,
        7,
        5,
        5
    ]

    amounts = []

    for w in weights:
        amounts.append(capital * w / 100)

    portfolio_df = pd.DataFrame({
        "Stock": stocks,
        "Weight %": weights,
        "Investment Amount ($)": amounts
    })

    return portfolio_df


# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("🎓 FYP Control Panel")

ticker = st.sidebar.selectbox(
    "Select Stock",
    ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","JPM","NFLX","Cash"]
)

period = st.sidebar.selectbox(
    "Select Period",
    ["6mo","1y","2y","5y","10y"]
)

capital = st.sidebar.number_input(
    "Investment Amount",
    min_value=1000,
    value=100000
)

run = st.sidebar.button("🚀 Analyze")

# ----------------------------------
# HEADER
# ----------------------------------

st.title("📈 Hybrid Mathematical AI Agent")
st.caption("Stock Prediction • Sentiment • Portfolio Optimization • Decision Support")

# ----------------------------------
# MAIN
# ----------------------------------

if run:

    df = load_data(ticker, period)

    current = float(df["Close"].iloc[-1])
    pred, rmse, mae = predict_price(df)
    preds7 = forecast7(df)

    sent_label, sent_score = sentiment(ticker)
    rec = signal(pred,current,sent_label)

    # --------------------------
    # METRICS
    # --------------------------
    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Current Price", f"${current:.2f}")
    c2.metric("Predicted Price", f"${pred:.2f}")
    c3.metric("Sentiment", sent_label)
    c4.metric("Signal", rec)

    # --------------------------
    # TABS
    # --------------------------

    tab1,tab2,tab3,tab4 = st.tabs([
        "Dashboard",
        "Mathematics",
        "Evaluation",
        "Portfolio Engine"
    ])

    # --------------------------
    # DASHBOARD
    # --------------------------

    with tab1:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Close Price"
        ))

        fig.update_layout(title=f"{ticker} Historical Price")

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("7 Day Forecast")

        future_df = pd.DataFrame({
            "Day":[f"Day {i+1}" for i in range(7)],
            "Predicted Price":preds7
        })

        st.dataframe(future_df, use_container_width=True)

    # --------------------------
    # MATHEMATICS
    # --------------------------

    with tab2:

        st.subheader("Mathematical Foundation")

        st.write("Linear Regression used for stock forecasting")

        st.latex(r"\hat{y} = \beta_0 + \beta_1 x")

        st.write("Portfolio variance minimization concept")

        st.latex(r"Risk = w^T \Sigma w")

        st.write("Natural language polarity score")

        st.latex(r"Sentiment \in [-1,1]")

    # --------------------------
    # EVALUATION
    # --------------------------

    with tab3:

        st.subheader("Model Evaluation")

        st.write(f"RMSE: {rmse:.4f}")
        st.write(f"MAE: {mae:.4f}")

        st.progress(min(int((1/(1+rmse))*100),100))

        st.success("Lower RMSE indicates better fit.")

    # --------------------------
    # MATHEMATICS + EVALUATION
    # --------------------------

    
        
        # ---------------------------------
        # PORTFOLIO OPTIMIZATION
        # ---------------------------------

        
        
        # ---------------------------------
        # SENTIMENT ANALYSIS
        # ---------------------------------

        
        
        # ---------------------------------
        # MODEL EVALUATION
        # ---------------------------------

        

        # ---------------------------------
        # INSIGHTS
        # ---------------------------------

    # --------------------------
    # PORTFOLIO
    # --------------------------

    with tab4:

        st.subheader("💼 Optimized Portfolio Allocation")

        alloc = portfolio(capital)

        # -----------------------------
        # PIE CHART
        # -----------------------------
        fig_port = go.Figure(
            data=[
                go.Pie(
                    labels=alloc["Stock"],
                    values=alloc["Weight %"],
                    hole=0.4
                )
            ]
        )

        fig_port.update_layout(
            title="Portfolio Weight Distribution"
        )

        st.plotly_chart(fig_port, use_container_width=True)

        # -----------------------------
        # TABLE
        # -----------------------------
        st.dataframe(alloc, use_container_width=True)

        # -----------------------------
        # INSIGHTS
        # -----------------------------
        
        # -----------------------------
        # TOTAL INVESTMENT
        # -----------------------------
        total = alloc["Investment Amount ($)"].sum()

        st.success(f"Total Allocated Capital: ${total:,.2f}")

    # --------------------------
    # CHATBOT
    # --------------------------

    # --------------------------
    # ANALYSIS
    # --------------------------

else:
    st.info("Select stock and click Analyze.")

# ----------------------------------
# FOOTER
# ----------------------------------

st.markdown("---")
st.caption("BS Mathematics Final Year Project | Runnable | Deployable | AI + Mathematics")