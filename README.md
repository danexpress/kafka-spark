# Distributed Streaming & Analytics Platform (Kafka + Spark + ELK + Prometheus)

## 📌 Overview
This project is a fully containerized, end-to-end real-time data streaming and analytics platform built using 
Docker Compose. It deploys a production-grade ecosystem consisting of:

- **Kafka KRaft Cluster** (3 controllers + 3 brokers)
- **Spark Cluster** (1 master + 3 workers)
- **Schema Registry**
- **Redpanda Console** for easy topic inspection
- **Prometheus + Alertmanager + Grafana** for metrics and cluster observability
- **ELK Stack** (Elasticsearch, Logstash, Kibana + Filebeat) for centralized log analytics

This platform is designed for:
- Real-time data processing
- Stream ingestion pipelines
- End-to-end observability (metrics + logs)
- Testing distributed data systems locally
- Prototyping streaming architectures before cloud deployment

---

## 🚀 Features

### **🔥 Kafka KRaft Cluster**
- Multi-controller quorum (3 nodes)
- Multi-broker architecture (3 brokers)
- Exposes internal + host listeners
- JMX metrics enabled via Prometheus Java Agent
- Persistent data volumes for durability

### **⚡ Spark Compute Cluster**
- Spark Master + 3 workers
- Volume-mounted Spark job directory
- Supports batch and streaming jobs
- Built for local development with production-style behavior

### **📜 Schema Registry**
- Centralized Avro schema storage
- Ensures serialization consistency across producers/consumers

### **📊 Redpanda Console**
- GUI for inspecting topics, partitions, consumers, offsets, and schemas

### **📈 Observability Stack**
**Prometheus**
- Scrapes Kafka JMX metrics
- Integrated with Spark and system-level monitoring

**Grafana**
- Custom dashboards for Kafka cluster health
- Spark executor and driver metrics
- System performance visualization

### **🪵 ELK Logging Stack**
- Filebeat ships logs → Logstash → Elasticsearch → Kibana dashboards
- Centralized cluster log analytics
- Useful for troubleshooting brokers, controllers, and Spark jobs

---

## 🛠 Architecture Diagram

Kafka Controllers (1,2,3) ---> Kafka Brokers (1,2,3) ---> Schema Registry
| |
| +--> Redpanda Console
Prometheus <------+
Grafana <---------+

  Filebeat --> Logstash --> Elasticsearch --> Kibana

  Spark Master --> Spark Workers (1,2,3)


---

## 📦 Project Structure



├─ jobs/ # Spark job scripts
├─ mnt/ # Spark state + checkpoints
├─ volumes/ # Kafka broker + controller storage
├─ logs/ # Kafka log directories
├─ monitoring/
│ ├─ prometheus/ # Prometheus config
│ ├─ grafana/ # Dashboards + provisioning
│ ├─ elk/
│ ├─ filebeat/ # Filebeat configuration
│ ├─ logstash/ # Logstash pipelines
├─ docker-compose.yml # Full platform orchestration


---

## ▶️ Getting Started

### **1. Install Requirements**
- Docker  
- Docker Compose  
- 16GB RAM recommended  

### **2. Start the Cluster**


docker-compose up -d


### **3. Check Running Containers**


docker ps


---

## 🧪 Testing the Platform

### **Create a Kafka topic**


docker exec -it kafka-broker-1 kafka-topics
--create --topic test-events
--partitions 3
--replication-factor 3
--bootstrap-server kafka-broker-1:19092


### **Produce events**


docker exec -it kafka-broker-1 kafka-console-producer
--topic test-events
--bootstrap-server kafka-broker-1:19092


### **Consume events**


docker exec -it kafka-broker-1 kafka-console-consumer
--topic test-events
--from-beginning
--bootstrap-server kafka-broker-1:19092


---

## 📊 Observability Access

| Tool | URL |
|------|-----|
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Kibana | http://localhost:5601 |
| Redpanda Console | http://localhost:8080 |
| Schema Registry | http://localhost:8082 |

---

## 🧰 Troubleshooting

### **Broker not ready?**
Wait for controllers to elect a quorum:


docker logs kafka-controller-1


### **Prometheus not scraping metrics?**
Ensure JMX exporter volumes are correctly mounted.

### **Elasticsearch memory errors?**
Increase Docker resources or set:


ES_JAVA_OPTS="-Xms512m -Xmx512m"


---

## 📌 Future Enhancements
- Add Kafka Connect for external integrations  
- Add Spark Structured Streaming examples  
- Add dbt-on-Spark transformations  
- Add Airflow DAGs for orchestration  

---

## 🙌 Contributions
PRs, improvements, and ideas are welcome!

---

## 📄 License
MIT License
