## Module 13 - CI/CD and ALM

### Introduction

In this module, we explore the critical role of Application Lifecycle Management (ALM) and Continuous Integration / Continuous Deployment (CI/CD) within the context of Microsoft Fabric’s Real-Time Intelligence (RTI) ecosystem. As real-time data solutions mature from experimentation to production workloads, the need for robust, repeatable, and automated deployment practices becomes paramount—not only to scale, but to maintain trust, compliance, and operational excellence.

We will dive deep into the tools, APIs, pipelines, and integration patterns that enable enterprise-grade DevOps practices for core RTI components, including Eventstreams, KQL Databases, Eventhouse, and Data Activator. This module addresses both platform-native capabilities like Git integration and deployment pipelines, as well as external orchestration through Azure DevOps and GitHub Actions.

Beyond the mechanics of deployment, we will cover key ALM considerations:

- How to version, test, and promote RTI artifacts across environments
- How to leverage automation APIs for declarative deployments
- How to troubleshoot deployment issues and schema inconsistencies
- Known limitations and workarounds in current CI/CD support for RTI
- Strategies for monitoring deployment health, governance, and compliance

By the end of this module, you will have the knowledge to design, implement, and operate a CI/CD pipeline tailored to Microsoft Fabric’s Real-Time Intelligence workloads, with the rigor and reliability demanded by enterprise production systems.

### Architectural deep dive

In this section, we explore the architecture underlying Continuous Integration, Continuous Deployment (CI/CD), and Application Lifecycle Management (ALM) for Real-Time Intelligence workloads in Microsoft Fabric, focusing on Eventhouse, KQL Database, and Event Streams.

#### Key Architectural Components and Interactions

The core RTI components relevant to ALM are:

- **Eventhouse:** A scalable ingestion and query platform, leveraging Azure Data Explorer (ADX) backend capabilities but optimized for Fabric’s capacity and operational model.

- **KQL Database:** The primary data storage and query layer inside Eventhouse, exposing Kusto Query Language (KQL) for transformations, aggregations, and materialized views.

- **Event Streams:** Managed streaming ingestion pipelines feeding Eventhouse, enabling low-latency data arrival for analytical and operational scenarios.

ALM architecture integrates these components into a source-controlled deployment workflow, either via Git integration or REST APIs, enabling version-controlled schema definitions, policies, and artifacts. Git integration comes with the Fabric Workspaces. If you want to do autmation on your own you can use the REST APIs.

##### CI/CD Architecture in Fabric RTI

There are two architectural paths for deploying and managing RTI artifacts:

**Git Integration and Deployment Pipelines:**

- Workspaces can be connected to Azure DevOps or GitHub repositories to synchronize artifacts bidirectionally.
- Upon sync, Fabric serializes RTI objects (Eventhouse, KQL Database, etc.) into a folder-based schema with platform metadata, properties JSON, and KQL schema files.
- Deployment pipelines orchestrate multi-environment promotion (Dev → Test → Prod) without external tools, using these serialized definitions.

**API-driven deployments:**

- Public REST APIs expose operations for create, update, delete on Eventhouse, KQL Databases, Event Streams.
- Crucially, these APIs accept a "create with definition" payload that encodes the KQL schema and object definitions as Base64-encoded scripts.
- The platform executes these scripts server-side, enabling declarative, idempotent deployments.

**Notable architectural decisions:**

- Artifact deletions in Git do not trigger deletions in Fabric; only additive and non-destructive changes are propagated.
- Platform maintains logical IDs to rebind resources across environments during promotion.

#### Architectural Considerations for Capacity and Cost

Implications of capacity management tightly coupled with Eventhouse scaling mechanics are:

- Eventhouse auto-scales based primarily on hot cache size, not query load alone.
- Clusters auto-scale up/down but are bounded by minimum consumption settings (soon renamed "Always On" mode).
- Customers incur compute-based pricing for uptime rather than per-query or per-ingestion billing.

Architecturally, this enforces a tight feedback loop between caching policies and deployment configurations: schema definitions must explicitly set caching and retention to control operational cost and scaling behavior.

```kql
.alter-merge table RawData policy caching hot = (0d)
```

avoids uncontrolled hot cache growth that triggers cluster scale-up and additional CU charges.

#### ALM Process Flow in the Architecture

Putting it together:

1. Developer Workflow:

   - Schema and object definitions authored in KQL → exported via .show database schema → checked into Git.
   - Other fabric items are created in the Web UI or through Visual Studio Code.

2. CI Pipeline:

   - Changes validated via API or direct deployment into a dev workspace.
   - Use of API payloads or Git sync to apply schema and metadata.

3. CD Pipeline:
   - Deployment pipelines promote artifacts from Dev → Test → Prod.
   - Declarative definitions ensure environment-specific rebinding without manual adjustments (e.g., Eventhouse IDs rebinding via logical ID resolution).

Integration with external DevOps tooling (e.g., Azure DevOps pipelines, GitHub Actions) optionally calls Fabric REST APIs for advanced orchestration.

### Technical deep dive

In this section, we examine the mechanics and internals of how CI/CD and ALM are implemented for Real-Time Intelligence workloads in Microsoft Fabric, with a focus on Eventhouse, KQL Database, Event Streams, and their integration into deployment pipelines and Git.

#### How Fabric Serializes and Deploys RTI Artifacts

At the technical core, Fabric’s CI/CD architecture relies on artifact serialization into a platform-defined schema, stored in Git. Each RTI artifact (e.g., Eventhouse, KQL Database, Event Stream) is exported into a set of structured files per artifact:

- **platform.json:** metadata about the artifact type, logical ID, display name
- **properties.json:** configuration like caching policy, retention, read/write flags
- **database.csl:** the KQL script representing schema and objects

Here are some examples for different artifact serialization files

**platform.json of a KQL Database**

This file describes the Fabric Metadata of the database.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "KQLDatabase",
    "displayName": "coffee_eh",
    "description": "coffee_eh"
  },
  "config": {
    "version": "2.0",
    "logicalId": "f2b03543-ffb1-9033-4369-aeff4ecb0eed"
  }
}
```

**DatabaseProperies.json of a KQL Database**

This file describes the database.

```json
{
  "databaseType": "ReadWrite",
  "parentEventhouseItemId": "cb651031-2912-bfac-407d-5d7da329becb",
  "oneLakeCachingPeriod": "P36500D",
  "oneLakeStandardStoragePeriod": "P36500D"
}
```

**DatabaseSchema.kql**

This file creates the assets within the KQL Database.

```kql
// KQL script
// Use management commands in this script to configure your database items, such as tables, functions, materialized views, and more.


.create-merge table BronzeCoffee (eventType:string, eventID:string, timestamp:string, machine_id:long, user:string, cup_size:string, strength:string, milk_added:string, sugar_packets:long, flavor_syrup:string, temperature:long, refill_required:long, beans_left_percentage:long, water_level_percentage:long, milk_level_percentage:long, used_grounds_container_full:long, cleaning_needed:long, usage_time:string, last_cleaning_date:string, next_scheduled_cleaning:string, filter_status:string, coffee_type:string, EventProcessedUtcTime:datetime, PartitionId:long, EventEnqueuedUtcTime:datetime)
.create-merge table BronzeMaintenance (eventType:string, eventID:string, timestamp:string, machine_id:long, user:string, cup_size:string, strength:string, milk_added:string, sugar_packets:long, flavor_syrup:string, temperature:long, refill_required:long, beans_left_percentage:long, water_level_percentage:long, milk_level_percentage:long, used_grounds_container_full:long, cleaning_needed:long, usage_time:string, last_cleaning_date:string, next_scheduled_cleaning:string, filter_status:string, coffee_type:string, EventProcessedUtcTime:datetime, PartitionId:long, EventEnqueuedUtcTime:datetime)
.create-merge table SilverCoffee (eventID:string, timestamp:datetime, machineid:int, user:string, cup_size:string, strength:string, milk_added:bool, sugar_packets:int, flavor_syrup:string, temperature:int, beans_left_percentage:int, water_level_percentage:int, milk_level_percentage:int, used_grounds_container_full:int, usage_time:string, coffee_type:string)
.create-merge table SilverMaintenance (eventID:string, eventDate:datetime, machineid:int, beans_left_percentage:int, water_level_percentage:int, milk_level_percentage:int, used_ground_container_full:int, last_cleaning_date:datetime, next_scheduled_cleaning:datetime, filter_status:string)
.create-or-alter function with (folder = "Bronze to Silver Transformations", skipvalidation = "true") prepareCoffee() {
BronzeCoffee
| project
    eventID,
    todatetime(timestamp),
    machineid = toint(machine_id),
    user,
    cup_size = cup_size,
    strength,
    milk_added = tobool(milk_added),
    sugar_packets = toint(sugar_packets),
    flavor_syrup,
    temperature = toint(temperature),
    beans_left_percentage = toint(beans_left_percentage),
    water_level_percentage = toint (water_level_percentage),
    milk_level_percentage = toint(milk_level_percentage),
    used_grounds_container_full = toint(used_grounds_container_full),
    usage_time,
    coffee_type
}

...
```

**Key behavior:**

The `.show database schema` command is used behind the scenes to export the KQL schema as .kql script, which includes:

- Table creation
- Materialized views
- Update policies
- Functions
- Permissions

This declarative schema is idempotent: reapplying it will create/update without duplication.

<div class="important" data-title="Importanz">

> Deletions are not propagated—removing a table from the schema file won’t drop it in the workspace. Deletions must be handled manually or scripted explicitly.

</div>

#### How API Deployments Work Internally

Fabric exposes REST APIs for automation. Most of the Create functions also accept a definition file as payload, for example [Items - Create KQL Database](https://learn.microsoft.com/en-us/rest/api/fabric/kqldatabase/items/create-kql-database?tabs=HTTP#create-a-readwrite-kql-database-with-definition-example). As seen in the next code block you can pass the three files `DatabaseProperties.json`, `DatabaseSchema.klq` and `.platform` as InlineBase64 Strings.

```html
POST https://api.fabric.microsoft.com/v1/workspaces/cfafbeb1-8037-4d0c-896e-a46fb27ff229/kqlDatabases { "displayName": "KQLDatabase_1", "description": "A KQL database description.", "definition": { "parts": [ { "path": "DatabaseProperties.json", "payload": "ewogICJkYXRhYmFzZVR5cGUiOiAiUmVhZFdyaXRlIiwKICAicGFyZW50RXZlbnRob3VzZUl0ZW1JZCI6ICI1YjIxODc3OC1lN2E1LTRkNzMtODE4Ny1mMTA4MjQwNDc4MzYiLAogICJvbmVMYWtlQ2FjaGluZ1BlcmlvZCI6ICJQMzY1MDBEIiwKICAib25lTGFrZVN0YW5kYXJkU3RvcmFnZVBlcmlvZCI6ICJQMzY1MDBEIgp9", "payloadType": "InlineBase64" }, { "path": "DatabaseSchema.kql", "payload": "Ly8gS1FMIHNjcmlwdAovLyBVc2UgbWFuYWdlbWVudCBjb21tYW5kcyBpbiB0aGlzIHNjcmlwdCB0byBjb25maWd1cmUgeW91ciBkYXRhYmFzZSBpdGVtcywgc3VjaCBhcyB0YWJsZXMsIGZ1bmN0aW9ucywgbWF0ZXJpYWxpemVkIHZpZXdzLCBhbmQgbW9yZS4KCi5jcmVhdGUtbWVyZ2UgdGFibGUgTXlMb2dzIChMZXZlbDpzdHJpbmcsIFRpbWVzdGFtcDpkYXRldGltZSwgVXNlcklkOnN0cmluZywgVHJhY2VJZDpzdHJpbmcsIE1lc3NhZ2U6c3RyaW5nLCBQcm9jZXNzSWQ6aW50KQ==", "payloadType": "InlineBase64" }, { "path": ".platform", "payload": "ZG90UGxhdGZvcm1CYXNlNjRTdHJpbmc=", "payloadType": "InlineBase64" } ] } }
```

On invocation, the backend:

- Decodes the script
- Executes it on the target Eventhouse/KQL Database
- Registers the artifact into the workspace metadata catalog
- Applies platform-level properties (e.g., caching policy)

This pattern enables infrastructure-as-code style deployments without using the GUI, aligning with DevOps practices.

Technically, these APIs mirror what Git integration does internally: both result in executing a .csl schema script and applying associated metadata.

#### How Git Integration Sync Works Internally

Git integration uses a pull-based sync model, operating bidirectionally:

**Commit workflow (Fabric → Git):**

1. Fabric detects changes to artifacts (schema, properties).
2. Fabric exports updated artifacts into serialized files.
3. Commits the folder structure to the configured Git repo.

**Update workflow (Git → Fabric):**

1. Fabric monitors the Git repo for changes.
2. Compares serialized files to current workspace state.
3. On update, parses .csl schema and properties.json.
4. Executes schema in target environment.
5. Updates platform metadata.

<div class="info" data-title="info">

> Fabric uses logical IDs inside platform.json to map artifact dependencies across environments:
>
> - Enables Eventhouse ID rebinding when promoting KQL DB from Dev → Test → Prod
> - Prevents schema referencing hard-coded IDs from other environments

</div>

<div class="warning" data-title="Technical Limitation">

> Current technical limitation: database-level properties like streaming policies are not yet included in Git sync (must be manually applied or scripted).

</div>

#### How Deployment Pipelines Work

Deployment pipelines in Fabric function similarly to Git integration, but without an external repository:

1. Each stage (Dev, Test, Prod) corresponds to a Fabric workspace.
2. Artifacts are promoted workspace-to-workspace, with the platform comparing serialized definitions.
3. Only additive/non-destructive updates are applied.
4. Platform uses logical ID mapping to reconnect references (e.g., KQL DB → Eventhouse binding).

Under the hood, Fabric reuses the same schema execution engine as the Git integration sync.

<div class="info" data-title="Key technical insight">

> There is no differential SQL or schema diff engine like SSDT/Visual Studio Database Projects — changes are applied by rerunning declarative scripts.

</div>

#### Capacity and Scaling Mechanics

A critical technical factor for RTI deployments is understanding how Eventhouse scales and costs:

- Scaling driven primarily by hot cache size, not query volume.
- Capacity auto-scales up when hot cache utilization exceeds thresholds (e.g., ~90%), scales down under ~70%.
- Minimum consumption ("Always On") pins cluster at baseline cores (e.g., 2 cores minimum).
- Billing is uptime-based: compute is billed per active core, not per query or per ingestion.

**Implication for CI/CD:**

Caching and retention policies must be explicitly set in deployment scripts to avoid auto-scale drift and cost overrun.

```kql
.alter-merge table RawData policy caching hot = (0d)
.alter-merge table RawData policy retention softdelete = (30d)
```

Without explicit settings, default policy (`hot = forever`) causes cache buildup → triggers scale-up → increases compute charges.

#### Known Technical Gaps and Workarounds

- **No schema-diff support:** Developers must handle schema evolution manually or by maintaining scripts external to Git sync. Fabric will not drop artifacts based on Git diffs.
- **No per-query/per-ingestion cost attribution:** Monitoring cost impacts must rely on capacity usage (CU/s) metrics rather than query-level cost.
- **Capacity App limitations:** Currently offers limited troubleshooting capability; advanced users must query diagnostic tables via .show cluster diagnostics and .show tables details for visibility into scaling triggers.
- **Partial artifact sync:** Some properties (e.g., database-level streaming policy) not synced; recommend setting such properties in schema scripts or manual deployment.

#### CI/CD Flow Internals

Putting it all together, here’s the technical flow when deploying a KQL Database via Git or API:

**1. Development** - Author schema via GUI or KQL scripts. - Connecting Workspace to Git Repo - Changes are automatically synced to git

**2. Sync/Deployment** - Git integration or API parses serialized files. - Platform resolves logical IDs → binds artifacts. - Executes schema script → creates/updates tables, views, policies. - Updates platform properties (caching, retention).

**3. Promotion (Pipeline)** - Schema and properties synced workspace-to-workspace. - Logical IDs rebinding ensures correct dependency mapping. - No destructive changes propagated; deletions require manual intervention.

### Implementations

### Troubleshooting

### Orchestration and optimization

### Schemas and throughput

### Monitoring and pricing

### Hands-on lab

---
