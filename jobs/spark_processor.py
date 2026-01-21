from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    LongType,
    BooleanType,
)

# Configuration
KAFKA_BROKERS = "kafka-broker-1:19092,kafka-broker-2:19092,kafka-broker-3:19092"  # Fixed: Use internal Docker network addresses
SOURCE_TOPIC = "financial-transactions"  # Fixed: Match your Java producer topic name
AGGREGATED_TOPIC = "transaction-aggregates"  # Fixed: Use hyphens consistently
ANOMALIES_TOPIC = "transaction-anomalies"
CHECKPOINT_LOCATION = "/mnt/spark-checkpoints"
STATE_DIR = "/mnt/spark-state"

# Create Spark Session
spark = (
    SparkSession.builder.appName("FinancialTransactionProcessor")
    .config("spark.sql.streaming.checkpointLocation", CHECKPOINT_LOCATION)
    .config("spark.sql.streaming.stateStore.stateSchemaCheck", "false")
    .config("spark.sql.shuffle.partitions", 20)
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Define schema - Fixed: Added missing comma and corrected field names
transaction_schema = StructType(
    [
        StructField("transactionId", StringType(), True),  # Match Java producer
        StructField("userId", StringType(), True),
        StructField("merchantId", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("transactionTime", LongType(), True),  # Fixed: Added missing comma
        StructField("transactionType", StringType(), True),
        StructField("location", StringType(), True),
        StructField("paymentMethod", StringType(), True),
        StructField(
            "isInternational", BooleanType(), True
        ),  # Fixed: Changed to BooleanType
        StructField("currency", StringType(), True),
    ]
)

# Read from Kafka
kafka_stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BROKERS)
    .option("subscribe", SOURCE_TOPIC)
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
)

# Parse JSON and extract fields
transaction_df = (
    kafka_stream.selectExpr("CAST(value AS STRING) as json_value")
    .select(from_json(col("json_value"), transaction_schema).alias("data"))
    .select("data.*")
)

# Convert timestamp from milliseconds to timestamp
transaction_df = transaction_df.withColumn(
    "transactionTime", (col("transactionTime") / 1000).cast("timestamp")
)

# Add watermark for late data handling
transaction_df = transaction_df.withWatermark("transactionTime", "10 minutes")

# Aggregate by merchant and time window
aggregated_df = (
    transaction_df.groupBy(
        col("merchantId"), window(col("transactionTime"), "5 minutes")
    )
    .agg(
        sum("amount").alias("total_amount"),
        count("*").alias("transaction_count"),
        avg("amount").alias("avg_amount"),
    )
    .select(
        col("merchantId"),
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("total_amount"),
        col("transaction_count"),
        col("avg_amount"),
    )
)

# Write aggregations to Kafka
aggregation_query = (
    aggregated_df.withColumn("key", col("merchantId").cast("string"))
    .withColumn(
        "value",
        to_json(
            struct(
                col("merchantId"),
                col("window_start"),
                col("window_end"),
                col("total_amount"),
                col("transaction_count"),
                col("avg_amount"),
            )
        ),
    )
    .selectExpr("key", "value")
    .writeStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BROKERS)
    .option("topic", AGGREGATED_TOPIC)
    .option("checkpointLocation", f"{CHECKPOINT_LOCATION}/aggregates")
    .outputMode("update")
    .start()
)

# Console output for monitoring
console_query = (
    transaction_df.writeStream.outputMode("append")
    .format("console")
    .option("truncate", "false")
    .option("numRows", 10)
    .start()
)

# Await termination
aggregation_query.awaitTermination()
