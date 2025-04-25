## Module 5 - Data modelling

### Introduction

In the landscape of real-time analytics, the fidelity and flexibility of your data model can be the decisive factor between a scalable solution and a bottlenecked architecture. This module focuses on the advanced practices of data modeling within the Microsoft Fabric Real-Time Intelligence platform, enabling precise, performant, and production-grade implementations.

Real-time systems differ fundamentally from traditional Business Intelligence Systems. They must ingest, transform and serve analytical insights with sub-minute latency—often against massive, high-cardinality, high-granular datasets. This requires a new class of modeling techniques tailored to streaming-first architectures.

This module delivers expert-level guidance on structuring data for streaming and hybrid workloads in Fabric’s KQL-based ecosystem, especially Eventhouse and KQL Database. It bridges theory and implementation through deep dives into update policies, materialized views and external tables, alongside schema strategies for performant Power BI Reports. These concepts are foundational to driving low-latency queries, minimizing compute cost and supporting downstream consumers like dashboards and alerting systems.

#### Business Value

This module is designed for architects, data engineers, and advanced BI professionals who are:

- Designing real-time intelligence systems in production,
- Troubleshooting high-latency or high-cost query workloads,
- Building Power BI semantic models directly over streaming or near real-time KQL data sources,
- Working with complex schema evolution, externalized data references, and time-sensitive joins.

By mastering these advanced techniques, participants will avoid common pitfalls — like improper caching policies, poorly scoped materializations, or inefficient joins - that we’ve seen derail real-world RTI implementations.

### Architectural deep dive

Data modeling in Microsoft Fabric’s Real-Time Intelligence (RTI) must be aligned with the architecture of Eventhouse, KQL Database, and the broader Fabric ecosystem. This section provides a blueprint for how real-time models are constructed in a high-concurrency, high-throughput architecture.

#### Fabric RTI Architectural Context

At the core of the RTI stack lies Eventhouse, a KQL-based data service optimized for high-frequency, time-series data. Eventhouse ingestion scales elastically, and data is indexed on ingest, partitioned, and stored in compressed extents for optimal query performance.

Data models in this environment are not just schemas — they are performance-critical assets. Modeling decisions directly affect:

- Costs (in terms of compute and latency),
- Query plan efficiency (especially under load),
- Retention policy tuning, and
- Downstream semantic model fidelity that can be used by Power BI.

#### Key Architectural Components for Modeling

##### 1. Datatypes

Datatypes in Microsoft Fabric RTI are foundational to data modeling. They define not only how data is stored and queried in KQL-based services like Eventhouse, but also how efficiently that data is joined, filtered, compressed, and consumed downstream (e.g., in Power BI). From an architectural perspective, datatypes:

- Determine compression strategy and extent shaping, impacting storage efficiency and query scan times.
- Affect join behavior and broadcast strategies in large distributed queries.
- Shape the semantic layer compatibility, especially for time-based models and dynamic data.
- Influence update policy and materialized view design, since transformations must respect and preserve type semantics.

In Real-Time Intelligence solutions, incorrect or inconsistent type usage - particularly with `datetime`, `timespan`, or `dynamic` can lead to performance degradation, broken filters in Power BI, and failed ingestion operations.

##### 2. Update Policies

Update policies are executed during ingestion time. They transform or enrich data as it lands and project it into derived tables. From an architectural perspective, this enables:

- Schema simplification at query time
- Filtering
- Normalization (e.g., from wide raw logs to fact/dimension schemas),
- Transformations, extracting columns
- Forking a source to several target tables

Update policies are executed synchronously at ingest, so they affect ingestion latency and capacity. Therefore, they must be lean, deterministic, and designed with ingestion slot constraints in mind.

##### 3. Materialized Views

Materialized views provide pre-aggregated views of a source table. They are defined over a single source table, with single summarize statement. They have a well defined schema and can be queried, just like any other table or function in the database. They exist as physically stored datasets and are automatically updated in the background. In architecture, they serve as:

- Query acceleration layers for common query patterns (e.g., arg_max per session, count by 15-minute bins),
- Mechanisms to reduce cost per query by offloading work from interactive query time,
- Foundations for Power BI models where freshness of the semantic model is bound to the materialization frequency.

They can be used for

- Downsampling

```kql
T
| summarize count() by bin(Timestamp, 1d))
```

```kql
T
| summarize dcount(User), avg(Duration) by bin(Timestamp, 1h))
```

- Last entity by update time

```kql
T
| summarize arg_max(Timestmap, *) by Id
```

- De-Duplication

```kql
T
| summarize take_any(*) by Dimension1, Dimension2…DimensionN
```

The internal materialized view architecture includes delta tracking and cursor-based processing, allowing the system to maintain freshness without reprocessing the full dataset. Query-time joins against MVs are optimized through filter pushdown and rewrite rules.

Although materialized views are a handy tool to reduce query time and pre-calculate you should not have too many of them because multi-tenancy is required. Always think about if it would be possible to replace a materialized view by a real table and an update policy.

##### 3. External Tables

External tables expose datasets that reside in external storage (ADLS, Blob, SQL) or OneLake, allowing you to query operational data without ingesting it. From an architectural perspective, this:

- Enables schema-on-read for low-frequency or archival datasets,
- Supports cross-system joins (e.g., enrichment from dimension data in SQL),
- Reduces storage cost by eliminating unnecessary ingestion.

Partition pruning and pre-filtering play a critical role in maintaining performance. Effective modeling requires aligning the external table’s path structure with likely filter predicates.

##### 4. Partitioning Policies

Partitioning policies define how extents (immutable data shards) are organized post-ingestion to optimize query performance. From an architectural perspective, this:

- Enables partition pruning by datetime or high-cardinality string keys (e.g., TenantId, AccountId),
- Reduces data movement across nodes in distributed queries and joins,
- Improves compression and caching efficiency for time-series and multi-tenant scenarios.

Policies can be configured to assign partitioned extents using `ByPartition` (co-location on same node) or `Uniform` (balanced distribution). Effective modeling requires aligning the partition key with common filter patterns and join conditions.

##### 5. Modeling for Power BI

Power BI semantic models built atop KQL-Databases must accommodate latency, freshness, and cardinality. Key architectural considerations include:

- Using star schemas over flat tables to improve slicer/filter efficiency,
- Ensuring dimension tables are set to Dual mode when feasible to reduce joins on Direct Query paths,
- Modeling datetime fields for efficient filtering (e.g., via time rounding or calendar relationships),
- Using KQL functions as semantic objects for reuse and clarity.

Semantic models should be architected with DirectQuery for the fact tables and dual mode for the dimension tables to balance performance with real-time accuracy.

##### 6. OneLake Availibility

OneLake plays a pivotal role in unifying data access across Microsoft Fabric, enabling seamless integration of streaming data with analytical and operational workloads. In the context of Real-Time Intelligence (RTI), OneLake serves not only as a persistent, queryable data layer but also as a critical component in reducing latency, cost, and complexity when managing event-driven architectures at scale.

This section dissects the architectural model that enables OneLake availability from Eventhouse, ensuring that data ingested in real time is efficiently exposed to downstream consumers in both raw and optimized formats.

**Architectural Flow**

At a high level, the architecture consists of the following stages:

1. Ingestion into Eventhouse (KQL DB)

   - Real-time data streams (via Eventstream or other pipelines) are ingested into Eventhouse in rowstore format for lowest latency.
   - This format is immediately queryable, enabling near-instant analytics post-ingestion.

2. Background Conversion to Columnstore

   - Behind the scenes, Eventhouse asynchronously converts rowstore data into columnar Parquet format for long-term analytics performance and compression efficiency.
   - These columnstore segments are co-located and made available through OneLake using shared storage pointers—avoiding data duplication.

3. Exposure in OneLake

   - The same Parquet-formatted data is made accessible through OneLake via logical shortcuts, either at the database level or for individual tables.

   - These OneLake representations appear as external tables for downstream compute engines (e.g., Spark, SQL, Power BI).

**Key Architectural Characteristics**

| Feature                          | Description                                                                                                                                                                                        |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hot and Cold Tiering             | Data initially resides in hot SSD-backed storage (rowstore), then is tiered to colder columnstore Parquet segments optimized for cost and performance.                                             |
| Parquet Exposure                 | The columnstore segments are exposed in Open Parquet format for compatibility with external engines.                                                                                               |
| One Copy Design                  | No redundant storage—data is referenced, not duplicated. This enables zero additional storage cost for making Eventhouse data available in OneLake.                                                |
| Latency Tuning                   | Trickling ingestion patterns (low event rates) can introduce delays (up to 3 hours) before data appears in OneLake. Heavier ingestion rates optimize latency by triggering faster materialization. |
| Adaptive File Optimization       | Eventhouse determines optimal file size for Parquet segments to balance performance and cost. No additional tuning is required by users.                                                           |
| Schema and Retention Constraints | Once OneLake exposure is enabled, schema changes and data deletion are restricted. Users cannot alter table schemas or delete data unless they disable OneLake availability.                       |

**Architectural Best Practices**

- **Design for Append-Only Workloads:** Due to schema immutability, datasets exposed to OneLake should be modeled as append-only where possible.
- **Avoid Excessive Trickling:** Avoid scenarios with a very low ingestion rate over extended time (e.g., few events per second), as this will delay columnstore availability in OneLake.
- **Use Logical Shortcuts Strategically:** Expose only the datasets that require cross-engine visibility; over-exposing datasets can lead to cost and operational overhead.
- **Understand the Cold Path Behavior:** For long-term analysis or integrations with external engines (e.g., Spark ML or Lakehouse), design queries to leverage OneLake data via SQL or Lakehouse endpoints.

##### 7. Vector Databases

### Technical deep dive

#### 1. Datatypes

Datatypes in Microsoft Real-Time Intelligence (Eventhouse/KQL Database) are more than schema constraints - they directly affect storage efficiency, query performance, and downstream integration, particularly with Power BI and external consumers.

**Core Datatypes and Storage Behavior**

Fabric RTI relies on a columnar storage engine, where each column is encoded and compressed independently. The choice of datatype influences both compression ratio and query execution plan:

- `datetime`: Always stored in UTC with nanosecond precision. Used extensively for filtering, binning, and temporal joins. Internally indexed for efficient range queries.

- `timespan`: Represents durations; supports arithmetic and comparisons. Appears as decimal in Power BI (in days), requiring careful modeling to preserve interpretability.

- `dynamic`: Stores JSON-like semi-structured data. Powerful for flexibility but expensive for parsing and filtering—avoid frequent projection or filtering on deep-nested fields.

- `string`: High-cardinality strings can inflate dictionary sizes and affect memory utilization. From its history, Kusto is aimed at working with strings, so if you have e.g. a number that is not calculated with store it as string. Use `hash()` where possible in joins or aggregations. The `hash()` function is recommended in scenarios where:

  - The actual string values are not needed in output,
  - You’re performing joins or group-bys where cardinality is high,
  - You need to reduce memory consumption and simplify value comparison.

- `int`, `long`, `real`, `decimal`: Fixed-precision numerics. Prefer `long` or `real` over `decimal` unless exact scale/precision is needed; decimal has a higher query-time cost.

**Modeling Implications**

- Avoid overuse of dynamic fields in hot paths; consider pre-flattening or projecting frequently used fields into dedicated columns via update policies.

- Be explicit with datetime handling when integrating with Power BI—timezone shifts (e.g., datetime_utc_to_local()) can degrade performance unless applied post-filtering.

- Normalize categorical fields used in slicers/joins into dimension tables (especially in Power BI) to avoid scanning large fact tables for distinct values.

- Enforce strong typing in ingestion paths—ambiguous schemas (e.g., mixing strings and numerics) can lead to costly type coercion at query time.

**Interop with Power BI**

When data is surfaced to Power BI:

- datetime → datetime (assumed UTC),
- timespan → decimal (duration in days),
- dynamic → string (Power Query may parse if JSON),
- bool, int, long, real → match directly.

Type conversions and representations may affect filter behavior and visuals e.g., duration in decimal form requires DAX formatting to be user-friendly.

##### 2. Update Policies

Update policies in KQL-Databases are server-side data transformation rules that automatically populate one or more target tables during ingestion of data into a source table. They are defined declaratively and executed in real time, enabling near-synchronous materialization of derived views, enriched datasets, or pre-aggregated snapshots—without requiring post-processing jobs.

**How Update Policies Work**

An update policy links a source table (where data is ingested) to one or more target tables (where processed results are written). The transformation logic is defined as a KQL function that runs at ingestion time. Architecturally, this means:

- The ingestion pipeline triggers the update policy as a side-effect of writing data to the source table.
- The output of the query is materialized into the target table in a transactionally consistent manner.
- Multiple target tables can be populated from the same source with different transformation logic.

**Common Use Cases**

- **Data filtering:** Routing only relevant records (e.g., where ErrorCode != 0) into a troubleshooting table.

- **Schema transformation:** Projecting or renaming columns to standardize downstream data structure.

- **Data enrichment:** Performing lookup joins against dimension tables to enhance the ingested records with descriptive metadata.

- **Data forking:** Distributing data from a raw ingestion table into multiple shaped, consumer-friendly tables based on business context (e.g., telemetry vs. alerts vs. billing).

**Technical Considerations**

- **Performance:** Since update policies execute at ingestion time, they directly impact ingestion throughput. Complex policies (e.g., joins, regex parsing) may throttle ingestion if not tuned.

- **Query behavior:** Policies must be ingestion-safe. That means they cannot use operators like `join kind=inner` on large tables without `hint.strategy=broadcast`, or call user-defined functions with unbounded logic.

- **Transformation Function:** Must take no parameters and be deterministic. Think of it as a logical view over newly ingested data.

- **Error handling:** If the update policy query fails, ingestion into the source table succeeds, but the target table is not updated. Failures are logged and can be monitored using .show ingestion failures.

- **Debugging:** Use `.get ingestion failures` or temporarily disable the policy and run the transformation logic manually to troubleshoot.

**Modeling Best Practices**

- Keep update policies idempotent and stateless — they should only process new ingested records, using ingestion-time context if needed.

- Precompute expensive transformations early via update policies if they are reused in queries, to offload query-time compute.

- Use the `.ingest inline` command or simulated ingestion to test policy logic before enabling in production.

- Avoid chaining update policies; Fabric does not support recursive execution between target tables with their own update policies.

**Example for an update policy**

In this example we enrich Logs using an update policy.

Step 1: Create the source table

```kql
.create table RawLogs (
    Timestamp: datetime,
    DeviceId: string,
    Message: string
)
```

Step 2: Create the Target Table

```kql
.create table EnrichedLogs (
    Timestamp: datetime,
    DeviceId: string,
    DeviceType: string,
    Region: string,
    Message: string
)
```

Step 3: Create a Dimension Table for enrichment

```kql
.create table Devices (
    DeviceId: string,
    DeviceType: string,
    Region: string
)
```

Step 4: Define a Transformation Function

```kql
.create function with (folder = "UpdatePolicies") EnrichRawLogs() {
    RawLogs
    | lookup kind=leftouter Devices on DeviceId
    | project Timestamp, DeviceId, DeviceType, Region, Message
}
```

Step 5: Attach the Update Policy to table `RawLogs`

```kql
.alter table RawLogs policy update
@'[{"IsEnabled": true, "Source": "RawLogs", "Query": "EnrichRawLogs()", "Destination": "EnrichedLogs"}]'
```

##### 3. Materialized Views

Materialized Views (MVs) in Microsoft Fabric RTI are a performance-critical modeling construct that allow pre-aggregation and deduplication of high-volume data streams in a cost-effective and scalable manner. Unlike traditional views or on-the-fly aggregations, materialized views are physically materialized and maintained incrementally using a delta-and-cursor-based architecture.

This section explores the internal mechanics, refresh behavior, query execution path, and advanced considerations for using Materialized Views effectively in Eventhouse and KQL Database.

**Internal Architecture**

Materialized Views are backed by a hidden physical table that stores precomputed results. The system maintains two key components:

- **View Table:** The hidden storage table containing the materialized extents.

- **Delta (Source Tail):** Newly ingested records not yet materialized.

![alt](./assets/images/materialized_views1.png)

The cursor tracks how far materialization has progressed in the source table. During materialization:

- New data is read based on the cursor position.
- Overlapping data is soft-deleted.
- A single commit replaces the materialized extents.
- The cursor is advanced accordingly.

This allows the view to stay fresh without reprocessing the entire source table, which is critical for high-ingest scenarios​.

**Query Execution Logic**

When querying a materialized view, the system combines the hidden view table and the delta tail to produce the most up-to-date result.

Query Planner Behavior:

- Aggregates the delta (non-materialized records).
- Joins it with the materialized part.
- Applies rewrite rules and filter pushdown to optimize execution​.

![alt](./assets/images/materialized_views2.png)

This mechanism ensures consistency and freshness, even in between materialization cycles.

You can also use the `materialized_view("ViewName", max_age)` function to explicitly reference only the materialized part, skipping delta aggregation. The function has an optional `max_age` argument. If the view was not materialized in the last `max_age` the entire view will be queried. This improves performance at the cost of data freshness and is useful for:

- Serving pre-aggregated metrics to Power BI dashboards.

- Running high-concurrency read queries under SLA constraints.

![alt](./assets/images/materialized_views3.png)

**Constraints and Characteristics**

- Defined over a single source table with a single summarize statement.
- Cannot contain joins, unions, or multiple stages of computation.
- Schema is auto-inferred and updated unless schema auto-update is disabled.
- MV over another MV is supported only if the first view uses `take_any()` (i.e., for deduplication).

**Materialization Behavior and Capacity Limits**

Materialization is an asynchronous background job, triggered when capacity allows. Triggers are based on:

- Eventhouse capacity policy (per-cluster limit on concurrent materializations).
- Extent age and size of delta region.

To inspect the materialization status

```kql
.show materialized-view <ViewName> details
```

**Performance Tuning Tips**

- Use `bin()` and `arg_max()`/`take_any()` to support time-based aggregations and deduplication.
- Filter early and reduce cardinality before materialization to lower cost.
- Avoid defining more MVs than the system can refresh concurrently.

Consider partitioning policies on the source table if your view has predictable slice patterns (e.g., by customer, tenant, or time).

**Use Cases**

- **Sessionization:** `arg_max()` per session ID for last known state.
- **Downsampling:** `summarize count() by bin(Timestamp, 1m)` for real-time visualizations.
- **De-duplication:** `take_any()` for noisy or overlapping event streams.
- **Power BI acceleration:** Precompute aggregates to reduce DirectQuery load and improve responsiveness.

##### 4. External Tables

##### 4. Partitioning Policies

##### 5. Modeling for Power BI

### Implementations

### Troubleshooting

### Orchestration and optimization

### Schemas and throughput

### Monitoring and pricing

### Hands-on lab
