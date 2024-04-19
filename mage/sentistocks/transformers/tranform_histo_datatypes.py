from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, DateType, FloatType, StringType
from pyspark.sql.functions import hour, month, year, col
from pyspark.context import SparkContext

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    try:
        
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName('KafkaStreamingSparkTransform') \
            .master('local[*]') \
            .config("spark.jars", "/opt/spark/jars/*.jar") \
            .config("spark.jars.packages", "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5") \
            .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS") \
            .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
            .config("spark.hadoop.fs.gs.auth.service.account.enable", "true") \
            .config("spark.hadoop.fs.gs.auth.service.account.json.keyfile", "/home/src/gcp-credentials.json") \
            .getOrCreate()
            #.master('spark://spark-master:7077') \
        
        

        kwargs['spark'] = spark
    
    except Exception as e:
        # Log error message
        print(f"Error occurred during session building: {e}")
        # Raise the exception to halt the pipeline execution
        raise e

    # Specify your transformation logic here
    schema = StructType([
        StructField("date", DateType(), True),
        StructField("low", FloatType(), True),
        StructField("high", FloatType(), True),
        StructField("open", FloatType(), True),
        StructField("close", FloatType(), True),
        StructField("volume", FloatType(), True),
        StructField("token", StringType(), True)
    ])
        
    # Convert Pandas DataFrame to Spark DataFrame
    df = spark.createDataFrame(data, schema)

    # Rename columns
    df = df.withColumnRenamed("date", "Date") \
         .withColumnRenamed("low", "Lowest_Price") \
         .withColumnRenamed("high", "Highest_Price") \
         .withColumnRenamed("open", "Opening_Price") \
         .withColumnRenamed("close", "Closing_Price") \
         .withColumnRenamed("volume", "Volume_Traded") \
         .withColumnRenamed("token", "Cryptocurrency") \
    
    df = df.withColumn("Month", month(col("Date")))
    df = df.withColumn("Year", year(col("Date")))
    return df.toPandas()



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'