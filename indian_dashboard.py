import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# Page settings
st.set_page_config(page_title="🇮🇳 Live Indian Stock Dashboard", layout="wide")

st.title("📊 Live Indian Stock Market Dashboard (NSE)")

# Sidebar controls
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Enter NSE Symbol (e.g. RELIANCE.NS, TCS.NS, HDFCBANK.NS)", "RELIANCE.NS").upper()
refresh_sec = st.sidebar.slider("Refresh interval (seconds)", 15, 300, 60)
period_days = st.sidebar.slider("Days of data", 5, 180, 30)
ma_short = st.sidebar.number_input("Short MA", 5, 50, 10)
ma_long = st.sidebar.number_input("Long MA", 10, 200, 50)
show_signals = st.sidebar.checkbox("Show BUY/SELL markers", True)

chart_placeholder = st.empty()
status_placeholder = st.empty()

while True:
    try:
        # Fetch live NSE data
        data = yf.download(symbol, period=f"{period_days}d", interval="1h", progress=False)

        if data.empty:
            st.warning(f"No data found for {symbol}")
            time.sleep(refresh_sec)
            continue

        # Calculate moving averages
        data["SMA_short"] = data["Close"].rolling(window=ma_short).mean()
        data["SMA_long"] = data["Close"].rolling(window=ma_long).mean()

        # Generate buy/sell signals
        data["Signal"] = 0
        data.loc[data["SMA_short"] > data["SMA_long"], "Signal"] = 1
        data.loc[data["SMA_short"] < data["SMA_long"], "Signal"] = -1

        latest_signal = data["Signal"].iloc[-1]
        status = "BUY 🟢" if latest_signal == 1 else "SELL 🔴"
        latest_close = float(data["Close"].iloc[-1])

        # Display signal and price
        status_placeholder.metric(
            label=f"Latest Signal ({symbol})",
            value=status,
            delta=f"₹ {latest_close:.2f}"
        )

        # Plot Candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candles"
        )])

        # Add moving averages
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["SMA_short"],
            mode="lines",
            line=dict(color="green", width=1.5),
            name=f"SMA{ma_short}"
        ))
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["SMA_long"],
            mode="lines",
            line=dict(color="red", width=1.5),
            name=f"SMA{ma_long}"
        ))

        # Add buy/sell markers
        if show_signals:
            buy_signals = data[data["Signal"] == 1]
            sell_signals = data[data["Signal"] == -1]

            fig.add_trace(go.Scatter(
                x=buy_signals.index,
                y=buy_signals["Close"],
                mode="markers",
                marker=dict(symbol="triangle-up", color="lime", size=10),
                name="BUY"
            ))
            fig.add_trace(go.Scatter(
                x=sell_signals.index,
                y=sell_signals["Close"],
                mode="markers",
                marker=dict(symbol="triangle-down", color="red", size=10),
                name="SELL"
            ))

        # Layout customization
        fig.update_layout(
            title=f"{symbol} — Live NSE Candlestick Chart",
            xaxis_title="Time",
            yaxis_title="Price (INR)",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            height=600
        )

        chart_placeholder.plotly_chart(fig, use_container_width=True, key=time.time())

        # Auto refresh
        time.sleep(refresh_sec)

    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(refresh_sec)
