"""Tests unitaires pour le job Spark Structured Streaming."""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import sys
sys.path.insert(0, '../src')

from streaming_kafka import NETFLOW_SCHEMA, AUTH_SCHEMA, compute_netflow_features, compute_auth_features


@pytest.fixture(scope="session")
def spark():
    """SparkSession pour les tests."""
    return (
        SparkSession.builder
        .appName("test-sentinel")
        .master("local[1]")
        .config("spark.sql.streaming.schemaInference", "true")
        .getOrCreate()
    )


def test_netflow_schema_valid():
    """Vérifie que le schéma netflow a tous les champs requis."""
    required_fields = {"timestamp", "src_ip", "dst_ip", "src_port", "dst_port", "protocol", "bytes", "packets", "duration_ms", "flags", "label"}
    schema_fields = {f.name for f in NETFLOW_SCHEMA.fields}
    assert required_fields.issubset(schema_fields)


def test_auth_schema_valid():
    """Vérifie que le schéma auth a tous les champs requis."""
    required_fields = {"timestamp", "src_ip", "dst_ip", "service", "user", "status", "label"}
    schema_fields = {f.name for f in AUTH_SCHEMA.fields}
    assert required_fields.issubset(schema_fields)


def test_compute_netflow_features(spark):
    """Teste le calcul des features netflow sur données synthétiques."""
    data = [
        ("2026-10-19T14:00:00", "10.0.1.1", "10.0.1.2", 1234, 80, "TCP", 100, 1, 10, "SYN", "normal"),
        ("2026-10-19T14:00:01", "10.0.1.1", "10.0.1.3", 1235, 443, "TCP", 200, 2, 20, "ACK", "normal"),
        ("2026-10-19T14:00:02", "10.0.1.1", "10.0.1.4", 1236, 22, "TCP", 50, 1, 5, "SYN", "normal"),
    ]
    df = spark.createDataFrame(data, NETFLOW_SCHEMA)
    df = df.withColumn("event_time", df["timestamp"].cast("timestamp"))

    features = compute_netflow_features(df)
    assert features is not None
    # Vérifier que les colonnes attendues existent
    feature_cols = {f.name for f in features.schema.fields}
    expected_cols = {"src_ip", "window_start", "window_end", "conn_count", "unique_dst_ips", "unique_dst_ports", "total_bytes", "avg_duration_ms", "syn_ratio", "port_diversity"}
    assert expected_cols.issubset(feature_cols)


def test_compute_auth_features(spark):
    """Teste le calcul des features auth sur données synthétiques."""
    data = [
        ("2026-10-19T14:00:00", "10.0.1.1", "10.0.1.22", "ssh", "root", "failed", "brute_force"),
        ("2026-10-19T14:00:01", "10.0.1.1", "10.0.1.22", "ssh", "admin", "failed", "brute_force"),
        ("2026-10-19T14:00:02", "10.0.1.1", "10.0.1.22", "ssh", "ubuntu", "success", "normal"),
    ]
    df = spark.createDataFrame(data, AUTH_SCHEMA)
    df = df.withColumn("event_time", df["timestamp"].cast("timestamp"))

    features = compute_auth_features(df)
    assert features is not None
    feature_cols = {f.name for f in features.schema.fields}
    expected_cols = {"src_ip", "window_start", "window_end", "auth_attempts", "failed_attempts", "unique_users"}
    assert expected_cols.issubset(feature_cols)
