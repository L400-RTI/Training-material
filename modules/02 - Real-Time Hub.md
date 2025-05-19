# Module 2 - Microsoft Fabric Real-time hub in Microsoft Fabric Real-Time Intelligence

> This module provides a comprehensive module on the architecture, advanced configuration, and optimization of Real-time hub in Microsoft Fabric Real-Time Intelligence.

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

Real-time hub acts as the central surface for discovering, configuring, and routing real-time data across Microsoft Fabric Real-time Intelligence. This module sets the stage for understanding its integration points, performance implications, and usage patterns.

---

## 2. Architectural Deep Dive

Real-time hub operates as the ingestion control plane within Microsoft Fabric’s real-time data architecture. It supports:

- Connecting to **CDC-enabled sources** like Azure SQL DB and SQL Server through Event Hubs or Kafka.
- Bridging ingestion from **source systems** to **real-time consumers** like Eventstream and Eventhouse.
- Working in conjunction with **Azure Event Grid** for ingesting Fabric and Azure system events.

### Connecting to **CDC-enabled sources** like Azure SQL DB and SQL Server through Event Hubs or Kafka

One of the most powerful and enterprise-relevant use cases for Microsoft Fabric Real-time hub is its ability to facilitate low-latency ingestion from change data capture (CDC) enabled databases such as Azure SQL Database and SQL Server. In scenarios where data changes must be reflected in near real-time across analytics, alerting, or operational pipelines, Real-time hub acts as a central integration layer to connect these source systems to downstream analytics platforms like Eventhouse.

#### Why CDC?

Change Data Capture allows systems to track and publish changes—insertions, updates, deletions—in the source database without polling the entire data set. This is critical for reducing load on transactional systems while enabling timely analytics, alerting, or replication.

Real-time hub itself does not extract changes directly from databases. Instead, it integrates seamlessly with modern CDC infrastructure patterns—typically involving connectors like **Debezium**, **Azure Data Factory (ADF)**, or **SQL Server Change Data Capture**—and ingests CDC data via **Azure Event Hubs** or **Apache Kafka**, both of which are natively supported.

#### CDC via Azure Event Hubs

For cloud-first architectures or Microsoft-centric deployments, Azure Event Hubs acts as a reliable ingestion buffer. The typical pipeline looks like this:

1. **CDC Extraction**: A tool like Debezium (running in Azure Container Apps, AKS, or a managed connector service) monitors the transaction logs of an Azure SQL DB or SQL Server instance and captures row-level changes.
2. **Transformation and Serialization**: Debezium serializes changes into structured JSON events that contain metadata like:
   - Operation type (insert/update/delete)
   - Before/after snapshots of the data
   - Timestamps and source metadata (database, schema, table)
3. **Streaming to Event Hub**: These CDC events are published to an Azure Event Hub, partitioned by table or primary key for parallelism.
4. **Ingestion by Real-time hub**: Real-time hub connects to the Event Hub as a streaming source and makes the CDC stream available to downstream consumers like Eventstream or directly to Eventhouse.

This architecture offers high durability, cloud-native scalability, and easy observability via Azure Monitor and Event Hub diagnostics.

#### CDC via Kafka

In hybrid or open-source environments, Apache Kafka is the preferred event backbone. Debezium, originally built for Kafka Connect, is often deployed to stream CDC data from SQL Server, PostgreSQL, MySQL, Oracle, and other systems into Kafka topics.

The architecture with Real-time hub follows a similar pattern:

1. **Debezium in Kafka Connect**: Change data is captured from the source database and published to specific Kafka topics (e.g., `dbserver.inventory.customers`).
2. **Real-time hub Kafka Connector**: Real-time hub connects to the Kafka cluster and subscribes to selected topics, enabling real-time discovery and ingestion.
3. **Downstream Routing**: The messages are routed to Eventstream for transformation/filtering or forwarded directly to Eventhouse for querying and storage.

Kafka offers low-latency, high-throughput capabilities, and guarantees exactly-once semantics when correctly configured, making it ideal for mission-critical ingestion pipelines.

#### Integration Considerations

- **Schema Handling**: CDC streams contain both metadata and payload. Real-time hub supports ingestion of these structured JSON payloads. In Eventhouse, the schema must match the payload’s shape—often requiring the use of KQL update policies to normalize, flatten, or filter fields such as `before`, `after`, and operation metadata (`__op`).
- **Latency**: The combination of Kafka/Event Hubs and Real-time hub enables sub-second end-to-end latency, assuming minimal transformation in Eventstream.
- **Resilience and Replay**: Both Event Hubs and Kafka provide checkpointing and offset-based replays, which Real-time hub respects through its connectors. This ensures that ingestion can resume from the correct position after failure without data loss.
- **Partitioning and Scale-Out**: Real-time hub supports parallel ingestion from multiple Event Hub partitions or Kafka topic partitions. When combined with sharded Eventhouse tables, this enables high-scale ingestion architectures.
- **Security**: Real-time hub supports secure access to Event Hubs and Kafka using managed identities, SAS tokens, or OAuth-based authentication depending on the source configuration.

#### Real-World Example

A logistics company uses Azure SQL Database to manage real-time parcel tracking. Debezium captures status updates (e.g., package picked up, in transit, delivered) and streams them to Azure Event Hubs. Real-time hub ingests these events and routes them to Eventhouse. KQL update policies extract and normalize key metrics like delivery time deltas. A Power BI dashboard (or a real-time dashboard) displays this in near real-time, allowing the operations team to monitor performance and trigger interventions.

### Working in Conjunction with **Azure Event Grid** for Ingesting Fabric and Azure System Events

Real-time hub in Microsoft Fabric offers a strategic capability for ingesting system-level events emitted by both Fabric and Azure services. These are not telemetry from user-defined applications but platform-generated events that signal state changes, health conditions, operational triggers, or resource lifecycles. This system event ingestion is built on top of **Azure Event Grid**, a fully managed event routing service that enables reactive, event-driven patterns across distributed systems.

In this context, Real-time hub provides a powerful interface that surfaces relevant system events for discovery and routing, while Event Grid acts as the under-the-hood backbone delivering those events from their source to consumers like Eventstream, Eventhouse, or Activator.

#### What Are Fabric and Azure System Events?

System events are structured messages automatically emitted by Microsoft Fabric or Azure services to indicate that something of significance has occurred. These include, but are not limited to:

- Dataset refresh completion in Power BI
- Capacity utilization threshold warnings
- Workspace creation, modification, or deletion
- Dataflow failures
- Eventstream deployment status updates

These events are standardized, contain rich context metadata, and follow consistent schemas. For example, a workspace creation event includes workspace ID, creator identity, timestamp, and other useful operational attributes.

From a monitoring and orchestration perspective, these events are critical for building automation, enforcing governance, or triggering data pipelines in response to system changes.

#### Role of Azure Event Grid

Azure Event Grid is the native transport layer for system events in Fabric and Azure. It enables:

- **Event subscription and filtering** based on event type or metadata
- **High-throughput, low-latency delivery**
- **Push-based architecture**—no need for polling
- **Built-in retry, dead-lettering, and diagnostics**

Internally, Fabric uses Event Grid to publish these events into a routing layer. Real-time hub integrates directly with that layer to expose these events to the user and make them available for real-time consumption.

#### Real-time hub as the Ingestion and Control Plane

When users open Real-time hub in Microsoft Fabric, they are presented with a curated interface that includes a category called **Fabric Events** and another called **Azure Events**. These are automatically populated with all the system events that Real-time hub can currently discover and ingest via Event Grid.

From here, users can:

- **Discover available system events** across Fabric and Azure services
- **Enable routing** of selected events to Eventstream for transformation or aggregation
- **Trigger rules** using Activator to invoke actions (e.g., sending Teams alerts, starting pipelines) in response to specific events

This simplifies what has historically been a complex event subscription process. Instead of manually wiring up Event Grid topics, endpoints, and event handlers, users can simply “opt in” to the event categories exposed by Real-time hub and configure routing with a few clicks.

#### Routing Options and Architecture

Once an event source is selected in Real-time hub, it can be routed to:

- **Eventstream**: For transformation, filtering, enrichment, or fan-out to multiple targets
- **Eventhouse (KQL Database)**: For real-time analytics, dashboarding, or historical event tracking
- **Activator**: For rules-based actions such as sending emails, webhooks, or invoking Azure Functions

Each event passes through Real-time hub, which acts as a governance and orchestration layer, ensuring observability, reliability, and decoupled consumption.

Example: A Power BI dataset refresh event might trigger the following:

1. **Event Grid** detects the completion of the refresh.
2. **Real-time hub** ingests the event and forwards it to Eventstream.
3. **Eventstream** filters only the datasets relevant to a department.
4. The filtered event is routed to **Activator**, which then triggers a webhook to notify a reporting system.

#### Current Limitations and Considerations

As of today, the Real-time hub supports a curated set of system events from Fabric and Azure. Not all services are covered, and the granularity of event types may vary.

Additionally:

- Event payloads may require flattening or transformation before ingestion into Eventhouse.
- Consumers must be built to tolerate occasional duplication or delays due to Event Grid retry policies.
- While the Real-time hub abstracts away the Event Grid subscription layer, understanding how Event Grid operates is still beneficial for troubleshooting and optimization.

#### Practical Use Cases in Real-time hub

- **Governance Automation**: Ingest workspace creation events and log them to Eventhouse for auditing.
- **Operational Monitoring**: Track capacity utilization events and generate proactive alerts via Activator.
- **Pipeline Coordination**: Use dataset refresh completion events to trigger dependent transformations or notifications.

---

## 3. Technical Deep Dive

### Ingesting Data with Real-time hub: Sources and Patterns

Real-time hub supports data ingestion from a variety of sources:

- **Change Data Capture (CDC) Ingestion**
- **Streaming Data Sources**
- **System Event Ingestion (Fabric and Azure Events)**
- **File-Based Ingestion (Embedded in Eventhouse)**
- **Pre-Built Sources and Sample Data**

### 1. **Change Data Capture (CDC) Ingestion**

One of the most enterprise-critical capabilities of Real-time hub is its ability to integrate with CDC-enabled databases such as Azure SQL Database, SQL Server, PostgreSQL, and MySQL. While Real-time hub does not perform CDC extraction directly, it serves as the ingestion and routing layer for CDC streams that have been externalized using tools like:

- **Debezium** (running on Kafka Connect or Azure Container Apps)
- **Azure Data Factory**
- **Custom applications writing to Event Hub or Kafka**

These tools monitor transaction logs in source systems and emit change events as structured JSON records. Real-time hub can then ingest these events via supported connectors such as:

- **Azure Event Hubs**
- **Apache Kafka**

Once connected, Real-time hub surfaces these CDC streams and enables routing to downstream consumers like Eventstream or directly to Eventhouse. From there, update policies written in KQL can be applied to manage transformations, filter on operations (insert/update/delete), and flatten nested structures typical of CDC payloads.

**Use case:** A logistics platform streams package status changes from Azure SQL to Real-time hub using Debezium and Event Hubs. Real-time hub forwards the data to Eventhouse, where analysts monitor delivery performance using KQL dashboards.

### 2. **Streaming Data Sources**

Real-time hub provides native support for streaming data ingestion from industry-standard event brokers. This includes:

- **Azure Event Hubs**: A fully managed, scalable event ingestion service. Event Hubs is ideal for telemetry, IoT, CDC, and microservices eventing.
- **Apache Kafka**: A widely used open-source distributed event streaming platform. Real-time hub can connect to Kafka topics using built-in connectors, providing seamless integration for hybrid or on-premise workloads.
- **MQTT**: Lightweight publish-subscribe protocol commonly used in IoT scenarios.
- **Custom HTTP Sources**: Custom applications or services that stream data via HTTP endpoints and are registered in Real-time hub as data sources.

These streaming sources allow for ingestion of high-throughput, low-latency event data. Real-time hub ensures observability and governance over these sources, enabling operations teams to monitor ingestion rates, validate formats, and control downstream flow behavior.

**Use case:** A smart factory uses MQTT to stream sensor data (temperature, vibration, power usage) to Real-time hub. From there, Eventstream applies filters and forwards critical anomalies to Eventhouse for analytics and to Activator for triggering alerts.

### 3. **System Event Ingestion (Fabric and Azure Events)**

Beyond external data streams, Real-time hub supports ingestion of **system-level events** emitted by Fabric and Azure services. These include:

- Power BI dataset refresh events
- Workspace lifecycle events
- Capacity usage events
- Eventstream deployment or failure notifications

These events are routed into Real-time hub using **Azure Event Grid** behind the scenes. From the user’s perspective, Real-time hub surfaces categories like **Fabric Events** and **Azure Events**, allowing simple configuration to route these system events to Eventstream, Activator, or Eventhouse.

This type of ingestion supports automation, observability, and governance without any custom instrumentation.

**Use case:** A data platform team uses Real-time hub to ingest Power BI dataset refresh events and trigger follow-on data quality checks using Activator when refreshes complete.

### 4. **File-Based Ingestion (Embedded in Eventhouse)**

Real-time hub is also embedded into other Fabric surfaces—most notably the **Get Data** wizard in Eventhouse (KQL databases). Here, Real-time hub enables real-time and semi-real-time ingestion from:

- **Local file uploads (CSV, TSV, JSON)**
- **Azure Storage (Blob Containers)**
- **Amazon S3**
- **OneLake file locations**
- **Eventstream** (as a source)
- **Pipelines/Dataflows** shortcuts

The embedded Real-time hub wizard allows users to infer schema, configure mapping policies, and preview data before ingestion. Files are uploaded to a temporary staging area, and Real-time hub coordinates ingestion into the KQL table using the engine’s native ingestion APIs.

This pattern is particularly useful for developers and analysts who want to perform one-time loads or semi-structured ingestion without configuring a pipeline.

**Use case:** A financial analyst uploads a CSV file with daily transactions into a KQL database via Eventhouse’s Get Data UI, which uses Real-time hub behind the scenes to perform the ingestion.

---

### 5. **Pre-Built Sources and Sample Data**

To accelerate adoption, Real-time hub also exposes pre-configured and sample data streams. These streams can be connected with a single click and routed through Eventstream and Eventhouse. This is especially useful in training or POC environments where teams want to validate ingestion logic or test alerting and analytics scenarios before integrating production data.

**Use case:** During a workshop, developers use the package delivery sample stream to build dashboards, define rules in Activator, and practice using KQL on simulated parcel delivery data.

---

## 4. Implementation Guidance

### Working Scenarios:

- **Telemetry ingestion** into Eventhouse with filtering via update policies.
- **Cold storage monitoring** using Activator with correct `changes()` logic.

### Common Failures:

- Filtering in Eventstream for high-frequency events → use Eventhouse instead.
- Misuse of `greater than` in Activator → causes alert spamming.

## Latency vs. Efficiency in Real-time hub: Balancing Act

When architecting solutions with Microsoft Fabric Real-time hub, one of the most critical engineering balances to strike is between **latency** and **efficiency**. These two performance dimensions are often in tension, and misjudging the trade-off can lead to failed expectations, bloated workloads, or user dissatisfaction. The Real-time hub, Eventstream, Eventhouse, and Activator collectively provide the building blocks of responsive data infrastructure—but the responsibility of choosing the right tool at the right point in the pipeline remains with the architect.

The platform is evolving toward a future with stronger schema enforcement, validation logic, and dead-letter handling. However, today’s architecture remains highly flexible, offering both power and risk. Misusing that flexibility—especially when it comes to latency-sensitive ingestion or high-frequency alerting—can derail even well-intended implementations.

Let’s explore this through the lens of two working implementations and two frequent architectural failures that hinge on mismanaging the latency-efficiency trade-off.

---

### Scenario 1: Telemetry Ingestion with Eventhouse Update Policies

Consider a use case where high-volume telemetry is streamed from industrial equipment into Eventhouse via Real-time hub. These events contain detailed metrics—temperatures, voltages, gear states—emitted multiple times per second per device. If the goal is to generate alerts or derive summaries based on these metrics, efficiency becomes paramount. The telemetry is consistent and voluminous, so routing through Eventstream for filtering could seem intuitive. But this is a misstep if latency is not the primary concern.

Instead, the correct approach is to ingest the raw stream directly into Eventhouse and apply **KQL update policies** for filtering, transformation, and projection. These policies are applied post-ingestion, ensuring that data arrives quickly and transformations are handled with the optimized performance of the Kusto engine.

This architecture respects the latency-efficiency boundary: by not interrupting the data at the streaming layer, you achieve minimal latency ingestion, and by doing the filtering in a columnar store optimized for batch transformations, you gain efficiency and cost control.

---

### Scenario 2: Cold Storage Monitoring with Activator

In a separate domain, consider cold storage monitoring for a food logistics company. Temperature sensors from 10 warehouses send data every 30 seconds. If a freezer fails, the temperature may rise above threshold levels for an extended time, during which an alert should be sent—**once**.

Here, latency is not the dominant concern; instead, **alerting precision and efficiency** matter more. A common mistake is using an Activator rule with a `greater than` condition: for instance, `temperature > 5°C`. While this is syntactically valid, it creates a storm of repeated alerts as long as the condition is true. Users are spammed until the temperature drops again.

The correct approach is to use the `changes()` function. This monitors for state transitions—i.e., when the temperature first exceeds the threshold—and suppresses alerts for static conditions. This design ensures that **efficiency is not just about CPU cycles—it’s about human attention**. And in this case, latency is only relevant at the point of condition change, not at every data point.

---

### Failure 1: Filtering in Eventstream for High-Frequency Events

A common failure pattern is attempting to perform pre-ingestion filtering in Eventstream for high-frequency data like telemetry or log ingestion. The interface makes it tempting: define a filter, route the filtered data to Eventhouse, and visualize.

But the Eventstream engine is not optimized for heavy real-time filtering at extreme throughput. This introduces latency, especially when multiple conditions are evaluated on high-cardinality streams. Moreover, filtering too early can eliminate context needed downstream—like comparing a metric’s previous value to its current one.

Instead, the better architecture is to **stream everything into Eventhouse and filter there**. Eventhouse is designed for large-scale ingestion with real-time query capability. Its KQL update policies can be used to evaluate conditional logic, compute deltas, and store clean results efficiently. This is the proper tool for the job when latency at the point of ingestion is more important than transformation latency.

---

### Failure 2: Misuse of Comparison Operators in Activator

In real-world deployments, teams often treat Activator as a traditional rules engine, writing expressions like `value > threshold` and expecting a single alert. As shown in the cold storage scenario, this leads to performance issues—not in system throughput, but in **alert volume and user fatigue**.

This is a misunderstanding of how event conditions should be modeled in an event-driven architecture. The `changes()` function is specifically designed to distinguish **state transitions** from **continuous conditions**, transforming Activator from a naïve alert dispatcher into a precise signal generator.

Using `changes()` is not just syntactically correct; it is architecturally aligned with the concept of **edge detection**, not level detection. That’s the key to balancing latency (respond immediately to the first crossing) with efficiency (avoid flooding the system or user).

---

### Conclusion

Latency and efficiency are not features—they are design outcomes. Filtering in the wrong place or alerting on the wrong condition undermines system performance and user trust. As the platform matures, schema-first design and more prescriptive pipelines will support better defaults. Until then, thoughtful architecture—respecting the right stages for each operation—is how successful real-time systems are built.

In this module, you've seen the difference between filtering too early versus transforming at scale, and the impact of getting edge-triggering right in Activator. These insights are not just performance optimizations—they’re critical to delivering Real-time Intelligence solutions that are fast, scalable, and maintainable.

---

## 5. Troubleshooting

This section outlines recurring misconfigurations and architectural missteps encountered in Real-time hub implementations. These issues often arise from incorrect assumptions about where logic should live in the pipeline—especially under performance constraints.

### Common Issues and Solutions

| **Problem**                    | **Cause**                                                                                         | **Recommended Resolution**                                                                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Missing schema inference**   | CSV files with nested headers, inconsistent column counts, or type ambiguity                      | Define schema manually in the Get Data wizard using KQL mapping. Avoid relying on auto-inference for multi-line headers or semi-structured data.     |
| **High latency in dashboards** | Eventstream is performing filtering or transformation on high-frequency streams (e.g., telemetry) | Ingest raw events directly into Eventhouse. Apply transformation logic using KQL update policies, which are optimized for batch evaluation at scale. |
| **Excess alerts in Activator** | Alert logic uses continuous comparisons like `value > threshold`, which re-trigger on every input | Use `changes()` to detect state transitions instead of level comparisons. Add cooldown logic to avoid repeat alerts during static violations.        |

### Deeper Guidance

#### Schema Inference Failures

Real-time hub supports schema inference primarily for flat, single-header CSV files. It struggles with:

- Multiple header rows
- Irregular or malformed data rows
- Fields with inconsistent types (e.g., string vs. numeric)

**Best Practice**: Manually define ingestion mappings using the schema editor in Eventhouse. Explicit column mappings provide better resilience and reusability across ingestion flows.

#### Eventstream Filtering Bottlenecks

Eventstream is optimized for routing and minor enrichment—not for complex filtering of high-cardinality or high-throughput streams. Applying filters directly in Eventstream can introduce substantial latency, especially for continuous telemetry sources.

**Recommended Pattern**:

- Route unfiltered data through Eventstream into Eventhouse.
- Perform filtering and transformation via KQL update policies post-ingestion.
- Leverage Eventhouse’s native performance and scaling model.

#### Activator Alert Volume

A common anti-pattern in Activator usage is level-based evaluation (`value > threshold`) without edge detection logic. This leads to repeated alerts while the condition remains true—wasting compute, alert bandwidth, and user attention.

**Best Practice**: Use `changes()` to detect threshold crossings (i.e., when the condition becomes true). Combine with cooldown logic or state-based suppression to prevent excessive alerting when values remain in violation.

---

### Monitoring + Triage

- Use **Real-time hub’s ingestion diagnostics** to track data volume, event lag, and connector health.
- Analyze **Eventstream metrics** to identify performance degradation from rule overload or skewed partitions.
- Review **Activator evaluation logs** to diagnose rule churn, alert frequency, and state transitions.
- Use **Azure Monitor** and **Log Analytics** to aggregate telemetry from Real-time hub, Eventstream, and Eventhouse for end-to-end observability.

---

## 6. Orchestration and Optimization

- **Stream to Store, Transform at Rest**: Route raw data streams through Real-time hub into Eventhouse and perform business logic using KQL update policies. This decouples ingestion from transformation, improving both scalability and query latency.

- **Minimize Logic in Eventstream**: Use Eventstream for lightweight operations such as routing, reshaping, or basic filtering—not for complex joins or rule evaluation. This preserves throughput and reduces transformation bottlenecks.

- **Use Activator for Event-Driven Actions Only**: Limit Activator usage to state transitions or control signals. Avoid using it as a processing engine—delegate filtering, aggregation, and evaluation to Eventhouse or Eventstream where appropriate.

- **Partition Strategically**: For high-volume sources like Kafka or Event Hubs, ensure partitioning aligns with logical workload boundaries (e.g., device ID, tenant ID) to prevent data skew and maximize parallelism across ingestion and query workloads.

- **Monitor Lag and Policy Latency**: Continuously monitor Real-time hub ingestion lag, Eventstream throughput, and Eventhouse update policy latency. Use this telemetry to tune ingestion batch sizes, adjust rule complexity, or scale out resource allocations.

---

## 7. Schemas and Throughput

- Leverage inferred schema for rapid onboarding.
- Use `create table` + `create ingestion mapping` for complex pipelines.
- Optimize ingestion throughput using:
  - Sharding
  - Parallelism
  - Staging blob uploads (via Get Data Wizard)

### Schemas and Throughput Deep Dive

# Schemas and Throughput Optimization in Real-time hub

Ingesting real-time data at enterprise scale requires more than just configuring connections and tables—it demands an intentional strategy around **schema management**, **data routing**, and **throughput optimization**. Real-time hub in Microsoft Fabric Real-Time Intelligence provides flexible schema tools and ingestion primitives that support both fast onboarding and high-performance stream processing. This section explores how advanced practitioners can leverage inferred schemas for agility, define ingestion mappings for robustness, and apply architectural techniques like sharding, parallelism, and staging uploads to maximize ingestion throughput.

---

## Leverage Inferred Schema for Rapid Onboarding

The fastest way to begin ingesting data in Real-time hub is through **schema inference**, which automatically detects column structure and data types from sample input files. This capability is built directly into the **Get Data Wizard**, allowing users to upload CSV, JSON, or Parquet files and have the engine generate a corresponding table schema without manual intervention.

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

Once the schema is locked down and mappings are defined, the next focus is performance—ensuring Real-time hub can ingest and process data at scale. Fabric’s ingestion engine (powered by the Kusto engine and the DM service) supports several strategies to maximize throughput and resilience:

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

### Scenario: Real-Time Parcel Delivery Monitoring

**Objectives**:

- Ingest CSV-based delivery telemetry using the Get Data Wizard.
- Route real-time parcel data into Eventhouse.
- Apply update policies to segment event types (e.g., delivery status, truck location).
- Use Activator to detect changes in delivery status.
- Trigger a Power Automate flow when a package is delayed or marked as failed delivery.

### Steps:

1. Upload two CSV files simulating delivery truck telemetry and parcel delivery status to a new KQL DB using the Get Data Wizard.
2. Define ingestion mappings to reflect the schema (e.g., `parcel_id`, `status`, `location`, `timestamp`).
3. Set up a Real-time hub connection via Eventstream to forward telemetry from an Event Hub or simulated stream.
4. Implement KQL update policies in Eventhouse to separate and enrich data by event type (e.g., truck movement vs. delivery status updates).
5. Configure Activator to alert when a parcel status changes to `delayed` or `failed`. Integrate with Power Automate to notify the logistics team.

---
