from pyspark.sql import DataFrame
from pyspark.sql.functions import when, col, month

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data: DataFrame, *args, **kwargs):
    try:

        # Initialize or retrieve Spark session from kwargs
        spark = kwargs.get('spark')
        if spark is None:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder \
                .appName('DataTransformation') \
                .getOrCreate()
            print("New Spark session created.")
        else:
            print("Using existing Spark session.")

        # Define the token mapping
        token_mapping = {
            'AAVE': 'Aave', 'USDT': 'Tether', 'CHZ': 'Chiliz', 'SOL': 'Solana', 'SHIB': 'Shiba Inu',
            'APE': 'ApeCoin', 'ADA': 'Cardano', 'CRO': 'Crypto.com Coin', 'DOGE': 'Dogecoin',
            'CRV': 'Curve DAO Token', 'AXS': 'Axie Infinity', 'ETC': 'Ethereum Classic',
            'UNI': 'Uniswap', 'SNX': 'Synthetix', 'AVAX': 'Avalanche', 'ETH': 'Ethereum',
            'BAT': 'Basic Attention Token', 'LTC': 'Litecoin', 'MASK': 'Mask Network',
            'ATOM': 'Cosmos', 'EOS': 'EOS', 'BICO': 'Biconomy', 'BTC': 'Bitcoin', 'DOT': 'Polkadot'
        }

        # Apply the mapping using a series of when() statements
        mapping_expr = col("Cryptocurrency")
        for token, name in token_mapping.items():
            mapping_expr = when(col("Cryptocurrency") == token, name).otherwise(mapping_expr)

        # Apply the transformation
        transformed_df = data.withColumn("Currency", mapping_expr)

        # Drop the old 'Cryptocurrency' column
        if "Cryptocurrency" in transformed_df.columns:
            transformed_df = transformed_df.drop("Cryptocurrency")
        print(transformed_df.columns)
        
        return transformed_df.toPandas()

    except Exception as e:
        print(f"Error occurred during transformation: {e}")
        raise e


