import os
import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import logging

@st.cache_data
def load_and_process(url_or_path_to_csv_file):
    # Method Chain 1 (Load data and deal with missing data)
    return (
        pd.read_csv(url_or_path_to_csv_file)
        .dropna()
        .reset_index(drop=True)
        .sort_values("Date")
    )

@st.cache_data
def query_bigQuery(query, project_id):
    # Initialize BigQuery client using the credentials

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_path is None:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(project=project_id, credentials=credentials)

    # Execute the query and fetch the results
    query_job = client.query(query)

    # Convert the query results to a DataFrame
    rows = query_job.result()
    data = []

    # Iterate over the rows and convert to a list of dictionaries
    for row in rows:
        data.append(dict(row.items()))

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    #df.loc[:, 'Date'] = pd.to_datetime(df['Date'])
    
    return df
