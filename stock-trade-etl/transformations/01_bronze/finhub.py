from pyspark import pipelines as dp

KAFKA_JAAS_CONFIG = (
    'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required '
    'username="avnadmin" '
    'password="AVNS_B_DQPXg1RMTpiEgjEyB";'
)

options = {
    "kafka.security.protocol": "SASL_SSL",
     "startingOffsets": "earliest",
    "kafka.bootstrap.servers": "kafka-jack-stock-trade.l.aivencloud.com:27831",
    "subscribe": "stock_trade",

    # Truststore (TLS)
    "kafka.ssl.truststore.location": "/Volumes/workspace/stock/kafka-certs/kafka.truststore.jks",
    "kafka.ssl.truststore.password": "Welcome1",

    # Keystore (ONLY needed if you use client certificate / mTLS)
    "kafka.ssl.keystore.location": "/Volumes/workspace/stock/kafka-certs/kafka.keystore.jks",
    "kafka.ssl.keystore.password": "Welcome1",

    # SASL (PLAIN)
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.sasl.jaas.config": KAFKA_JAAS_CONFIG,
}

@dp.table
def finhub_bronze():
    return spark.readStream.format("kafka").options(**options).load()