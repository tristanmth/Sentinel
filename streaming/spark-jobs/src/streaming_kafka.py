#!/usr/bin/env python3
"""Job Spark Structured Streaming — SENTINEL S3.

Lit les topics Kafka `netflow` et `auth`, calcule des features par fenêtre
glissante (5 min), et écrit les résultats au format Parquet sur LocalStack (S3).

Usage :
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \\
    streaming_kafka.py
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, window, count, countDistinct, sum as _sum, avg,
    from_json, when
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# ── Configuration ─────────────────────────────
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localstack:4566")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "sentinel")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "sentinel123")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR", "/tmp/spark-checkpoints")

# ── Schémas JSON ──────────────────────────────
NETFLOW_SCHEMA = StructType([
    StructField("timestamp", StringType()),
    StructField("src_ip", StringType()),
    StructField("dst_ip", StringType()),
    StructField("src_port", IntegerType()),
    StructField("dst_port", IntegerType()),
    StructField("protocol", StringType()),
    StructField("bytes", IntegerType()),
    StructField("packets", IntegerType()),
    StructField("duration_ms", IntegerType()),
    StructField("flags", StringType()),
    StructField("label", StringType()),
])

AUTH_SCHEMA = StructType([
    StructField("timestamp", StringType()),
    StructField("src_ip", StringType()),
    StructField("dst_ip", StringType()),
    StructField("service", StringType()),
    StructField("user", StringType()),
    StructField("status", StringType()),
    StructField("label", StringType()),
])


def create_spark_session():
    return (
        SparkSession.builder
        .appName("sentinel-streaming")
        .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", S3_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", S3_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .config("spark.sql.streaming.checkpointLocation", CHECKPOINT_DIR)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
        .getOrCreate()
    )


def read_kafka_stream(spark, topic, schema):
    """Lit un topic Kafka et parse le JSON."""
    return (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", topic)
        .option("startingOffsets", "latest")
        .load()
        .selectExpr("CAST(value AS STRING) as json_str")
        .select(from_json(col("json_str"), schema).alias("data"))
        .select("data.*")
        .withColumn("event_time", col("timestamp").cast(TimestampType()))
    )


def compute_netflow_features(df):
    """Agrégations par IP source sur fenêtre de 5 minutes."""
    return (
        df.withWatermark("event_time", "10 minutes")
        .groupBy(
            col("src_ip"),
            window(col("event_time"), "5 minutes")
        )
        .agg(
            count("*").alias("conn_count"),
            countDistinct("dst_ip").alias("unique_dst_ips"),
            countDistinct("dst_port").alias("unique_dst_ports"),
            _sum("bytes").alias("total_bytes"),
            avg("duration_ms").alias("avg_duration_ms"),
            (count(when(col("flags") == "SYN", True)) / count("*")).alias("syn_ratio"),
            (countDistinct("dst_port") / count("*")).alias("port_diversity"),
        )
        .select(
            col("src_ip"),
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("conn_count"),
            col("unique_dst_ips"),
            col("unique_dst_ports"),
            col("total_bytes"),
            col("avg_duration_ms"),
            col("syn_ratio"),
            col("port_diversity"),
        )
    )


def compute_auth_features(df):
    """Agrégations auth : échecs par IP sur fenêtre de 5 minutes."""
    return (
        df.withWatermark("event_time", "10 minutes")
        .groupBy(
            col("src_ip"),
            window(col("event_time"), "5 minutes")
        )
        .agg(
            count("*").alias("auth_attempts"),
            count(when(col("status") == "failed", True)).alias("failed_attempts"),
            countDistinct("user").alias("unique_users"),
        )
        .select(
            col("src_ip"),
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("auth_attempts"),
            col("failed_attempts"),
            col("unique_users"),
        )
    )


def write_stream(df, output_path):
    """Écrit le stream au format Parquet sur S3."""
    return (
        df.writeStream
        .outputMode("append")
        .format("parquet")
        .option("path", output_path)
        .option("checkpointLocation", f"{CHECKPOINT_DIR}/{output_path.split('/')[-1]}")
        .start()
    )


def main():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    print("=== SENTINEL Streaming Job démarré ===", flush=True)
    print(f"S3 endpoint: {S3_ENDPOINT}", flush=True)

    netflow_raw = read_kafka_stream(spark, "netflow", NETFLOW_SCHEMA)
    auth_raw = read_kafka_stream(spark, "auth", AUTH_SCHEMA)

    netflow_features = compute_netflow_features(netflow_raw)
    auth_features = compute_auth_features(auth_raw)

    query_netflow = write_stream(netflow_features, "s3a://sentinel-data/features/netflow")
    query_auth = write_stream(auth_features, "s3a://sentinel-data/features/auth")

    query_console = (
        netflow_features.writeStream
        .outputMode("complete")
        .format("console")
        .option("truncate", False)
        .start()
    )

    print("Streams démarrés. Attente de données...", flush=True)
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
