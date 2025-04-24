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

##### 4. Modeling for Power BI

Power BI semantic models built atop KQL-Databases must accommodate latency, freshness, and cardinality. Key architectural considerations include:

- Using star schemas over flat tables to improve slicer/filter efficiency,
- Ensuring dimension tables are set to Dual mode when feasible to reduce joins on Direct Query paths,
- Modeling datetime fields for efficient filtering (e.g., via time rounding or calendar relationships),
- Using KQL functions as semantic objects for reuse and clarity.

Semantic models should be architected with DirectQuery for the fact tables and dual mode for the dimension tables to balance performance with real-time accuracy.

### Technical deep dive

### Implementations

### Troubleshooting

### Orchestration and optimization

### Schemas and throughput

### Monitoring and pricing

### Hands-on lab
