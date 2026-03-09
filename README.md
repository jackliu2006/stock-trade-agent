# Stock Trade Agent

A real-time stock trade analytics pipeline built on **Databricks Lakeflow Declarative Pipelines** with a **Medallion Architecture** (Bronze → Silver → Gold). The pipeline ingests live trade data from [Finnhub](https://finnhub.io/) via **Kafka**, deserializes Avro payloads using **Confluent Schema Registry**, and produces multi-granularity aggregated views for downstream analysis and AI agent consumption.

---

## Architecture Overview

```
Finnhub WebSocket ──► Kafka (Aiven) ──► Databricks Lakeflow Declarative Pipelines
                                              │
                                    ┌─────────┴──────────┐
                                    ▼                     ▼
                              Bronze Layer          Schema Registry
                             (raw Kafka bytes)       (Avro schema)
                                    │                     │
                                    └─────────┬───────────┘
                                              ▼
                                        Silver Layer
                                    (parsed trade records)
                                              │
                        ┌─────────┬───────────┼───────────┬──────────┐
                        ▼         ▼           ▼           ▼          ▼
                     5-min     30-min      60-min       Daily     Per-Trade
                     OHLCV      Agg         Agg         Agg      Streaming
                                                                   Table
                                     Gold Layer
```

## Tech Stack

| Component | Technology |
|---|---|
| **Streaming Source** | Finnhub WebSocket API |
| **Message Broker** | Apache Kafka (Aiven Cloud) with SASL_SSL + mTLS |
| **Schema Management** | Confluent Schema Registry (Avro) |
| **Pipeline Engine** | Databricks Lakeflow Declarative Pipelines |
| **Processing** | PySpark Structured Streaming, Spark SQL |
| **Storage** | Delta Lake (Streaming Tables + Materialized Views) |
| **Language** | Python, SQL |

## Medallion Architecture

### Bronze Layer — Raw Ingestion

Consumes raw Kafka messages (key, value, offset, partition, timestamp) via Spark Structured Streaming with secure SASL_SSL authentication and TLS certificates.

```python
@dp.table
def finhub_bronze():
    return spark.readStream.format("kafka").options(**options).load()
```

### Silver Layer — Schema-Aware Parsing

Deserializes Avro-encoded trade payloads using the Confluent Schema Registry, producing a clean table of trade events with `symbol`, `price`, `volume`, `timestamp`, and `conditions`.

```python
@dp.table(name="finhub_silver", table_properties={"quality": "silver"})
def finhub_silver():
    return spark.readStream.table("finhub_bronze").select(
        from_avro(data=col("value"), subject=SUBJECT,
                  schemaRegistryAddress=SCHEMA_REGISTRY_URL,
                  options=schema_registry_options).alias("data")
    ).select("data.*")
```

### Gold Layer — Business Aggregations

Multi-granularity aggregated views for analytics:

| Table / View | Type | Description |
|---|---|---|
| `gld_stock_trade` | Streaming Table | Per-trade records clustered by date |
| `gld_stock_trade_5min` | Materialized View | 5-minute VWAP & volume aggregation |
| `gld_stock_trade_30min` | Materialized View | 30-minute trade view |
| `gld_stock_trade_60min` | Materialized View | Hourly price & volume aggregation |
| `gld_stock_trade_day` | Materialized View | Daily OHLC-style summary (avg, max, min) |

## Exploration & Signal Analysis

The exploration notebooks demonstrate advanced institutional trade analysis:

- **VWAP Calculation** — Volume-Weighted Average Price per minute for ISO-condition trades
- **Sliding Window Analysis** — 5-trade rolling VWAP and volume aggregation to detect institutional accumulation patterns
- **Sweep Signal Detection** — Identifies moments where volume surges 2x+ over previous windows, flagging potential institutional sweep orders
- **Visual Analytics** — Matplotlib-based price charts with bullish/bearish sweep signal overlays

## Project Structure

```
stock-trade-agent/
├── README.md
└── stock-trade-etl/
    ├── explorations/
    │   └── sample_exploration.py      # Institutional signal analysis notebook
    ├── transformations/
    │   ├── 01_bronze/
    │   │   └── finhub.py              # Kafka raw ingestion
    │   ├── 02_silver/
    │   │   └── finhub.py              # Avro deserialization via Schema Registry
    │   └── 03_gold/
    │       ├── trade.sql              # Per-trade streaming table
    │       ├── trade_5min.sql         # 5-minute aggregation
    │       ├── trade_30min.sql        # 30-minute aggregation
    │       ├── trade_60min.sql        # 60-minute aggregation
    │       └── trade_day.sql          # Daily aggregation
    └── utilities/
        └── utils.py                   # PySpark UDFs
```

## Key Highlights

- **End-to-end streaming pipeline** — from external WebSocket source through Kafka to curated Delta Lake tables with zero manual orchestration
- **Production-grade security** — SASL_SSL + mTLS authentication for Kafka, authenticated Schema Registry access
- **Declarative pipeline definitions** — leveraging Databricks Lakeflow Declarative Pipelines for automatic dependency resolution and incremental processing
- **Multi-granularity time-series** — aggregated views at 5-min, 30-min, 60-min, and daily intervals for flexible analysis
- **Institutional behavior detection** — exploratory analytics identifying sweep orders, volume surges, and accumulation signals