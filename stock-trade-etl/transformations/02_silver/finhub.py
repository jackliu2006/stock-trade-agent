from pyspark import pipelines as dp
from pyspark.sql.functions import col
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col, current_timestamp

SCHEMA_REGISTRY_URL = "https://avnadmin:AVNS_B_DQPXg1RMTpiEgjEyB@kafka-jack-stock-trade.l.aivencloud.com:27823"  # replace port if different
SR_USERNAME = "avnadmin"
SR_PASSWORD = "AVNS_B_DQPXg1RMTpiEgjEyB"
# Subject name follows the default Confluent naming strategy: <topic>-value
SUBJECT = "stock_trade-value"
# Options passed to from_avro for authenticated Schema Registry access
schema_registry_options = {
    "confluent.schema.registry.basic.auth.credentials.source": "USER_INFO",
    "confluent.schema.registry.basic.auth.user.info": f"{SR_USERNAME}:{SR_PASSWORD}",
    # If Aiven Schema Registry uses a self-signed cert, also set:
    # "confluent.schema.registry.ssl.truststore.location":   "/Volumes/workspace/stock/kafka-certs/kafka.truststore.jks",
    # "confluent.schema.registry.ssl.truststore.password":   "Welcome1",
}


@dp.table(
    name="finhub_silver",
    comment="Parsed Avro records from finhub_bronze using Aiven Schema Registry",
    table_properties={"quality": "silver"},
)
def finhub_silver():
    return spark.readStream.table("finhub_bronze").select(
        from_avro(
            data=col("value"), subject=SUBJECT, schemaRegistryAddress=SCHEMA_REGISTRY_URL, options = schema_registry_options
        ).alias("data")
    ).select("data.*")
