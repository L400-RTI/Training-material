# Module 7 - Advanced AI Capabilities in Microsoft Fabric Real-Time Intelligence (RTI)

## Introduction to the Module

- **Objective:** Introduce advanced AI use cases within Real-Time Intelligence using Microsoft Fabric.
- **Audience:** Data engineers, architects, and consultants building AI-powered real-time applications.
- **Focus Areas:**
  - Vectors in Eventhouse
  - Embedding storage and retrieval
  - AI plugins: `ai_embed_text`, `ai_chat_completion_prompt`
  - OneLake mirroring and semantic search scenarios

---

## Architectural Deep Dive Highlights

### Eventhouse as a Vector Store

- Dual storage model: Rowstore (real-time) + Columnstore (analytics)
- Embeddings stored in `dynamic` columns for scalability
- Partitioning strategy for high performance vector similarity

### OneLake Mirroring

- Delta Parquet format with adaptive mirroring
- Auto-compaction avoids Spark optimize overhead
- Zero-copy architecture enables Lakehouse/Power BI shortcuts

### Plugins Architecture

- Seamless integration with Azure OpenAI
- Plugin runtime execution from within KQL context

## Architectural Deep Dive - Eventhouse and OneLake

At the heart of Microsoft Fabric’s real-time intelligence (RTI) capabilities is Eventhouse, an advanced telemetry platform purpose-built for high-throughput data, ultra-low-latency querying, and—crucially for this module—AI-native architectures. In this section, we go under the hood to examine how Eventhouse supports storing, querying, and reasoning over vectorized data, and how its design enables real-time, AI-powered applications at enterprise scale.

Eventhouse extends the core Kusto engine, but differentiates itself with seamless integration into Fabric's unified compute and storage layers. It leverages a dual-storage model: an ephemeral **rowstore** for low-latency access and a persistent **columnstore** optimized for analytical workloads. When streaming data arrives, it is first ingested into the rowstore, providing sub-second availability. Later, Eventhouse transforms this data into an optimized shard-based columnar format for long-term querying and integration.

Crucially, Eventhouse introduces **adaptive mirroring into OneLake**, Fabric’s centralized storage backbone. This allows ingested data to be automatically written to **Delta Parquet** format in OneLake, following industry-standard, open data formats. Unlike traditional pipelines, this mirroring is handled _internally_ and _intelligently_. Eventhouse batches files into ~250MB sizes, aligning with Delta Lake optimization guidance, without requiring the user to run Spark optimize jobs or compaction flows. This makes the system exceptionally cost- and performance-efficient, especially for continuous, high-frequency streaming workloads.

The mirrored data can then be accessed in real-time by other Fabric components—Lakehouse, Warehouse, or even external tools—using **shortcuts**. This promotes a zero-copy architecture, enabling developers to build AI pipelines and dashboards on top of event-driven data without duplication or delay.

To accommodate advanced AI workloads, the Eventhouse schema layer includes **support for dynamic columns**, allowing ingestion of semi-structured or high-dimensional vector data. This is essential for storing AI embeddings, which often vary in dimension and source structure. Combined with Eventhouse’s ability to scale partitioned storage, these dynamic fields become the backbone of semantic search and retrieval-augmented generation (RAG) solutions.

Finally, this architecture is enriched by **plugin extensibility**. Plugins like `ai_embed_text` and `ai_chat_completion_prompt` enable Eventhouse to interact directly with Azure OpenAI endpoints, facilitating embedded LLM reasoning and text-to-vector transformations inline. This architectural choice positions Eventhouse not just as a data store, but as a first-class AI execution platform for streaming intelligence.

---

## Module 3: Technical Deep Dive Highlights

### Vectors and Embeddings

- Embedding generation using `ai_embed_text` plugin
- Supports OpenAI embeddings (`text-embedding-ada-002`)
- KQL support for storing and querying high-dimensional vectors

### Similarity Search

- Use of `vector_cosine_distance()` in KQL
- Indexing for scalable top-K retrieval
- Threshold tuning for relevance control

### Plugin Deep Dive

- `ai_embed_text`: Generates vector embeddings from text
- `ai_chat_completion_prompt`: Contextual response generation from structured/unstructured logs

## Technical Deep Dive – Vectors, Embeddings, and Semantic Querying in Eventhouse

As enterprises race to implement AI-first architectures, the demand for real-time vector storage and semantic search has surged. Eventhouse addresses this head-on with native support for high-dimensional vector embeddings and fast approximate similarity search—all accessible via Kusto Query Language (KQL).

At a foundational level, Eventhouse supports embeddings through its **dynamic column type**, allowing storage of arbitrary-length vectors per record. These embeddings—often generated from models like OpenAI’s `text-embedding-ada-002`—can represent anything from customer support transcripts to log anomaly descriptions. Using the `ai_embed_text` plugin, users can invoke Azure OpenAI or another configured model to convert unstructured text into vector embeddings directly within a KQL expression.

These embeddings are then stored as JSON arrays in the dynamic column and can be indexed and queried using new **vector-aware functions**. Eventhouse introduces `vector_cosine_distance()` and related functions to compare an input vector to those stored in the table. This enables **top-K similarity search** using cosine similarity, a standard metric in vector search engines. The queries support filter predicates, allowing efficient hybrid search where text filters narrow the candidate set before similarity ranking is applied.

A major strength of this architecture is **scale**. Eventhouse supports millions of vectors and intelligently shards them based on partitioning policies. This ensures that even similarity searches across large corpora (e.g., support tickets, telemetry logs, product descriptions) complete within milliseconds to seconds, depending on cardinality and query complexity.

Another standout feature is **plugin orchestration within KQL**. Beyond embedding, the `ai_chat_completion_prompt` plugin allows users to pass structured or semi-structured data (like logs, telemetry, or extracted entities) into a prompt template and invoke a model like GPT-4 for contextual reasoning. For example, a SOC analyst could query recent log entries and prompt an LLM to label them as benign or suspicious. This can be done inline, at query time, without moving data to another service.

Eventhouse’s execution engine supports **batched plugin evaluation**, allowing multiple rows to be sent together to the LLM for processing. This drastically improves throughput and reduces cost. Since embeddings are often reused, developers can cache embeddings per document and only generate new ones for incremental content, reducing round-trips to OpenAI.

In short, Eventhouse transforms the traditional telemetry engine into a high-performance, AI-native platform. By co-locating vector generation, storage, and querying in one system—and integrating with the broader Fabric ecosystem via OneLake—developers can now build rich, semantic, and intelligent applications with minimal pipeline complexity. The system’s plugin model and vector capabilities are not just bolt-ons; they represent a foundational shift in how streaming data and AI can coalesce in real time.

---

## Implementation Example Scenarios

### Scenario 1: Build Your Own Copilot

- Use vector similarity for RAG (Retrieval-Augmented Generation)
- Store previous chat contexts in Eventhouse
- Use LLMs for personalized responses

### Scenario 2: Threat Detection

- Ingest security logs
- Use embeddings + LLM to detect anomalous or malicious activity

### Scenario 3: Semantic Recommendation Engine

- Ingest product/ingredient metadata
- Recommend based on contextual similarity of vector embeddings

---

## Troubleshooting

### Common Pitfalls

- Mismatched embedding dimensions across datasets
- Long similarity search execution due to lack of partitioning

### Best Practices

- Pre-check model encoding settings
- Use `vector_score_threshold()` to limit results
- Regularly validate embedding schema compatibility

### Best Practices Deep Dive

## Best Practices for Operationalizing Vectors in Microsoft Fabric RTI

Effectively implementing vector storage and semantic search in Microsoft Fabric Real-Time Intelligence (RTI) requires not only technical fluency but also architectural discipline. As vector-based applications mature beyond proof-of-concept, operational resilience and precision become critical. This section outlines three advanced best practices that help ensure reliability, performance, and maintainability in real-world deployments.

### Pre-check Model Encoding Settings

Before generating or storing any embeddings in Eventhouse, it's essential to align encoding settings with the embedding model in use—particularly when using the `ai_embed_text` plugin. The plugin supports Azure OpenAI models such as `text-embedding-ada-002`, which output fixed-length vector arrays. If schema mismatches occur (e.g., storing a 1536-dimensional vector in a column expecting 1024 dimensions), it can result in ingestion failures or silent truncation—both of which are difficult to debug at scale.

To mitigate this, establish a pre-ingestion verification scheme as part of your ingestion. This can be implemented as a schema validation function in KQL. When working across multiple vector sources or switching between OpenAI models, always re-confirm that dimensionality and data types match your Eventhouse table schema—especially when using `dynamic` columns, which can obscure errors at the metadata level.

Another critical consideration is tokenization: different models tokenize text differently, which can impact embedding granularity. To preserve consistency across training and inference, document and lock in your tokenizer and embedding model versions as part of your deployment objects. This is especially important when embeddings are being generated in external systems (e.g., Azure ML or Databricks) and then ingested into Fabric.

### Use `vector_score_threshold()` to Limit Results

Similarity search in Eventhouse using functions like `vector_cosine_distance()` can be powerful—but also computationally expensive. Without constraints, these queries can evaluate against millions of vector rows, significantly increasing execution time and potentially exhausting capacity.

To mitigate this, use the `vector_score_threshold()` function to apply a cosine similarity threshold that filters out semantically irrelevant results. For example, if you're searching for customer support logs similar to a known issue description, setting a threshold of `0.8` ensures only closely matching cases are returned. This not only improves performance but enhances the interpretability of the results.

The threshold should be tuned based on empirical evaluation of your dataset and use case. For anomaly detection, a high threshold (e.g., `>0.9`) might be appropriate; for semantic recommendations, a broader range (e.g., `>0.6`) may yield better recall. This tuning can be performed using test queries and monitoring result distributions.

Furthermore, combining `vector_score_threshold()` with KQL’s `top-k` filtering gives you both relevance and precision, allowing real-time applications to remain performant even under high throughput.

### Regularly Validate Embedding Schema Compatibility

In production environments, embedding schemas often evolve. Text fields may be added, removed, or re-encoded, especially in environments where upstream data structures are managed by multiple teams. Any such change can corrupt vector quality or make historical data incompatible with new queries.

To avoid this, implement a schema validation routine that checks the following on a scheduled basis:

- **Vector dimensionality and type**
- **Embedding source model version**
- **Schema shape of `dynamic` or nested fields used for embeddings**
- **Encoding logic consistency across environments**

This can be enforced using a metadata manifest table in Eventhouse or external configuration management in Git. Also, consider implementing a form of schema fingerprinting: store a hash of the embedding generation pipeline configuration alongside each vector row, and surface mismatches in monitoring dashboards.

When schema drift is detected, downstream vector queries should be halted or redirected to filtered subsets to avoid query corruption. For teams managing multi-tenant or multi-model deployments, isolating embeddings by table or database is advisable to reduce the blast radius of schema changes.

---

By integrating these best practices into your architecture, you ensure that vector-powered applications in Microsoft Fabric Real-Time Intelligence are not just functional, but also production-grade—capable of scaling with enterprise demand and surviving real-world complexity.

---

## Orchestration and Optimization

### Adaptive Mirroring

- Eventhouse auto-determines write frequency and file size (250MB optimal)
- Write delay customizable (default 3 hours, configurable to 5 min)

### Plugin Optimization

- Batch queries via `ai_chat_completion_prompt` for throughput
- Minimize cost by caching embeddings rather than repeated generation

### RAG Architecture

- Use Eventhouse as a persistent memory vector DB
- Ingest → Embed → Store → Retrieve → Prompt

---

## Schemas and Throughput

### Schema Design for AI Workloads

- Use `dynamic` for embedding storage
- Include metadata like timestamp, source ID, context tags

### Performance Considerations

- Partition by high-cardinality fields (e.g., customer_id)
- Separate raw and enriched tables for clean modeling

### Schemas and Throughput Deep Dive

## Schema Design and Performance Best Practices for AI Workloads in Fabric RTI

Designing an efficient, scalable schema is foundational to the success of AI-enhanced real-time intelligence solutions in Microsoft Fabric. As workloads increasingly incorporate embeddings, vector similarity queries, and context-aware inference, traditional schema practices fall short. This section outlines essential best practices for schema modeling and performance optimization, ensuring that your Fabric Eventhouse solutions are prepared to operate under enterprise-scale, low-latency demands.

### Schema Design for AI Workloads

#### Use `dynamic` for Embedding Storage

The cornerstone of AI workloads in Eventhouse is the ability to store high-dimensional vector embeddings. These embeddings, often generated via models like OpenAI’s `text-embedding-ada-002`, produce arrays of 768, 1024, or 1536 floating-point values. Attempting to model these dimensions as individual columns leads to bloated schemas, complex update logic, and poor maintainability.

Instead, the recommended best practice is to use the `dynamic` data type in Eventhouse for embedding storage. This allows you to store vector arrays as JSON-like structures—ideal for schema flexibility and compatibility with plugin-generated embeddings. With `dynamic`, developers can evolve the embedding format over time without requiring costly schema migrations, and downstream queries can deserialize and compute similarity as needed.

In addition, using `dynamic` supports use cases where embeddings are attached to multiple context fields—such as summarizations, user messages, or document chunks—without rigid column definitions. This makes it easier to ingest data from diverse sources while maintaining consistent storage practices across use cases.

#### Include Metadata: Timestamp, Source ID, and Context Tags

Beyond the embedding itself, AI applications require rich metadata to enable context filtering, time-bound reasoning, and auditability. Every row that contains an embedding should also include the following key metadata fields:

- **Timestamp (`datetime`)** – Enables time-series slicing, event windowing, and decay logic for vector relevance over time.
- **Source ID (`string`)** – Indicates the origin of the embedding (e.g., application name, pipeline ID), aiding in debugging and drift detection.
- **Context Tags (`dynamic`)** – A flexible set of descriptive labels (e.g., `"category": "support"`, `"priority": "high"`) that allow for semantic segmentation, filtering, and prompt customization in RAG scenarios.

This combination of vector and metadata supports both similarity search and contextual retrieval, a pattern commonly seen in retrieval-augmented generation (RAG), anomaly detection, and intelligent alerting systems.

---

### Performance Considerations

#### Partition by High-Cardinality Fields

Performance in Real-Time Intelligence vector workloads is tightly linked to how well data is partitioned for parallel processing. In Eventhouse, this means leveraging horizontal partitioning via ingestion-time sharding. The recommended approach is to partition tables using a high-cardinality field such as `customer_id`, `device_id`, or `session_id`.

Partitioning by a high-cardinality identifier achieves two critical objectives:

1. **Query Pruning** – Only relevant shards are scanned during queries, drastically reducing I/O.
2. **Ingestion Scaling** – Eventhouse can parallelize ingestion pipelines across shards, improving throughput and consistency under heavy load.

When partitioned effectively, similarity queries (`vector_cosine_distance()` + `where`) can achieve sub-second latency even over tens of millions of records, which is essential for real-time applications such as live chat assistants or fraud detection systems.

#### Separate Raw and Enriched Tables

Another key performance best practice is to separate raw and enriched data into distinct tables. AI pipelines often involve multiple stages: raw ingestion, embedding generation, enrichment with tags or scores, and downstream inference. Attempting to store all stages in one monolithic table leads to convoluted schema logic, data quality issues, and degraded query performance.

Instead, adopt a layered schema design:

- **Raw Table** – Stores original events, text, or logs prior to embedding.
- **Vector Table** – Stores embeddings and associated metadata.
- **Enriched Table** – Stores results of similarity matches, scoring, or inference outputs.

This separation supports modular pipeline orchestration, simplifies table compaction and retention strategies, and enables data teams to independently scale or tune each phase without cross-impact.

Additionally, by separating concerns, you can apply differing retention policies—for example, retaining raw data for 7 days, vectors for 30 days, and enriched results for 90 days—aligning storage use with business value.

---

## Module 8: Monitoring and Pricing

### Plugin Telemetry

- Log latency and error rates from AI plugins
- Capture embedding generation counts per model and table

### Storage Cost Management

- OneLake mirroring is free (same logical copy)
- Embedding generation charged via Azure OpenAI subscription

### Real-Time Intelligence Query Cost Control

- Use query limits and time filters in similarity searches
- Materialize static embedding scenarios if re-used often

---

# Hands-On Lab Example: Semantic Analysis and Reasoning on Delivery Truck Logs

## Objectives

- Embed textual delivery incident logs, store vectors, and perform semantic similarity search
- Augment real-time data with AI reasoning for operational insights

## Lab Steps

### 1. Ingest Delivery Logs Dataset into Eventhouse

Load a structured dataset of delivery incident logs from trucks. Example log entries might include:

- "Delayed due to weather"
- "Route blocked"
- "Package not found"
- "Mechanical issue on vehicle"

Ingest the data into an Eventhouse table named `truck_logs`.

### 2. Generate Embeddings Using `ai_embed_text`

Use the `ai_embed_text` plugin to convert the `incident_description` column into vector embeddings:

```kql
set async_execution = true;
truck_logs
| extend incident_vector = ai_embed_text("azure_openai_deployment_url", incident_description)
```

### 3. Store Vectors Using a `dynamic` Column

Ensure `incident_vector` is defined as a `dynamic` column in your table schema. This allows efficient storage and querying within Eventhouse.

Example KQL snippet to confirm or cast the column:

```kql
truck_logs
| extend incident_vector = todynamic(incident_vector)
```

### 4. Perform Semantic Similarity Search

Use `vector_cosine_distance()` to find records similar to a new incident:

```kql
let new_incident = "Road closed due to snowstorm";
let new_vector = ai_embed_text("azure_openai_deployment_url", new_incident);
truck_logs
| extend similarity = vector_cosine_distance(incident_vector, new_vector)
| top 5 by similarity desc
```

### 5. Summarize with `ai_chat_completion_prompt`

Use `ai_chat_completion_prompt` to generate a summary for dispatchers:

```kql
truck_logs
| where TimeStamp > ago(30m)
| summarize logs=make_list(incident_description, 10)
| extend summary = ai_chat_completion_prompt("azure_openai_chat_url", "Summarize these recent delivery incidents for a dispatcher: " + strcat_array(logs, "; "))
```

### Bonus Tasks

#### Add Activator Trigger for High-Severity Incidents
Configure an Activator rule to trigger on critical phrases (e.g., "theft", "breakdown") or based on AI-generated summaries.

#### Export Embeddings to OneLake for ML Training
Use `.export` or Continuous Export to write embeddings to OneLake in Delta Parquet format for use in ML model training pipelines.

```kql
.export async to delta (h@"https://<your_onelake_url>/deliveries/embeddings") <|
truck_logs
| project TimeStamp, incident_description, incident_vector
```

> **Note**: Replace `azure_openai_deployment_url` and `azure_openai_chat_url` with your actual Azure OpenAI endpoint URLs.

---
