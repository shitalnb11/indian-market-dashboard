<<<<<<< HEAD
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
from plyer import notification  # for desktop alerts

# Streamlit Page Config
st.set_page_config(page_title="📱 Indian Stock Market Dashboard", layout="wide")

# Title
st.markdown("<h2 style='text-align:center;'>📈 Indian Stock Live Dashboard (NSE)</h2>", unsafe_allow_html=True)

# Sidebar Settings
st.sidebar.header("⚙️ Dashboard Settings")
symbols_input = st.sidebar.text_input(
    "Enter NSE symbols (comma separated):",
    "RELIANCE.NS, TCS.NS, HDFCBANK.NS"
)
symbols = [s.strip().upper() for s in symbols_input.split(",")]

refresh_sec = st.sidebar.slider("Refresh interval (seconds)", 15, 300, 60)
period_days = st.sidebar.slider("Days of data", 5, 180, 30)
ma_short = st.sidebar.number_input("Short MA (e.g., 10)", 5, 50, 10)
ma_long = st.sidebar.number_input("Long MA (e.g., 50)", 10, 200, 50)
show_signals = st.sidebar.checkbox("Show BUY/SELL markers", True)

# Placeholder Layout
signal_placeholder = st.empty()
chart_placeholder = st.container()

# Helper Function - Plot Chart
def plot_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Candlestick"
    )])

    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_short"],
                             mode="lines", line=dict(color="lime", width=1.5),
                             name=f"SMA {ma_short}"))
    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_long"],
                             mode="lines", line=dict(color="red", width=1.5),
                             name=f"SMA {ma_long}"))

    if show_signals:
        buy_points = data[data["Signal"] == 1]
        sell_points = data[data["Signal"] == -1]

        fig.add_trace(go.Scatter(x=buy_points.index, y=buy_points["Close"],
                                 mode="markers", marker=dict(symbol="triangle-up", color="lime", size=10), name="BUY"))
        fig.add_trace(go.Scatter(x=sell_points.index, y=sell_points["Close"],
                                 mode="markers", marker=dict(symbol="triangle-down", color="red", size=10), name="SELL"))

    fig.update_layout(
        title=f"{symbol} — Live Chart",
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="Price (INR)",
        xaxis_rangeslider_visible=False,
        height=450
    )
    return fig

# Track last signals to trigger notifications
last_signal_status = {}

# Live Update Loop
while True:
    try:
        summary_data = []

        for symbol in symbols:
            data = yf.download(symbol, period=f"{period_days}d", interval="1h", progress=False)
            if data.empty:
                continue

            # Calculate MAs & signals
            data["SMA_short"] = data["Close"].rolling(ma_short).mean()
            data["SMA_long"] = data["Close"].rolling(ma_long).mean()
            data["Signal"] = 0
            data.loc[data["SMA_short"] > data["SMA_long"], "Signal"] = 1
            data.loc[data["SMA_short"] < data["SMA_long"], "Signal"] = -1

            latest_signal = data["Signal"].iloc[-1]
            latest_close = float(data["Close"].iloc[-1])
            signal_text = "BUY 🟢" if latest_signal == 1 else "SELL 🔴"

            summary_data.append({
                "Stock": symbol,
                "Price (₹)": f"{latest_close:.2f}",
                "Signal": signal_text
            })

            # Send desktop alert only if signal changed
            if symbol in last_signal_status and last_signal_status[symbol] != latest_signal:
                notification.notify(
                    title=f"{symbol} Signal Changed!",
                    message=f"New Signal: {signal_text} | Price ₹{latest_close:.2f}",
                    timeout=5
                )
            last_signal_status[symbol] = latest_signal

            # Display charts
            with chart_placeholder:
                st.plotly_chart(plot_chart(data, symbol), use_container_width=True, key=symbol)

        # Display signals table
        signal_df = pd.DataFrame(summary_data)
        signal_placeholder.subheader(f"📊 Live Signals (Updated: {datetime.now().strftime('%H:%M:%S')})")
        signal_placeholder.dataframe(signal_df, use_container_width=True)

        time.sleep(refresh_sec)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        time.sleep(refresh_sec)
=======
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
from plyer import notification  # for desktop alerts

# Streamlit Page Config
st.set_page_config(page_title="📱 Indian Stock Market Dashboard", layout="wide")

# Title
st.markdown("<h2 style='text-align:center;'>📈 Indian Stock Live Dashboard (NSE)</h2>", unsafe_allow_html=True)

# Sidebar Settings
st.sidebar.header("⚙️ Dashboard Settings")
symbols_input = st.sidebar.text_input(
    "Enter NSE symbols (comma separated):",
    "RELIANCE.NS, TCS.NS, HDFCBANK.NS"
)
symbols = [s.strip().upper() for s in symbols_input.split(",")]

refresh_sec = st.sidebar.slider("Refresh interval (seconds)", 15, 300, 60)
period_days = st.sidebar.slider("Days of data", 5, 180, 30)
ma_short = st.sidebar.number_input("Short MA (e.g., 10)", 5, 50, 10)
ma_long = st.sidebar.number_input("Long MA (e.g., 50)", 10, 200, 50)
show_signals = st.sidebar.checkbox("Show BUY/SELL markers", True)

# Placeholder Layout
signal_placeholder = st.empty()
chart_placeholder = st.container()

# Helper Function - Plot Chart
def plot_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Candlestick"
    )])

    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_short"],
                             mode="lines", line=dict(color="lime", width=1.5),
                             name=f"SMA {ma_short}"))
    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_long"],
                             mode="lines", line=dict(color="red", width=1.5),
                             name=f"SMA {ma_long}"))

    if show_signals:
        buy_points = data[data["Signal"] == 1]
        sell_points = data[data["Signal"] == -1]

        fig.add_trace(go.Scatter(x=buy_points.index, y=buy_points["Close"],
                                 mode="markers", marker=dict(symbol="triangle-up", color="lime", size=10), name="BUY"))
        fig.add_trace(go.Scatter(x=sell_points.index, y=sell_points["Close"],
                                 mode="markers", marker=dict(symbol="triangle-down", color="red", size=10), name="SELL"))

    fig.update_layout(
        title=f"{symbol} — Live Chart",
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="Price (INR)",
        xaxis_rangeslider_visible=False,
        height=450
    )
    return fig

# Track last signals to trigger notifications
last_signal_status = {}

# Live Update Loop
while True:
    try:
        summary_data = []

        for symbol in symbols:
            data = yf.download(symbol, period=f"{period_days}d", interval="1h", progress=False)
            if data.empty:
                continue

            # Calculate MAs & signals
            data["SMA_short"] = data["Close"].rolling(ma_short).mean()
            data["SMA_long"] = data["Close"].rolling(ma_long).mean()
            data["Signal"] = 0
            data.loc[data["SMA_short"] > data["SMA_long"], "Signal"] = 1
            data.loc[data["SMA_short"] < data["SMA_long"], "Signal"] = -1

            latest_signal = data["Signal"].iloc[-1]
            latest_close = float(data["Close"].iloc[-1])
            signal_text = "BUY 🟢" if latest_signal == 1 else "SELL 🔴"

            summary_data.append({
                "Stock": symbol,
                "Price (₹)": f"{latest_close:.2f}",
                "Signal": signal_text
            })

            # Send desktop alert only if signal changed
            if symbol in last_signal_status and last_signal_status[symbol] != latest_signal:
                notification.notify(
                    title=f"{symbol} Signal Changed!",
                    message=f"New Signal: {signal_text} | Price ₹{latest_close:.2f}",
                    timeout=5
                )
            last_signal_status[symbol] = latest_signal

            # Display charts
            with chart_placeholder:
                st.plotly_chart(plot_chart(data, symbol), use_container_width=True, key=symbol)

        # Display signals table
        signal_df = pd.DataFrame(summary_data)
        signal_placeholder.subheader(f"📊 Live Signals (Updated: {datetime.now().strftime('%H:%M:%S')})")
        signal_placeholder.dataframe(signal_df, use_container_width=True)

        time.sleep(refresh_sec)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        time.sleep(refresh_sec)
>>>>>>> d679f2133ccc2d56a2cc8158062fd1c15f51854e
