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

External tables in Microsoft Fabric Real-Time Intelligence (RTI) are user-defined schema entities that reference data stored outside the native Kusto (Eventhouse/KQL DB) database.

They provide a critical architectural capability for real-time access, cross-system integration, and cost optimization without requiring ingestion into the database engine.

An external table behaves similarly to a regular KQL table in that it exposes a well-defined schema, supports partitions, and is addressable via standard KQL queries. However, the backing data is remote—stored either in cloud storage systems or SQL databases.

**External Table Types**

There are two primary external table types:

- **Storage External Tables:** Reference files stored in Azure Blob Storage,
  Azure Data Lake Storage Gen2, or Microsoft OneLake. Supported formats
  include Parquet, Delta, CSV, JSON, and Cosmos DB's Stream format.
- **SQL External Tables:** Reference relational database tables directly
  from systems such as Azure SQL Database, Cosmos DB, PostgreSQL, and MySQL.

Each type demands specific configuration:

- **Storage tables** require storage connection strings, path formats,
  and format specifications.
- **SQL tables** require SQL connection strings and native query mappings.

**How External Table Queries Work**

When querying an external table, the Fabric engine does not ingest the
data into Eventhouse. Instead, it issues an on-demand retrieval and
parsing operation:

- For **Storage External** Tables, file metadata is accessed first to plan
  efficient reads (especially for partitioned datasets).
- For **SQL External Tables**, queries are pushed down and executed
  against the external SQL database whenever possible (pushdown optimization).

Partition pruning, format-specific readers (Parquet, Delta), and
optimized network retrieval are core backend mechanisms that ensure
minimal latency and resource consumption.

Example:

```kql
external_table("MyExternalStorageTable")
| where Timestamp > ago(1d)
| summarize count() by bin(Timestamp, 1h)
```

Behind the scenes, this pulls only the minimum required file segments
or database rows.

**Partitioning**

Partitions are fundamental for scaling external table performance:

- **Storage tables** often partition by date or tenant ID in the folder
  path structure.
- **SQL external** tables rely on database indexes for partitioning,
  with optional KQL-side partition hints.

Effective partitioning is crucial to avoid full scans and optimize query
latency and cost. Partition keys must match query patterns for efficient pruning.

**Authentication**

Fabric supports multiple authentication models depending on the external system:

- Managed Identity for Azure resources.
- EntraID Principals for cross-service authentication.
- SQL Authentication for SQL databases.

Secure credential storage is enforced, and external table definitions
reference credential entities abstracted from the user.

**Query and Export**

External tables can be used for both query and export workflows:

- **Query:** Ad-hoc or scheduled queries reading from external
  sources in place.
- **Export:** Data in Eventhouse can be continuously or on-demand
  exported to external storage using Continuous Export.

<div class="info" data-title="Note">

> **Continuous Export into external tables must account for schema drift and file format constraints (only Parquet, Delta, CSV, and JSON supported).**

</div>

**Performance Considerations**

- **Cost Model:** No storage cost in Eventhouse; costs shift toward network, read transactions, and potentially compute from source systems​.
- **Performance Tip:** Frequent heavy queries over external tables might be more expensive and slower than ingesting the data. Evaluate query frequency and data freshness needs.
- **Query Acceleration:** Use Query Acceleration Policies where applicable (currently in preview) to speed up queries over OneLake shortcuts​.

**Common Pitfalls**

- High-latency storage or SQL servers severely affect query times.
- Poor partitioning leads to full scans and excessive resource usage.
- Schema mismatches between definition and actual data can cause query errors.
- Authentication failures if tokens expire or credentials are rotated incorrectly.

**Hidden Complexity**

While external tables seem straightforward conceptually, under the hood they involve:

- Distributed read scheduling
- Partition pruning engines
- Intelligent format readers
- Secure and auditable access tracking
- Error retries and partial query failure handling

Fabric hides these complexities from the user but understanding them helps optimize architecture designs.

##### 4. Partitioning Policies

Partitioning policies in Microsoft Fabric RTI (Real-Time Intelligence) allow database administrators and solution architects to control the physical layout of data inside tables.

In a system designed for massive ingestion and low-latency querying, partitioning is critical for:

- Minimizing query scan footprint (I/O optimization)
- Accelerating aggregation and filtering
- Optimizing storage lifecycle management (retention policies)
- Reducing cost (compute and storage)

Partitioning is **declarative:** it is defined in advance as part of the table’s metadata, and the engine automatically applies it during ingestion and query processing.

**How Partitioning Policies Work**

Partitioning policies logically segment the ingested data into extents based on one or more columns.

An extent is the core internal storage unit in Kusto (Fabric Eventhouse) — it can be thought of as a "mini-table" with up to hundreds of megabytes of data.

When a partitioning policy is configured:

- During ingestion, data is bucketed based on the partition key(s).
- During querying, only the relevant buckets (extents) are accessed, avoiding full table scans.
- During retention, partition policies help the system efficiently delete or archive data.

**Types of Partitioning**

Partitioning in KQL databases is **column-based** and usually falls into two common scenarios:

1. **Time-based Partitioning**

   - Most critical for telemetry, log analytics, IoT, event data.
   - Partition on a datetime column like Timestamp or EventTime.
   - Typically combined with `bin()` functions in queries for efficient time slicing.

   Example:

   ```kql
   .alter-merge table Events policy partitioning
   { "PartitionKeys": [ { "ColumnName": "Timestamp", "Kind": "UniformRange" } ] }
   ```

2. **Key-based Partitioning**

   Partitioning based on business keys, such as `CustomerID`, `DeviceID`, `Region`, or `TenantID`.
   Common for multitenant solutions to improve query isolation and minimize noisy neighbor effects.

   Example:

   ```kql
   .alter-merge table Metrics policy partitioning
   { "PartitionKeys": [ { "ColumnName": "TenantId", "Kind": "Hash" } ] }
   ```

**Partition Key Kinds**
Partition keys can have different partitioning strategies (Kind)​:

- **UniformRange** — Used for datetime or numeric columns. Buckets are ranges (e.g., one-day intervals).
- **Hash** — Used for categorical/text keys (e.g., `CustomerId`). Buckets are based on hash values.
- **None** — No partitioning.

Choosing the wrong kind (e.g., hashing timestamps) can severely degrade performance.

**How Partitioning Affects Queries**

During query compilation:

- The query engine applies partition pruning: only relevant extents are scanned based on filter predicates.
- Example: A query filtered on `Timestamp > ago(1d)` automatically limits the scan to recent partitions.

Without a filter on the partition key(s), full table scan occurs - leading to worse performance than expected.

<div class="warning" data-title="Critical Tip">

> **Always filter on partition keys wherever possible for performance-sensitive queries.**

</div>

**Best Practices for Defining Partitioning Policies**

- **Time-based data:** Always partition on a datetime column (e.g., event timestamp).
- **High cardinality dimensions:** Partition on fields like `DeviceId` or `CustomerId` if you query by them.
- **Low cardinality caution:** Avoid partitioning on fields with very few unique values (e.g., Status = Active/Inactive) — it provides no benefit.
- **Multiple keys:** You can define multiple partition keys, but be mindful of complexity and diminishing returns.
- **Retention and Cost:** Align partitioning keys with your retention policies for efficient aging-out of data.

**Common Mistakes**

- Partitioning on non-filtered columns: Leads to no pruning benefit.
- Over-partitioning: Too many partitions (e.g., by `UserId`) can create operational overhead and metadata bloat.
- Wrong partition key type: Hash when uniform range would be better (especially for time series).

**Hidden Complexity**
Internally, the Fabric Eventhouse engine:

- Tracks partitions via extent metadata.
- Automatically merges small extents and splits large ones during background optimization cycles (Compaction, Repartitioning).
- Dynamically updates partition pruning hints during query plan optimization.

Users **do not** manually manage partitions once policy is set - it's a fully managed, auto-optimized system.

##### 5. Modeling for Power BI

When building real-time analytics solutions in Fabric RTI, modeling data properly for Power BI is essential to achieve:

- Fast and scalable reports
- Correct aggregations and slicing
- Efficient storage and memory usage
- Seamless end-user experiences

While raw data might be optimized for ingestion and storage in Eventhouse (KQL DB), it must be remodeled to match Power BI’s semantic and performance requirements​.

**Fabric to Power BI Connection Modes**

When connecting Power BI to Eventhouse (KQL DB) you typically use:

| Mode        | Description                                                 | When to Use                                                                        |
| ----------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| DirectQuery | Queries the Eventhouse database live at query time.         | Real-time freshness is critical. Data size too large to fit in memory.             |
| Import      | Imports a static snapshot of the data into Power BI memory. | When query latency from Eventhouse is high, or high-performance dashboards needed. |
| Dual        | Supports both import and DirectQuery dynamically.           | Best of both worlds; for filtering and small lookups.                              |
| DirectLake  | For lakehouse scenarios, not typical for KQL sources.       | Only when sourcing via OneLake or Delta tables.                                    |

**Best Practice:**

- Use **DirectQuery** or **Dual** for live real-time datasets.
- Use **Import** for heavy aggregations on large datasets that can tolerate some latency​.

**Importance of Star Schema**

A star schema remains best practice for Power BI models even when sourcing from KQL​:

- **Fact Tables:** Large tables capturing events (telemetry, transactions, logs).
- **Dimension Tables:** Smaller tables for descriptive attributes (users, devices, categories).

**Benefits:**

- Improved performance (Power BI query engine optimizations)
- Cleaner DAX and simpler relationships
- Enables Dual storage mode for dimensions, allowing fast slicing without live Eventhouse queries.

**Storage Mode Strategy**

Real-world guidance for fabric RTI to Power BI modeling:

| Table Type                       | Recommended Storage Mode | Reason                                   |
| -------------------------------- | ------------------------ | ---------------------------------------- |
| Fact Table (Events, Logs)        | DirectQuery              | Real-time freshness; too big for import. |
| Small Dimensions (Lookup Tables) | Dual                     | Faster slicer/filtering; caches locally. |
| Large Dimensions                 | DirectQuery              | If size > 1M rows and freshness needed.  |

<div class="info" data-title="Key Tuning Tip">

> **Set dimensions that do not change often (e.g., country, device type) to Dual mode to avoid query latency during filtering​.**

</div>

**Key Tuning Tip:**

**Handling DateTime Columns**

Datetime modeling is non-trivial with KQL sources​​​:

- Always treat DateTime columns as UTC.
- Create a Calendar Table to filter by dates.
- Use datetime_utc_to_local() only carefully (performance penalty if used extensively​).
- Use relative time slicers in Power BI for "Last N hours/minutes" analysis​.

Example of generating a DateTime table (M Query):

```M
let
    StartDate = DateTime.From(Date.AddDays(DateTime.LocalNow(), -30)),TimeSeries = List.DateTimes(StartDate, 43200, #duration(0,0,1,0)),
    #"Converted to Table" = Table.FromList(TimeSeries, Splitter.SplitByNothing(), {"Timestamp"})
in
    #"Converted to Table"
```

**Query Pushdown and Native Query**

When using the Azure Data Explorer (Kusto) connector:

- Native Query folding is supported: KQL runs server-side.
- Avoid heavy Power Query (M) transformations post-load — push filtering and aggregation into KQL as much as possible.

Best practice:
Model complex transformations as Kusto Functions inside Fabric and reference them from Power BI.

**Monitoring Power BI Query Performance**

In large RTI solutions:

- Use Performance Analyzer in Power BI Desktop.
- Watch for slow DirectQuery requests.
- Profile KQL query execution in Eventhouse side (.show queries).

Typical signs of bad modeling:

- High row retrieval counts
- Slow slicer/filter performance
- Repeated queries without result reuse

**Common Modeling Pitfalls**

- No star schema: Flat wide tables slow down slicers.
- DirectQuery everything: Even for small dimension tables — causes unnecessary latency.
- Local time conversions in visuals: Slows queries massively.
- Missing relationships: Forces Power BI to do expensive cartesian joins.
- Overuse of calculated columns: Instead, compute fields at the source using KQL.

**Hidden Complexity**

Behind the scenes:

- Power BI maintains a query cache even for DirectQuery datasets.
- Dual-mode tables automatically switch modes depending on query patterns.
- Advanced users can parameterize KQL queries via M dynamic parameters for multi-tenant or on-demand filtering.

### Implementations

### Troubleshooting

### Orchestration and optimization

### Schemas and throughput

### Monitoring and pricing

### Hands-on lab
