from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    try:
        project_id = os.environ['GCP_PROJECT_ID']
        # Define table ID and configuration settings
        table_id = f'{project_id}.coinbase.histo'
        config_path = os.path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        # Export DataFrame to BigQuery
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
    except Exception as e:
        print(f"Error occurred during data export to BigQuery: {e}")
        raise ValueError("Failed to export data to BigQuery.")
