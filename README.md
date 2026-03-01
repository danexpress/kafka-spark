# FinStream 🚀
### Real-Time Financial Transaction Pipeline with Distributed Kafka, Spark & Full-Stack Observability



---

## Overview

**FinStream** is a production-grade, containerized distributed streaming platform that ingests, processes, and monitors high-throughput financial transaction events in real time. Built to address visibility and reliability gaps common in event-driven financial systems, it delivers low-latency analytics, fault-tolerant ingestion, and end-to-end observability across a fully distributed workload.

The system simulates a realistic financial transaction stream — purchases, refunds, multi-currency events across merchants and geographies — and processes them continuously through a hardened Kafka KRaft cluster into Spark Streaming, with every layer monitored via ELK and Prometheus.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FinStream Architecture                        │
└─────────────────────────────────────────────────────────────────────┘

  Python Producers (3 threads)
         │
         │  financial_transactions topic
         ▼
┌─────────────────────────────────────┐
│     Kafka KRaft Cluster             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Broker 1 │ │ Broker 2 │ │ Broker 3 │  │
│  │ :29092   │ │ :39092   │ │ :49092   │  │
│  └──────────┘ └──────────┘ └──────────┘  │
│   5 Partitions │ Replication Factor: 3   │
└───────────────────┬─────────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Spark Streaming  │
         │  (spark-master +  │
         │   spark-workers)  │
         └────────┬─────────┘
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
  ┌───────────┐      ┌───────────────┐
  │ Analytics │      │  ELK Stack    │
  │  Output   │      │ Elasticsearch │
  │           │      │  Logstash     │
  └───────────┘      │  Kibana       │
                     └───────────────┘
                            │
                     ┌──────▼──────┐
                     │ Prometheus  │
                     │  + Grafana  │
                     └─────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Event Streaming** | Apache Kafka (KRaft mode — no ZooKeeper) |
| **Stream Processing** | Apache Spark Structured Streaming 3.5 |
| **Producers** | Python/Java + confluent-kafka (multi-threaded) |
| **Log Aggregation** | Elasticsearch + Logstash/Filebeat + Kibana (ELK) |
| **Metrics & Alerting** | Prometheus + Grafana |
| **Containerization** | Docker + Docker Compose |

---

## Key Features

**Kafka KRaft Cluster (No ZooKeeper)**
Three-broker KRaft cluster with multi-controller quorum, eliminating ZooKeeper dependency for simplified operations and improved fault tolerance. Each topic is configured with 5 partitions and replication factor 3 to guarantee data durability and horizontal scalability.

**Multi-Threaded Python and Java Producer**
Generates synthetic financial transaction events — purchases, refunds, multi-currency, international flags — across 3 parallel threads. Producer is tuned for throughput with batching, gzip compression, and buffered sends to minimize latency under load.

**Spark Structured Streaming**
Consumes directly from Kafka and applies real-time transformations — deserialization, enrichment, windowed aggregations — submitted via `spark-submit` to a standalone Spark master with distributed workers.

**Full-Stack Observability**
Every layer is instrumented. ELK captures structured logs from producers, brokers, and Spark jobs. Prometheus scrapes Kafka JMX metrics and broker health. Grafana dashboards surface consumer lag, throughput, and partition leadership in real time.

**Fault-Tolerant Design**
With replication factor 3, the cluster tolerates broker failure without data loss or consumer disruption. Producer `acks=1` balances durability with throughput, appropriate for high-frequency transaction streams.

---

## Project Structure

```
finstream/
├── docker-compose.yml           # Full stack orchestration
├── producers/
│   └── transaction_producer.py  # Multi-threaded Kafka producer
├── spark/
│   └── jobs/
│       └── spark_processor.py   # Spark Structured Streaming job
├── elk/
│   ├── logstash/
│   │   └── pipeline.conf        # Logstash pipeline config
│   └── Filebeat/
│       └── dashboards/          # Pre-built Kibana dashboards
├── monitoring/
│   ├── prometheus.yml           # Prometheus scrape config
│   └── grafana/
│       └── dashboards/          # Grafana dashboard definitions
├── config/
│   └── kafka/
│       └── broker.properties    # Broker configuration
└── README.md
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- 16GB RAM recommended for full stack

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/finstream.git](https://github.com/danexpress/kafka-spark
cd kafka-spark
```

### 2. Start the full stack

```bash
docker-compose up -d
```

This spins up all services: 3 Kafka brokers (KRaft), Spark master + workers, Elasticsearch, Logstash, Kibana, Prometheus, and Grafana.

### 3. Verify Kafka brokers are healthy

```bash
docker exec -it kafka-broker-1 kafka-topics.sh \
  --bootstrap-server localhost:29092 \
  --list
```

### 4. Run the producer

```bash
pip install confluent-kafka
python main.py
```

The producer will auto-create the `financial_transactions` topic if it doesn't exist, then begin streaming events across 3 parallel threads.

### 5. Submit the Spark job

```bash
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /opt/spark/jobs/spark_processor.py
```

### 6. Access dashboards

| Service | URL | Credentials |
|---|---|---|
| Redpanda | http://localhost:8080 | — |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Spark UI | http://localhost:4040 | — |

---

## Kafka Configuration

| Parameter | Value | Rationale |
|---|---|---|
| Brokers | 3 (KRaft) | Multi-controller quorum, no ZooKeeper |
| Partitions | 5 | Parallel consumer throughput |
| Replication Factor | 3 | Full broker failure tolerance |
| `acks` | 1 | Throughput-optimized acknowledgment |
| `compression.type` | gzip | Reduced network I/O at scale |
| `batch.num.messages` | 1000 | Batched sends for efficiency |
| `linger.ms` | 10 | Slight delay to maximize batch size |

---

## Transaction Schema

Each event produced to the `financial_transactions` topic follows this schema:

```json
{
  "transaction_id": "uuid-v4",
  "user_id": "user_42",
  "amount": 87432.50,
  "transactionTime": 1709251200,
  "merchantID": "merchant_2",
  "transactionType": "purchase",
  "location": "location_17",
  "paymentMethod": "credit_card",
  "isInternational": true,
  "currency": "CAD"
}
```

---

## Observability

**ELK Stack**
Logstash ingests structured logs from producers and Spark workers, parsing and indexing them into Elasticsearch. Kibana provides searchable log exploration and pre-built dashboards for transaction volume, error rates, and consumer lag.

**Prometheus + Grafana**
Kafka JMX metrics are scraped by Prometheus and visualized in Grafana. Key metrics monitored include broker throughput (bytes in/out), consumer group lag, partition leadership distribution, and under-replicated partition count — the primary signal for cluster health degradation.

---

## Design Decisions & Tradeoffs

**Why KRaft over ZooKeeper?**
ZooKeeper introduces an additional distributed system to operate, monitor, and scale independently of Kafka. KRaft consolidates metadata management into the broker quorum itself, reducing operational overhead and removing a common failure point. As of Kafka 3.3+, KRaft is production-ready and the direction the ecosystem is moving.

**Why `acks=1` instead of `acks=all`?**
For a high-frequency synthetic transaction stream, `acks=1` provides the right balance — the leader acknowledges the write without waiting for all replica confirmations. For a real production financial system handling actual settlements, `acks=all` with `min.insync.replicas=2` would be the correct choice to prevent any data loss.

**Why gzip compression?**
Financial transaction payloads are JSON with repetitive field names and predictable value ranges — highly compressible. Gzip trades a small amount of CPU for significant network I/O reduction, which matters at high throughput across multiple brokers.

---

## Future Improvements

- Add a dead letter queue (DLQ) topic for malformed or unprocessable events
- Implement consumer group lag alerting in Prometheus with Grafana alert rules
- Add schema registry (Confluent or Apicurio) to enforce Avro schema evolution
- Extend Spark job with fraud detection model inference using MLflow-registered model
- Add Kafka Connect sink to persist processed events to Iceberg/DuckDB for historical analytics

---

## Related Projects

- **[ChurnGuard](#)** — Production-grade churn prediction pipeline with Airflow, MLflow, and PostgreSQL

---

## License

MIT License. See `LICENSE` for details.
