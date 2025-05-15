# Module 2 - Microsoft Fabric Real-time Hub in Microsoft Fabric Real-Time Intelligence

> This module provides a comprehensive module on the architecture, advanced configuration, and optimization of Real-time Hub in Microsoft Fabric Real-Time Intelligence.

---

## Table of Contents

1. [Introduction to the Module](#1-introduction-to-the-module)
2. [Architectural Deep Dive](#2-architectural-deep-dive)
3. [Technical Deep Dive](#3-technical-deep-dive)
4. [Implementations](#4-implementations)
5. [Troubleshooting](#5-troubleshooting)
6. [Orchestration and Optimization](#6-orchestration-and-optimization)
7. [Schemas and Throughput](#7-schemas-and-throughput)
8. [Monitoring and Pricing](#8-monitoring-and-pricing)
9. [Hands-on Lab](#9-hands-on-lab)

---

## 1. Introduction to the Module

Real-time Hub acts as the central surface for discovering, configuring, and routing real-time data across Microsoft Fabric Real-time Intelligence. This module sets the stage for understanding its integration points, performance implications, and usage patterns.

---

## 2. Architectural Deep Dive

### Key Components:

- **Event Ingestion**: Azure Event Hubs, OneLake, S3, local files.
- **Real-time Routing**: To Eventstream, Eventhouse, Activator.
- **Execution Layer**: Kusto Engine and Data Management Service (DM).

## Execution Layer Deep Dive

## Kusto Engine and Data Management Service (DM)

The execution layer of Microsoft Fabric’s Real-time Hub underpins the system’s ability to handle high-volume, low-latency data ingestion with enterprise-grade scalability. This layer is powered by two foundational services inherited and evolved from Azure Data Explorer (ADX): the Kusto Engine and the Data Management (DM) Service. Understanding their roles, orchestration, and operational mechanics is crucial to designing performant and reliable Real-Time Intelligence solutions.

## Kusto Engine: The Analytical Core

At the heart of the execution layer lies the Kusto Engine, an advanced, distributed query and ingestion engine designed to handle real-time analytics workloads. It is the same core technology that powers Azure Data Explorer, but in Fabric, it has been extended and integrated to support broader orchestration scenarios.

The Kusto Engine is optimized for time-series and event data and is responsible for parsing, transforming, and ingesting data into KQL databases (Eventhouse). When a stream or file lands in Fabric via the Real-time Hub, the Kusto Engine performs several key operations:

- **Schema Inference**: When using tools like the Get Data Wizard, the engine examines sample data to infer the schema automatically. This is especially useful in ad hoc or semi-structured environments where upstream schema enforcement is minimal.

- **Ingestion Mapping**: The engine uses ingestion mapping definitions—JSON-based or KQL-declared—to correlate raw data fields to structured table schemas. This ensures both consistency and flexibility across ingestion pipelines.

- **Update Policies Execution**: For scenarios that require transformation or Partitioning (e.g., splitting telemetry into multiple tables), the Kusto Engine executes update policies in near real time. This allows for lightweight, declarative stream processing without the need for additional compute layers.

- **Query Execution**: After ingestion, the same engine supports ultra-fast query performance across vast amounts of streaming and historical data. This dual-purpose design—serving both ingestion and analytical querying—eliminates latency layers between processing and insight.

The Kusto Engine operates with high concurrency and supports aggressive compression and indexing strategies. These features are largely abstracted from the user, but they manifest in the system’s ability to ingest millions of events per second and query them with sub-second latency.

## Data Management (DM) Service: Ingestion Coordination and Reliability

Complementing the Kusto Engine is the Data Management Service, often referred to simply as “DM.” If the Kusto Engine is the analytics core, DM is the logistics backbone—responsible for coordinating ingestion operations, ensuring reliability, and managing the data pipeline lifecycle.

DM serves several crucial roles:

- **Buffering and Batching**: DM receives raw input data from sources configured in Real-time Hub—whether those are files, streaming connectors, or system events. It buffers and batches this data before handing it off to the Kusto Engine for ingestion. This allows for improved throughput and reduced latency, especially in burst scenarios.

- **Routing and Load Distribution**: DM intelligently distributes ingestion tasks across available engine nodes. For enterprise deployments with high concurrency and multiple databases, this ensures optimal resource utilization and avoids hotspot scenarios.

- **Retry and Error Management**: In cases where ingestion fails—due to schema mismatches, mapping errors, or transient platform issues—DM implements retry policies and surfaces detailed diagnostics to the user via the Fabric monitoring tools. This minimizes data loss and provides transparency for troubleshooting.

- **Connection to Staging Area**: When users upload files through the Get Data Wizard, the data is temporarily stored in a secure, Fabric-managed staging area (staging blob). DM manages the secure transfer of this staged data to the engine. This process is seamless to users, but it's critical to the success of large-scale or multi-part ingestion scenarios.

- **Ingestion Throttling and Protection**: To ensure system stability, DM enforces quotas and throttles ingestion where necessary. For example, if a workspace exceeds predefined limits or a pipeline initiates an excessive number of ingestion attempts, DM will defer processing and emit warnings. This protects shared infrastructure and ensures quality of service across tenants.

## Kusto + DM: Carefully Coordinated

The power of the execution layer lies in the tight coupling and orchestrated flow between Kusto and DM. Data ingested through Real-time Hub doesn’t simply pass through a single monolithic pipe. Instead, it follows a carefully managed pipeline:

- **Source Connection**: Real-time Hub receives a stream or file and registers it.
- **Staging and Batching**: DM buffers, stages, and optionally transforms the data.
- **Schema Handling**: Kusto infers schema (or applies pre-configured mappings).
- **Ingestion Execution**: DM coordinates ingestion into KQL tables via the engine.
- **Post-ingestion Logic**: Update policies (if configured) are executed.
- **Query Availability**: The data becomes immediately available for querying in Eventhouse or downstream via dashboards and notebooks.

This pipeline is elastic, scalable, and largely automated—but it exposes hooks for expert users to tune behavior via KQL mappings, ingestion propeReal-Time Intelligencees, and routing rules.

## Design Implications for Architects

For architects and engineers working on enterprise-grade Real-Time Intelligence solutions, understanding the Kusto-DM dynamic is essential. Decisions about schema design, ingestion frequency, mapping granularity, and update policy complexity all impact engine load and DM throughput.

**Best practices include:**

- Predefine schemas and mappings where possible to avoid real-time inference overhead.
- Use update policies judiciously; chain transformations only when needed.
- Monitor ingestion metrics and capacity events to tune pipeline performance.

### Design Principles:

- Decoupled ingestion and consumption.
- Declarative routing via Fabric UI.
- Powered by Azure Event Grid for system events.

---

## 3. Technical Deep Dive

### Connector Types:

- **Native**: Event Hubs, Amazon S3, Azure Storage.
- **Fabric-native**: Pipelines, Eventstream, Embedded Real-time Hub in Get Data.
- **System Events**: Fabric + Azure services via Event Grid.

### Advanced Features:

- Embedded schema inference engine.
- Ingestion mapping with visual and KQL support.
- Get Data Wizard: integrated view of streaming + static sources.

### Advanceed Features Deep Dive

# Advanced Features of Real-time Hub in Microsoft Fabric Real-Time Intelligence

The Real-time Hub in Microsoft Fabric Real-time Intelligence (Real-Time Intelligence) offers a streamlined yet sophisticated surface for connecting data sources, managing real-time data flows, and orchestrating ingestion across the broader Fabric platform. At Level 400/500, it's essential to understand not just how to connect data, but how Real-time Hub intelligently adapts to complex and variable datasets through **schema inference**, **ingestion mapping**, and the **Get Data Wizard**. These advanced features play a pivotal role in unlocking usability, performance, and extensibility.

---

## Embedded Schema Inference Engine

One of the most powerful and often underappreciated components of Real-time Hub is its **schema inference engine**, embedded within the data onboarding workflows. At a high level, schema inference refers to the automatic deduction of a table’s structure—columns, types, and relationships—based on a sample of incoming data. In the context of Microsoft Fabric, this capability is built directly into the ingestion path, particulary when using tools like the Get Data Wizard or Real-time Hub-integrated workflows.

### How It Works

When a user selects or uploads a data file (e.g., CSV, JSON, or Parquet), the Real-time Hub stages that file and runs a lightweight inference process over its contents. The engine identifies:

- Column headers and names
- Data types (int, datetime, string, etc.)
- Column order
- Formatting irregularities (e.g., delimiters, quoting)

If multiple files are uploaded at once, the engine allows the user to select a _representative sample_ for schema inference. This is crucial in scenarios where batch files may vary slightly in structure. Once inferred, the schema is shown to the user for validation and optionally edited before ingestion.

### Benefits

- **Speed**: Users can go from file to live ingestion in minutes without manually writing table definitions.
- **Reduced friction**: Schema inference enables non-expert users (e.g., data analysts) to participate in ingestion workflows.
- **Consistency**: Inferred schemas can be reused and promoted to shared ingestion pipelines.

### Considerations for Advanced Users

While schema inference accelerates development, it’s not foolproof. Enterprises should:

- Validate inferred schemas before applying them in production.
- Use schema locking or custom mappings to enforce governance.
- Prefer explicitly defined schemas for mission-critical or frequently changing datasets.

---

## Ingestion Mapping with Visual and KQL Support

After schema inference, or in cases where the schema is already known, Real-time Hub enables precise control over **ingestion mapping**. Mapping defines how incoming fields are routed to columns in a target KQL table and how transformations (e.g., parsing or casting) are applied during ingestion.

### Visual Mapping Interface

For users working through Fabric’s GUI (e.g., via Get Data), a visual interface is provided to configure mappings without writing code. This includes:

- **Drag-and-drop field assignment** from source data to table schema
- **Preview of transformations and type conversions**
- **Built-in format recognition** (CSV, JSON, AVRO)

Users can select from existing ingestion mappings or create a new one during the ingestion flow. Each mapping is versioned and can be saved for reuse.

### KQL-Based Mapping

For advanced users or scenarios that require granular control, ingestion mappings can be authored and deployed using Kusto Query Language (KQL). The syntax supports formats such as:

```kusto
.create table MyTable ingestion csv mapping "MyMapping"
[
  {"column":"timestamp", "datatype":"datetime", "ordinal":0},
  {"column":"temperature", "datatype":"real", "ordinal":1},
  {"column":"deviceId", "datatype":"string", "ordinal":2}
]
```

Mappings can also specify transformations, default values, and optional propeReal-Time Intelligencees. When authored via KQL, these mappings can be version-controlled, included in deployment scripts, or parameterized via DevOps pipelines.

---

## Operational Advantages

- **Explicit lineage**: Mapping declarations provide transparency and reproducibility.
- **Pipeline stability**: Prevents schema drift or malformed records from polluting target tables.
- **Compatibility with update policies**: Mappings can feed into Eventhouse policies for continuous transformation or filtering.

---

## Best Practices

- Always name mappings clearly using a convention (e.g., `table_format_v1`) for traceability.
- Store mappings centrally and promote shared use across pipelines.
- Test new mappings on sample datasets before promoting to production ingestion.

---

## Get Data Wizard: Integrated Streaming + Static Ingestion

The **Get Data Wizard** acts as the primary interface for onboarding data into Eventhouse via Real-time Hub. It abstracts complexity without hiding power—bringing together streaming, batch, and file-based ingestion into a unified interface.

---

### Entry Point for Practitioners

Found within the KQL database view (Eventhouse), the Get Data Wizard is designed to onboard data in three common scenarios:

- **Upload from local files**
- **Connect to streaming sources** (e.g., Event Hubs, Eventstream)
- **Browse OneLake or cataloged datasets**

This makes it a foundational tool for both prototyping and production ingestion workflows.

---

### Real-time Hub Integration

The wizard seamlessly integrates **Real-time Hub** as a source selector. Users can browse available streams registered in the hub and ingest them directly into their KQL tables. The integration includes:

- **Schema previews** from live stream samples
- **Ingestion mapping setup**
- **Inline schema editing**

For real-time data, this streamlines routing telemetry or events from Eventstream to Eventhouse with just a few clicks.

---

### Strategic Value

- **Unifies ingestion paths**: No need to distinguish batch vs. stream at the tooling level.
- **Low-code onboarding**: Ideal for self-service and departmental usage.
- **Accelerates prototype-to-production**: Streamlined flow from data sample to operational table.

---

## 4. Implementations

### Working Scenarios:

- **Telemetry ingestion** into Eventhouse with filtering via update policies.
- **Cold storage monitoring** using Activator with correct `changes()` logic.

### Common Failures:

- Filtering in Eventstream for high-frequency events → use Eventhouse instead.
- Misuse of `greater than` in Activator → causes alert spamming.

---

## 5. Troubleshooting

| Problem                    | Cause                          | Solution                            |
| -------------------------- | ------------------------------ | ----------------------------------- |
| Missing schema inference   | Complex CSV structure          | Use KQL mapping manually            |
| High latency in dashboards | Overloaded Eventstream filters | Shift filtering to Eventhouse       |
| Excess alerts in Activator | Improper conditions            | Use `changes()` and cool-down logic |

---

## 6. Orchestration and Optimization

- Use Eventhouse update policies to reduce processing load.
- Route mission-critical events through Activator for stateful alerting.
- Apply selective ingestion using routing filters in Real-time Hub.
- Consolidate mappings to avoid ingestion redundancy.

---

## 7. Schemas and Throughput

- Leverage inferred schema for rapid onboarding.
- Use `create table` + `create ingestion mapping` for complex pipelines.
- Optimize ingestion throughput using:
  - Sharding
  - Parallelism
  - Staging blob uploads (via Get Data Wizard)

### Schemas and Throughput Deep Dive

# Schemas and Throughput Optimization in Real-time Hub

Ingesting real-time data at enterprise scale requires more than just configuring connections and tables—it demands an intentional strategy around **schema management**, **data routing**, and **throughput optimization**. Real-time Hub in Microsoft Fabric Real-Time Intelligence provides flexible schema tools and ingestion primitives that support both fast onboarding and high-performance stream processing. This section explores how advanced practitioners can leverage inferred schemas for agility, define ingestion mappings for robustness, and apply architectural techniques like sharding, parallelism, and staging uploads to maximize ingestion throughput.

---

## Leverage Inferred Schema for Rapid Onboarding

The fastest way to begin ingesting data in Real-time Hub is through **schema inference**, which automatically detects column structure and data types from sample input files. This capability is built directly into the **Get Data Wizard**, allowing users to upload CSV, JSON, or Parquet files and have the engine generate a corresponding table schema without manual intervention.

### Why It Matters

In enterprise data onboarding scenarios—especially during proof-of-concept or initial prototyping phases—teams often don’t have complete schema documentation. The ability to infer schema on-the-fly accelerates experimentation, supports iterative development, and reduces time-to-insight. Users can select one or more representative files, view the inferred schema, and confirm or modify column definitions before proceeding with ingestion.

Use cases include:

- Ad hoc analytics for sensor or log data
- Streamlined onboarding of business-unit owned data
- First-time integration of third-party datasets

### Caveats and Guidance

While inference is powerful, it has limitations. For mission-critical pipelines, teams should:

- Validate inferred types against known business rules (e.g., datetime vs. string ambiguities)
- Apply type overrides for fields with inconsistent formatting
- Eventually transition from inferred to explicitly defined schemas and ingestion mappings

---

## Use `create table` + `create ingestion mapping` for Complex Pipelines

As real-time pipelines move from prototype to production, schema management must transition from reactive to intentional. This is where **explicit table creation** and **KQL-based ingestion mappings** become essential.

### Explicit Schema Definition

Using `create table` in KQL allows teams to precisely control:

- Column names and data types
- Table Partitioning and retention policies
- Governance over changes (e.g., schema versioning)

```kusto
.create table SensorData (
    Timestamp: datetime,
    Temperature: real,
    DeviceId: string
)
```

This table becomes the anchor for ingestion pipelines and can be referenced across environments and automation frameworks.

## Ingestion Mapping

After defining a table, ingestion mappings define how incoming data (structured or semi-structured) maps to that table. These mappings specify:

- **Field positions or names**
- **Type coercion rules**
- **Defaults for missing or null values**

```kusto
.create table SensorData ingestion csv mapping "csvMap1"
[
    { "column": "Timestamp", "datatype": "datetime", "ordinal": 0 },
    { "column": "Temperature", "datatype": "real", "ordinal": 1 },
    { "column": "DeviceId", "datatype": "string", "ordinal": 2 }
]
```

Mappings ensure ingestion consistency and act as a contract between source systems and the KQL table.

## Best Practices Include:

- **Reuse and version mappings**
- **Incorporate them into deployment scripts**
- **Parameterize via DevOps pipelines**

---

## Optimize Ingestion Throughput

Once the schema is locked down and mappings are defined, the next focus is performance—ensuring Real-time Hub can ingest and process data at scale. Fabric’s ingestion engine (powered by the Kusto engine and the DM service) supports several strategies to maximize throughput and resilience:

---

### 1. Sharding

**Sharding** divides large datasets into smaller, more manageable pieces based on a logical key—such as device ID, region, or timestamp. When implemented at the source level, this enables ingestion services to process data concurrently, reducing bottlenecks.

**Use cases include:**

- Uploading large CSVs or JSON blobs
- Parallel ingest from many Event Hubs or Kafka partitions
- Reducing contention on high-throughput KQL tables

---

### 2. Parallelism

Fabric Real-Time Intelligence supports **parallel ingestion pipelines** at both ingestion and query layers:

- Use multiple ingestion sources (e.g., Event Hub partitions)
- Batch multiple files or blobs
- Distribute ingestion using update policies and mappings

The ingestion engine handles multithreaded scheduling, improving throughput while maintaining consistency.

---

### 3. Staging Blob Uploads (via Get Data Wizard)

Files uploaded through the Get Data Wizard are staged in secure blob storage before ingestion begins. This **staging layer** enables:

- **Asynchronous uploads** decoupled from ingestion
- **Scalable buffering** for large or bursty workloads
- **Retry logic** for resiliency

This process is abstracted from the user but is essential for large-scale or batch ingestion scenarios.

---

### Summary

Designing high-throughput, real-time ingestion pipelines in Microsoft Fabric Real-Time Intelligence requires a balance of agility, precision, and scale. Practitioners can begin with schema inference for quick wins, then transition to explicit table and mapping definitions for operational maturity. Performance can be tuned using architectural strategies such as sharding and parallel ingestion, while Fabric’s managed infrastructure—like staging blob uploads—ensures resilience under load.

---

## 8. Monitoring and Pricing

### Monitoring:

- Use Activator for anomaly detection.
- Analyze ingestion logs and failures from Event Grid.

### Pricing Considerations:

- Ingestion volume and frequency drive costs.
- Activator executions metered by action triggers.
- Minimize TCO by optimizing stream routing logic.

---

## 9. Hands-on Lab Example

### Scenario: IoT Vehicle Telemetry Routing

**Objectives**:

- Ingest CSV telemetry via Get Data Wizard.
- Route data to Eventhouse.
- Apply update policies to split stream.
- Use Activator to detect gear change events.
- Trigger Power Automate flow when anomaly is detected.

### Steps:

1. Upload two CSV files to a new KQL DB using Get Data.
2. Configure ingestion mapping and preview schema.
3. Set up Real-time Hub connection via Eventstream.
4. Use Eventhouse update policies to split by telemetry type.
5. Configure Activator to alert when `gear` changes.

---

## 📎 Resources

- [Microsoft Fabric Real-time Intelligence Documentation](https://learn.microsoft.com/fabric)
- [Azure Event Grid Docs](https://learn.microsoft.com/azure/event-grid/)
- [Kusto Query Language Reference](https://learn.microsoft.com/azure/data-explorer/kusto/query/)

---
