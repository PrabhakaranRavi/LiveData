import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("Live Stock Market Data")

ticker_symbol = st.text_input("Enter stock ticker:", "MARUTI.NS")
end_date = "2024-07-10"

if st.button("Get Data"):
    st.write(f"Fetching data for {ticker_symbol}...")

    def get_data(ticker):
        data = yf.download(ticker, start=end_date, interval="1m")
        return data

    data = get_data(ticker_symbol)
    st.write(data)

    # Display the data as a table
    st.write("OHLC Data:")
    st.dataframe(data)

    # Display the data as a line chart
    st.line_chart(data['Close'])

    # Refresh the data every minute
    refresh_interval = 60  # in seconds
    while True:
        time.sleep(refresh_interval)
        data = get_data(ticker_symbol)
        st.write(data)
        st.line_chart(data['Close'])

# To run the app, use the command: streamlit run stock_app.py
