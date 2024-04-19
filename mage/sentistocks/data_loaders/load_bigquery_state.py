from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
import os
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_big_query(*args, **kwargs):
    """
    Template for loading data from a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery

    """
    project_id = os.environ['GCP_PROJECT_ID']
    query = f"SELECT MAX(Date) AS Date FROM `{project_id}.coinbase.histo` limit 1"
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
    


