import streamlit as st
import pandas as pd
import os

from data_loader import query_bigQuery
from visuals_elements import plot_candlestick_chart, create_correlation_heatmap


def main():
    st.title("Cryptocurrency Analysis Dashboard")
    st.markdown("This dashboard provides insights into cryptocurrency data, including visualizations like candlestick charts and correlation heatmaps.")
    # load data
    project_id = os.getenv("GCP_PROJECT_ID")
    data_available = query_bigQuery(f"SELECT COUNT(1) FROM `{project_id}.coinbase.histo`", project_id)
    st.write(f"Data Available: {data_available.iloc[0, 0]}")
    data_available = data_available.iloc[0, 0] > 0
    if not data_available:
        st.warning("No data available to display. Please check if the database is populated or the query is correct.")
        return
    
    allTokens = query_bigQuery(f"SELECT DISTINCT Cryptocurrency FROM `{project_id}.coinbase.histo`", project_id)
    max_date , min_date = query_bigQuery(f"SELECT MAX(Date) as max_date, MIN(Date) as min_date FROM `{project_id}.coinbase.histo`", project_id).values[0]

    min_date = pd.Timestamp(min_date)
    max_date = pd.Timestamp(max_date)
    st.write(f"**Data Range:** {min_date} to {max_date}")


    # filter data
    currency = st.selectbox("Select Currency", options=allTokens['Cryptocurrency'].unique())
    date_range = st.date_input("Select Date Range", min_value=min_date, max_value=max_date , value=[min_date, max_date], format="YYYY.MM.DD")

    st.write(f"Selected Date Range: {date_range[0]} to {date_range[1]}")

    if not date_range or len(date_range) < 2:
        st.error("No data found for the selected Timeframe. Please select the Time.")
        return
    
    currency_data = query_bigQuery(f"SELECT * FROM `{project_id}.coinbase.histo` WHERE Cryptocurrency = '{currency}' AND Date BETWEEN '{date_range[0]}' AND '{date_range[1]}'", project_id)
    currency_data.loc[:, 'Date'] = pd.to_datetime(currency_data['Date'])


    
    if currency_data.empty:
        st.warning("No data for this currency available to display. Please check if the database is populated or the query is correct.")
        return  # Early return to stop further execution
    
    daterange_data = currency_data[
        (currency_data['Date'] >= pd.to_datetime(date_range[0])) & (currency_data['Date'] <= pd.to_datetime(date_range[1]))
    ]

    if daterange_data.empty:
            st.error("No data found for the selected Timeframe. Please select the Time.")
            return

    
    
    st.write(f"Data Loaded. Shape: {currency_data.shape}")
    

    # visualize data
    st.header("Candlestick Chart")
    ma_options = st.multiselect("Select Moving Averages", options=[5, 10, 20, 30, 40, 50], default=[5, 10])
    candlestick_chart = plot_candlestick_chart(currency_data, ma_options)
    st.plotly_chart(candlestick_chart)

    st.header("Correlation Heatmap")

    correlation_heatmap = create_correlation_heatmap(daterange_data)
    st.plotly_chart(correlation_heatmap)

if __name__ == "__main__":
    main()