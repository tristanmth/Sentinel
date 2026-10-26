from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SentinelKafkaReader")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("Sentinel : connexion à Kafka...")

events = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")    
    .option("subscribe", "sentinel-events")
    .option("startingOffsets", "earliest")
    .load()
)

messages = events.selectExpr("CAST(value AS STRING) AS message")

query = (
    messages.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .start()
)

print("Sentinel écoute maintenant les événements Kafka.")

query.awaitTermination()
