import streamlit as st
import yfinance as yf
import pandas as pd
import time
from streamlit_lightweight_charts import renderLightweightCharts

st.title("Live Stock Market Data")

ticker_symbol = st.text_input("Enter stock ticker:", "MARUTI.NS")
end_date = "2024-07-10"

def get_data(ticker):
    data = yf.download(ticker, start=end_date, interval="1m")
    return data

def convert_data_to_candlestick_format(data):
    data = data.reset_index()
    candlestick_data = []
    for index, row in data.iterrows():
        candlestick_data.append({
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close'],
            "time": int(time.mktime(row['Datetime'].timetuple()))
        })
    return candlestick_data

if st.button("Get Data"):
    st.write(f"Fetching data for {ticker_symbol}...")

    data = get_data(ticker_symbol)
    st.write(data)

    # # Display the data as a table
    # st.write("OHLC Data:")
    # st.dataframe(data)

    # # Display the data as a line chart
    # st.line_chart(data['Close'])

    # Convert data to candlestick format
    candlestick_data = convert_data_to_candlestick_format(data)

    # Chart options
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesCandlestickChart = [{
        "type": 'Candlestick',
        "data": candlestick_data,
        "options": {
            "upColor": '#26a69a',
            "downColor": '#ef5350',
            "borderVisible": False,
            "wickUpColor": '#26a69a',
            "wickDownColor": '#ef5350'
        }
    }]

    st.subheader("Candlestick Chart")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesCandlestickChart
        }
    ], 'candlestick')

    # Refresh the data every minute
    refresh_interval = 60  # in seconds
    while True:
        time.sleep(refresh_interval)
        data = get_data(ticker_symbol)
        st.write(data)
        st.line_chart(data['Close'])
        candlestick_data = convert_data_to_candlestick_format(data)
        seriesCandlestickChart[0]["data"] = candlestick_data
        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": seriesCandlestickChart
            }
        ], 'candlestick')

# To run the app, use the command: streamlit run streamlit_app.py
