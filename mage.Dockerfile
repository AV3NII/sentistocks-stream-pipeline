FROM mageai/mageai:latest

COPY mage/ /home/src/

COPY secrets/gcp-sentistocks-credentials.json  /home/src/gcp-credentials.json

RUN echo 'deb http://deb.debian.org/debian bullseye main' > /etc/apt/sources.list.d/bullseye.list

# Update package lists and install OpenJDK 11
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jdk-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and add Spark dependencies
RUN mkdir -p /opt/spark/jars \
    && wget -O /opt/spark/jars/spark-core.jar https://repo1.maven.org/maven2/org/apache/spark/spark-core_2.12/3.5.1/spark-core_2.12-3.5.1.jar \
    && wget -O /opt/spark/jars/spark-sql.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql_2.12/3.5.1/spark-sql_2.12-3.5.1.jar \
    && wget -O /opt/spark/jars/spark-streaming.jar https://repo1.maven.org/maven2/org/apache/spark/spark-streaming_2.12/3.5.1/spark-streaming_2.12-3.5.1.jar \
    && wget -O /opt/spark/jars/spark-hive.jar https://repo1.maven.org/maven2/org/apache/spark/spark-hive_2.12/3.5.1/spark-hive_2.12-3.5.1.jar \
    && wget -O /opt/spark/jars/spark-mllib.jar https://repo1.maven.org/maven2/org/apache/spark/spark-mllib_2.12/3.5.1/spark-mllib_2.12-3.5.1.jar \
    && wget -O /opt/spark/jars/gcs-connector-hadoop3-2.2.5.jar https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.5/gcs-connector-hadoop3-2.2.5-shaded.jar \
    && wget -O /opt/spark/jars/google-cloud-storage.jar https://repo1.maven.org/maven2/com/google/cloud/google-cloud-storage/2.1.3/google-cloud-storage-2.1.3.jar

# Install PySpark
RUN pip install -r /home/src/mage_req.txt

ENTRYPOINT [ "mage", "start", "sentistocks" ]