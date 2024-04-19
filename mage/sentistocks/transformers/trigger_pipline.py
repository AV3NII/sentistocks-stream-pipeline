import json
import requests
import pandas as pd
from mage_ai.orchestration.triggers.api import trigger_pipeline

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
    
@transformer
def transform(data: pd.DataFrame, *args, **kwargs):
    if pd.isna(data['Date'].iloc[0]):
        trigger_pipeline(
            'coinbase_histo',
            variables={ "start_date": "2023-7-1" },
            check_status=False,
            error_on_failure=False,
            poll_interval=60,
            poll_timeout=None,
            schedule_name=None,  # Enter a unique name to create a new trigger each time
            verbose=True,
        )
        
    else:
        print(f"Most recent date in BigQuery is {data['Date'].iloc[0] }. Load full historical data")
        
        trigger_pipeline(
            'coinbase_histo',
            variables={ "start_date":  str(data['Date'].iloc[0])},
            check_status=False,
            error_on_failure=False,
            poll_interval=60,
            poll_timeout=None,
            schedule_name=None,  # Enter a unique name to create a new trigger each time
            verbose=True,
        )
