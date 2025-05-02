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

Implementing Continuous Integration and Continuous Deployment (CI/CD) in Microsoft Fabric for Real-Time Intelligence (RTI) workloads involves selecting a workflow that aligns with your team's development practices and deployment requirements. Microsoft Fabric supports multiple CI/CD strategies, each catering to different organizational needs.

#### Option 1: Git-Based Deployments with Multiple Branches

In this approach, each environment stage—Development, Test, and Production—corresponds to a dedicated branch in your Git repository.

Workflow:

1. Developers commit changes to the Development branch.
2. Upon approval, a release pipeline deploys updates to the Development workspace using Fabric Git APIs.
3. Changes are merged into the Test branch, triggering deployment to the Test workspace.
4. After successful testing, changes are merged into the Production branch for final deployment.

Considerations:

- Suitable for teams following Gitflow branching strategies.
- Ensures clear separation between environments.
- Requires managing multiple branches and coordinating merges.

#### Option 2: Git-Based Deployments Using Build Environments

This method utilizes a single main branch, with build and release pipelines handling environment-specific configurations.

**Workflow:**

1. Changes are committed to the main branch.
2. A build pipeline creates a build environment, runs tests, and adjusts configurations (e.g., data source connections) for the Development stage.
3. A release pipeline deploys the adjusted artifacts to the Development workspace.
4. The process repeats for Test and Production stages, with necessary configuration adjustments at each step.

**Considerations:**

- Ideal for teams following trunk-based development.
- Allows dynamic configuration per environment.
- Requires scripting to handle environment-specific adjustments.

#### Option 3: Deployments Using Fabric Deployment Pipelines

Fabric's built-in deployment pipelines facilitate direct promotion of artifacts between workspaces without relying solely on Git branches.

**Workflow:**

1. Developers commit changes to the main branch connected to the Development workspace.
2. Upon approval, Fabric deployment pipelines promote changes from Development to Test, and subsequently to Production workspaces.
3. Automated and manual tests can be integrated at each stage.

**Considerations:**

- Simplifies deployment by managing promotions within Fabric.
- Useful when Git is primarily used for development, and deployments are managed within Fabric.
- Provides features like deployment history and change tracking.

#### Option 4: CI/CD for ISVs Managing Multiple Customers

Independent Software Vendors (ISVs) serving multiple customers can adopt a CI/CD approach that accommodates multi-tenant deployments.

**Workflow:**

1. A centralized development process handles common features.
2. Build and release pipelines adjust configurations for each customer (e.g., data connections) using scripts or APIs.
3. Deployments are executed in parallel across customer-specific workspaces.

**Considerations:**

- Suitable for managing numerous customer environments.
- Requires handling customer-specific configurations dynamically.
- Demands careful coordination to ensure consistency across deployments.

Selecting the appropriate CI/CD strategy in Microsoft Fabric depends on factors such as team structure, development practices, and deployment complexity. Each option offers distinct advantages, and organizations may adopt a hybrid approach to best meet their needs.

#### Implementation: CI/CD with the REST API

While Microsoft Fabric provides Git integration and deployment pipelines as first-class CI/CD tools, direct use of the Fabric REST API offers maximum control and flexibility for advanced automation scenarios. This approach is especially valuable for:

- Fine-grained deployment orchestration across environments
- Integrating Fabric into existing enterprise CI/CD pipelines (e.g., Azure DevOps, GitHub Actions, Jenkins)
- Dynamic deployments where artifact definitions are generated or transformed at runtime

This implementation guide explains how to leverage the REST API for managing Eventhouse, KQL Databases, and Event Streams in Real-Time Intelligence workloads.

<div class="info" data-title="information">

> In the example we use PowerShell. The same is possible with any other language that can call REST Apis.

</div>

##### Understanding the API Model

Fabric’s REST API follows a declarative artifact model:

- Every deployable item (Eventhouse, KQL Database, Event Stream) is treated as an “item” in the workspace.

Creation is performed by POSTing an "item definition", which includes:

- platform.json metadata (type, name, logical ID)
- properties.json configuration (caching, retention)
- In case of a KQL Database A CSL schema script encoded in Base64 (the actual KQL schema)

The REST API exposes endpoints to:

- Create items
- Retrieve item definitions
- Update items
- Delete items
- Manage item properties

##### Deploying a KQL Database via REST API

A typical deployment flow for a KQL Database looks like this:

**Step 1: Export the schema**

Use KQL command in your dev workspace:

```kql
.show database schema
```

Save the output .csl file.

This script contains:

- create table
- create materialized-view
- alter-merge policy
- create function
- permissions

**Step 2: Encode schema**

Encode the .csl schema file as Base64:

```powershell
$schemaText = Get-Content "C:\path\schema.csl" `
                    -Raw

$schemaBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($schemaText))
```

**Step 3: Prepare API payload**

Construct the JSON body:

```powershell
$body = @{
  "displayName": "MyDatabase",
  "type": "KQLDatabase",
  "properties": {
    "readOnly": false,
    "hotCachePeriod": "30d"
  },
  "definition": "<Base64 schema string>"
} | ConvertTo-Json `
        -Depth 2
```

Adjust properties to set caching and retention.

**Step 4: Call the API**

Invoke the REST API endpoint:

```powershell
$WorkspaceID = '<GUID>'

$uri = "https://api.fabric.microsoft.com/workspaces/$workspaceId/items"

$response = Invoke-RestMethod `
                    -Headers @{ Authorization = "Bearer $token" } `
                    -Method POST `
                    -Uri $uri `
                    -Body ($body) `
                    -ContentType "application/json"
```

- This creates the KQL Database, schema, and configuration declaratively.

##### Updating an Existing Database

- Use PUT or PATCH API with updated definition payload.

<div class="important" data-title="important">

> Changes are additive; deletions (dropping tables/columns) must be explicitly scripted in the .csl schema.
> API doesn’t automatically diff schema or remove objects.

</div>

##### Automating Across Environments

To deploy across Dev → Test → Prod:

1. Parameterize workspace IDs and environment-specific configurations in your CI/CD pipeline.
2. Use the same API payload, adjusting displayName or properties as needed.
3. Map logical IDs in platform.json to maintain artifact dependencies (e.g., Eventhouse binding).

Implement validation after deployment by querying:

```kql
.show cluster
.show database schema
.show tables details 5. Advantages and Considerations

```

**Advantages:**

- Full control over deployment sequencing
- Can integrate with any CI/CD orchestrator
- Supports dynamic generation of schema
- Decouples from Git integration

**Considerations:**

- Requires manual schema diffing for destructive changes
- No built-in rollback; must implement idempotent scripts
- Requires authentication handling (OAuth token acquisition)

##### Implementation Example: End-to-End Flow

1. Developer commits schema .csl to Git.

2. CI pipeline:

- Pulls schema from Git
- Encodes schema to Base64
- Builds JSON API payload
- Calls `POST /items` API for Dev workspace

3. Automated tests validate schema + queries in Dev.
4. If passed, same pipeline deploys to Test → Prod via REST API.

Implementing CI/CD for Fabric RTI using the REST API provides maximum flexibility and environment control. It aligns with Infrastructure-as-Code principles by deploying declarative definitions via API calls, supporting dynamic, automated deployments independent of Git integration or built-in deployment pipelines.

**Recommended for:**

- Enterprise DevOps teams integrating Fabric into existing CI/CD stacks
- ISVs deploying into multiple customer tenants
- Scenarios requiring dynamic schema generation or transformation at deployment time

### Troubleshooting

Implementing CI/CD and ALM in Microsoft Fabric Real-Time Intelligence introduces new operational challenges. Troubleshooting deployment issues requires a deep understanding of how Fabric manages artifacts, schema, and deployment state across environments.

This section provides actionable guidance for diagnosing and resolving common issues in Git integration, deployment pipelines, REST API deployment, and schema management.

#### Git Integration Issues

##### Issue: Uncommitted or Out-of-Sync Artifacts\*\*

**Symptoms:**

- Artifact shows as Uncommitted or Update Required in Git integration view.
- Unable to sync changes from Git or push to Git.

**Root Causes:**

- Artifact modified directly in workspace but not committed to Git.
- Manual edits in Git repository not reflected in Fabric workspace.
- Branch mismatch or merge conflicts in Git.

**Resolution:**

- Use Source Control → Commit in Fabric to push local changes to Git.
- Use Source Control → Update to pull latest changes from Git into workspace.
- Verify correct Git branch is connected in Workspace Settings → Git Integration.
- Check Git repo permissions and authentication.

<div class="tip" data-title="tip">

> Avoid manual edits to platform.json or properties.json unless you understand schema-binding dependencies (e.g., logical IDs).

</div>

##### Issue: Missing or Incomplete Artifact Definitions in Git

**Symptoms:**

- Some artifacts missing in Git repo.
- Missing schema updates in database.csl.

**Root Causes:**

- Certain database-level properties (e.g., streaming policies) not yet supported by Git integration export.
- Artifact created outside Git-connected workspace.

**Resolution:**

- Validate schema export with .show database schema to compare definitions.
- For unsupported properties, use post-deployment scripts via REST API or manual configuration.
- Recreate artifact inside Git-connected workspace.

#### Deployment Pipeline Issues

##### Issue: Artifact Not Deploying to Target Workspace

**Symptoms:**

- Deployment pipeline shows Update Required but does not apply changes.
- Target workspace does not reflect promoted changes.

**Root Causes:**

- Artifact dependencies not resolved (e.g., KQL Database missing binding to Eventhouse).
- Logical ID mismatch between source and target workspace.
- Manual changes in target workspace creating drift.

**Resolution:**

- Inspect logical IDs in platform.json to confirm mappings.
- Use Fabric UI to manually bind KQL Database to correct Eventhouse if automatic rebinding fails.
- Reset workspace state by redeploying from clean Git source.
- Check deployment pipeline logs for skipped artifacts.

<div class="tip" data-title="tip">

> Deployment pipelines are non-destructive: deletions in source workspace or Git are not automatically deleted in downstream environments.

</div>

#### REST API Deployment Issues

##### Issue: API Call Fails with Validation Error

**Symptoms:**

- 400 Bad Request or validation error when calling POST /items.
- Error referencing missing schema, invalid payload, or undefined references.

**Root Causes:**

- Invalid Base64-encoded schema string.
- Required fields missing in payload (displayName, type, properties).
- Artifact dependencies unresolved (e.g., Eventhouse ID missing for KQL Database).

**Resolution:**

- Validate Base64 schema by decoding and manually inspecting KQL.
- Use .show database schema output to regenerate accurate schema.
- Ensure platform.json includes valid logicalId and correct parent references.
- Test schema manually in development workspace before API deployment.

##### Issue: Deployment Succeeds but Schema Not Applied

**Symptoms:**

- API call returns 200 OK but target workspace missing tables, views, or policies.

**Root Causes:**

- Schema script missing create table / create materialized-view statements.
- Schema execution partial or skipped due to dependency errors.
- Platform applies artifact definition without executing invalid schema.

**Resolution:**

- Confirm .csl schema includes complete DDL statements.
- Check .show database schema violations for broken dependencies.
- Run schema manually in KQL editor to validate before encoding.

<div class="tip" data-title="tip">

> The REST API executes schema declaratively; any failed statement does not stop deployment but silently fails downstream schema objects.

</div>

#### Schema Drift and Object Violations

##### Issue: Materialized Views or Update Policies Broken

**Symptoms:**

- Queries referencing materialized views fail.
- Update policies no longer execute.

**Diagnostic Command:**

```kql
.show database schema violations
```

**Common Causes:**

- Upstream table schema changes breaking dependent objects.
- Dropped columns or renamed fields without updating dependent objects.
- Manual schema changes bypassing deployment process.

**Resolution:**

- Rebuild broken objects using corrected schema in .csl.
- Add schema evolution scripts alongside declarative schema to manage object drops/renames.

**Best Practice:**

- Always validate schema with `.show database schema violations` after deploying schema changes via Git or API.

#### Capacity and Scaling-Related Troubleshooting

Although not CI/CD-specific, capacity issues can block deployments in Real-Time Intelligence workloads:

**Symptoms:**

- Auto-scaling causes throttling.
- Deployment blocked due to insufficient capacity.

Queries slow or failing after deployment.

```kql
.show cluster
.show cluster diagnostics
.show tables details
```

**Resolution:**

- Adjust table-level caching policy via .alter-merge to reduce hot cache pressure.
- Monitor capacity via Capacity App.
- Scale minimum cluster capacity if always-on or minimum consumption enabled.

<div class="tip" data-title="tip">

> Include caching and retention policies explicitly in .csl schema to control capacity impacts at deployment.

</div>

#### Summary of Troubleshooting Strategies

- Use Fabric UI, Git repo inspection, and REST API response logs as primary sources of troubleshooting evidence.
- Validate schema at each stage (Dev, Test, Prod) using `.show database schema` and `.show database schema violations`.
- Understand that Fabric’s deployment model is additive, non-destructive: drift and undeployed deletions require manual intervention.
- Document and maintain migration scripts for schema evolution outside declarative .csl schema.

This troubleshooting guidance ensures that CI/CD and ALM implementations for RTI in Microsoft Fabric remain resilient, transparent, and auditable across environments.

### Hands-on lab

---
