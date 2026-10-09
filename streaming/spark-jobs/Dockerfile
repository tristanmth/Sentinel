FROM apache/spark:3.5.0

WORKDIR /app

# Dépendances Python supplémentaires si besoin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

COPY src/ ./src/

CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "src/streaming_kafka.py"]
