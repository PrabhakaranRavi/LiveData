import streamlit as st
import yfinance as yf
import pandas as pd
import time
import streamlit.components.v1 as components

st.title("Live Stock Market Data with TradingView Charts")

ticker_symbol = st.text_input("Enter stock ticker:", "MARUTI.NS")
end_date = "2024-07-10"

if st.button("Get Data"):
    st.write(f"Fetching data for {ticker_symbol}...")

    def get_data(ticker):
        data = yf.download(ticker, start=end_date, interval="1m")
        return data

    data = get_data(ticker_symbol)
    
    # Display the data as a table
    st.write("OHLC Data:")
    st.dataframe(data)

    # Prepare data for TradingView chart
    chart_data = data.reset_index()
    chart_data['Date'] = chart_data['Datetime'].astype(int) // 10**9  # Convert to UNIX timestamp

    # Convert the DataFrame to a list of dictionaries
    chart_data_list = chart_data[['Date', 'Open', 'High', 'Low', 'Close']].to_dict(orient='records')

    # TradingView Lightweight Charts
    chart_code = f"""
    <div id="chart" style="width: 100%; height: 400px;"></div>
    <script type="text/javascript">
      const chart = LightweightCharts.createChart(document.getElementById('chart'), {{
        width: 600,
        height: 300,
        layout: {{
          backgroundColor: '#ffffff',
          textColor: '#000',
        }},
        grid: {{
          vertLines: {{
            color: 'rgba(197, 203, 206, 0.5)',
          }},
          horzLines: {{
            color: 'rgba(197, 203, 206, 0.5)',
          }},
        }},
        crosshair: {{
          mode: LightweightCharts.CrosshairMode.Normal,
        }},
        rightPriceScale: {{
          borderColor: 'rgba(197, 203, 206, 0.8)',
        }},
        timeScale: {{
          borderColor: 'rgba(197, 203, 206, 0.8)',
        }},
      }});
      const candleSeries = chart.addCandlestickSeries();
      candleSeries.setData({chart_data_list});
    </script>
    """

    components.html(chart_code, height=400)

# To run the app, use the command: streamlit run stock_app.py
