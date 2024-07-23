# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import time
# from streamlit_lightweight_charts import renderLightweightCharts

# st.title("Live Stock Market Data")

# ticker_symbol = st.text_input("Enter stock ticker:", "MARUTI.NS")
# end_date = "2024-07-10"

# def get_data(ticker):
#     data = yf.download(ticker, start=end_date, interval="1m")
#     return data

# def convert_data_to_candlestick_format(data):
#     data = data.reset_index()
#     candlestick_data = []
#     for index, row in data.iterrows():
#         candlestick_data.append({
#             "open": row['Open'],
#             "high": row['High'],
#             "low": row['Low'],
#             "close": row['Close'],
#             "time": int(time.mktime(row['Datetime'].timetuple()))
#         })
#     return candlestick_data

# if st.button("Get Data"):
#     st.write(f"Fetching data for {ticker_symbol}...")

#     data = get_data(ticker_symbol)
#     st.write(data)

#     # # Display the data as a table
#     # st.write("OHLC Data:")
#     # st.dataframe(data)

#     # # Display the data as a line chart
#     # st.line_chart(data['Close'])

#     # Convert data to candlestick format
#     candlestick_data = convert_data_to_candlestick_format(data)

#     # Chart options
#     chartOptions = {
#         "layout": {
#             "textColor": 'black',
#             "background": {
#                 "type": 'solid',
#                 "color": 'white'
#             }
#         }
#     }

#     seriesCandlestickChart = [{
#         "type": 'Candlestick',
#         "data": candlestick_data,
#         "options": {
#             "upColor": '#26a69a',
#             "downColor": '#ef5350',
#             "borderVisible": False,
#             "wickUpColor": '#26a69a',
#             "wickDownColor": '#ef5350'
#         }
#     }]

#     st.subheader("Candlestick Chart")
#     renderLightweightCharts([
#         {
#             "chart": chartOptions,
#             "series": seriesCandlestickChart
#         }
#     ], 'candlestick')

#     # Refresh the data every minute
#     refresh_interval = 60  # in seconds
#     while True:
#         time.sleep(refresh_interval)
#         data = get_data(ticker_symbol)
#         st.write(data)
#         st.line_chart(data['Close'])
#         candlestick_data = convert_data_to_candlestick_format(data)
#         seriesCandlestickChart[0]["data"] = candlestick_data
#         renderLightweightCharts([
#             {
#                 "chart": chartOptions,
#                 "series": seriesCandlestickChart
#             }
#         ], 'candlestick')

# # To run the app, use the command: streamlit run streamlit_app.py
import streamlit as st
from supabase import create_client, Client
import uuid

# Supabase configuration
url = "https://ggmsabzwvfglwkpiymzg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbXNhYnp3dmZnbHdrcGl5bXpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3MDE4MDIsImV4cCI6MjAzNzI3NzgwMn0.tTpxh_aQbQWSiHHFPxn5rybFD2yJkl90RhbJQBOmlMI"
supabase: Client = create_client(url, key)

# Function to insert a new job post
def insert_job_post(location, link, description=""):
    data = {
        "id": str(uuid.uuid4()),
        "location": location,
        "link": link,
        "description": description
    }
    supabase.table("job_posts").insert(data).execute()

# Function to get job posts by location
def get_job_posts(location):
    response = supabase.table("job_posts").select("*").eq("location", location).execute()
    return response.data

# Streamlit UI
st.title("Job Vacancies Tracker")

menu = ["Add Job Post", "View Job Posts"]
choice = st.sidebar.selectbox("Menu", menu)

locations = ["Chennai", "Bangalore", "Coimbatore", "Trichy", "Madurai"]

if choice == "Add Job Post":
    st.subheader("Add Job Post")
    location = st.selectbox("Select Location", locations)
    link = st.text_input("Job Post Link")
    description = st.text_area("Description (optional)")

    if st.button("Add"):
        if link:
            insert_job_post(location, link, description)
            st.success("Job post added successfully!")
        else:
            st.error("Job post link is required.")

elif choice == "View Job Posts":
    st.subheader("View Job Posts")
    location = st.selectbox("Select Location to View", locations)
    if st.button("View"):
        posts = get_job_posts(location)
        if posts:
            for post in posts:
                st.write(f"**Link**: {post['link']}")
                if post['description']:
                    st.write(f"**Description**: {post['description']}")
                st.write("---")
        else:
            st.write("No job posts found for this location.")
