import io
import os
import pandas as pd
import requests
from datetime import datetime, timedelta
import time

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Python http.client'
    })

    def get_json_response(url):
        try:
            response = session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_data(token, start_date, end_date):
        url = f'https://api.exchange.coinbase.com/products/{token}-EUR/candles?start={start_date}&end={end_date}&granularity=86400'
        return get_json_response(url)

    def process_response(data):
        if not data or not isinstance(data, list) or len(data[0]) != 6:
            return pd.DataFrame()
        try:
            df = pd.DataFrame(data, columns=['date', 'low', 'high', 'open', 'close', 'volume'])
            df['date'] = pd.to_datetime(df['date'], unit='s')
            return df
        except Exception as e:
            print(f"Error processing data: {e}")
            return pd.DataFrame()


    def fetch_all_tokens():
        url = "https://api.exchange.coinbase.com/products"
        products = get_json_response(url)
        return [product['id'].split('-')[0] for product in products if '-' in product['id'] and product['id'].split('-')[1] == 'EUR'] if products else []

    
    end_date = kwargs['execution_date'].date()
    start_date = datetime.strptime(kwargs['start_date'], '%Y-%m-%d')
    #earliest_date = datetime.strptime('2023-7-1', '%Y-%m-%d')

    # Check if the start_date is before the earliest accessible date
    #if start_date < earliest_date:
    #    print(f"Adjusted Start Date from {start_date} to {earliest_date}")
    #    start_date = earliest_date


    print("Start Date:", start_date)
    print("End Date:", end_date)

    all_tokens = fetch_all_tokens()
    wanted_tokens = {'AAVE', 'USDT', 'CHZ', 'SOL', 'SHIB', 'APE',
                     'ADA', 'CRO', 'DOGE', 'CRV', 'AXS', 'ETC', 'UNI',
                     'SNX', 'AVAX', 'ETH', 'BAT', 'LTC', 'MASK', 'ATOM',
                     'EOS', 'BICO', 'BTC', 'DOT', 'TRX'}
    selected_tokens = set(all_tokens).intersection(wanted_tokens)

    master_df = pd.DataFrame()
    for token in selected_tokens:
        candles = get_data(token, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        token_df = process_response(candles)
        if not token_df.empty:
            token_df['token'] = token
            master_df = pd.concat([master_df, token_df], ignore_index=True)
            time.sleep(1)  # Be nice to the API

    return master_df

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
