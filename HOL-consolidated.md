## Startup script

To get started with all the labs in this training, you need to execute [this KQL script](/modules/assets/scripts/StartupKQL.txt) in a local Eventhouse in your workspace.

We expect you to be proficient in creating an Eventhouse and how to execute the provided script.

## Real-Time hub

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

## Connectors

### Ingest data from SQL server to Eventhouse

In this lab you will have the task to read data from a SQL server in Azure and be able to live query data from the SQL server and join it to data already existing in the KQL database.

### Situation

You are the Real-Time Intelligence developer of Fabricam and the infrastructure is built to have a Master Data services application in a SQL server. The SQL data is ingesting live and the business have the following requirements:

1. The Master Data from the SQL server must be read live
2. The SQL server has a table named Production.Product which must be used.
3. The KQL query must have a join with the Master Data to create the needed insights in a Real-Time Dashboard

Your task is to create a connection to the SQL server directly from the KQL engine (not using an Eventstream or one-time ingestion).

The information you have are the following:

SQL Server: pragmaticworkspublic.database.windows.net
Database: Adventureworks
SQL server username: PWStudent
SQL server password: PW5tud3nt

Stored procedure name: Production.Product

Create the connection to the SQL server in such a way that it can be used to live query data and joined in a KQL query for further processing.

Use the live connection to create a query which uses the newly created connection in a KQL statement. The statement can be made in your own liking, as long as it uses both data from the SQL server and the existing KQL database.

### Read data from JSON file to Eventhouse

In this task, you will build a ingestion process directly in the KQL database. So no use of Evenstrem, shortcuts or other "built-in" connectors.

The JSON file has a floating schema, and the existing schema is as follows:

{
ProductKey
,age
,name
,email
,phone
,address
,about
,registered
,latitude
,longitude
,tags
,friends
,greeting
,favoriteFruit
}

Your task is:

1. Create a connection to the JSON file and make sure to expand the needed business columns from the JSON file.
2. The needed buisness columns are:
   1. Name
   2. email
3. For all other columns, the JSON payload must be loaded to the KQL database in the same table.
4. Every new key-value pair from the JSON must also be accepted in the connection and be stored in the destination table

Use [this file](./modules/assets/datafiles/import.json) to complete the task described above.

## Ingestion

### Build ingestion with a mapping transformation of a JSON file

Using the file from the Module 3 - connectors, import the file using mapping transformations which does the following:

1. Drop the 3 columns: friends, registered and favoriteFruit
2. Ingest the rest of the columns as normal "exploded" columns - one for each key/value pair
3. Handles any changes in the future structure of the file and makes sure to add a new column which holds new key/value pairs in case of schema drift

You can find the file [here](/modules/assets/datafiles/import.json).

### Come up with a solution for ingesting large volume data and find the correct settings for all 3 areas of throughput

In pairs of two people, discuss and draw solutions to the 2 scenarios below. Present to the team to your right and discuss the differences in solutions.

1. Streaming data from Google pub/sub
   1. Data is streamed live from a website trafic
   2. Trafic is estimated to flow at a rate of 12.700 messages a second
1. JSON files from storage account
   1. JSON must be imported on a schedule - every 10 mins (filenames indicate the timestamp, take only the latest)
   2. JSON must be exploded for all elements of the key/value pairs
   3. Mapping of the JSON must be able to be used in other ingestion configurations on the same KQL database

## Analytics

### Geospacial analytics on data

Using the ingestion made in Module 3, use the same dataset to do the following:

1. Calculate the clustering of latitude and logitude of the dataset, grouped by the [H3](https://h3geo.org/) algorithm in resolution 10. Return the number of observations
2. Select two polygons from the above task and calcuclate the distance between the two in kilometers
3. Given the two points in the world
   1. Lat: 51.470020 Long: -0.454296 (Heathrow, London)
   2. Lat: 35.698700 Long: -97.494659 (Redmond, Seattle)
   3. Calculate the shortest route between the two points as if it was an airline calculating the route to save fuel.

### Anomaly detection and forecasting

Import [this file](/modules/assets/datafiles/art_load_balancer_spikes.csv) into your KQL database.

Create KQL statement which find and points out the anomolies found in the dataset.

Visualize the findings in a chart in the KQL statement.

### (Extra) Built-in datasets which can be used

Using the imported data set from module 3, try to play around with the convertion features. For instance between KG to stones, pounds, etc. Or from CM to Miles, Inches etc.

## AI and Copilot- Semantic Analysis and Reasoning on Delivery Truck Logs

Objectives

- Embed textual delivery incident logs, store vectors, and perform semantic similarity search
- Augment real-time data with AI reasoning for operational insights

### 1. Ingest Delivery Logs Dataset into Eventhouse

Load a structured dataset of delivery incident logs from trucks. Example log entries might include:

- "Delayed due to weather"
- "Route blocked"
- "Package not found"
- "Mechanical issue on vehicle"

Ingest the data into an Eventhouse table named `truck_logs`.

### 2. Generate Embeddings Using `ai_embeddings`

Use the `ai_embeddings` plugin to convert the `incident_description` column into vector embeddings:

```kusto
set async_execution = true;
truck_logs
| extend incident_vector = ai_embeddings("azure_openai_deployment_url", incident_description)
```

### 3. Store Vectors Using a `dynamic` Column

Ensure `incident_vector` is defined as a `dynamic` column in your table schema. This allows efficient storage and querying within Eventhouse.

Example KQL snippet to confirm or cast the column:

```kusto
truck_logs
| extend incident_vector = todynamic(incident_vector)
```

### 4. Perform Semantic Similarity Search

Use `vector_cosine_distance()` to find records similar to a new incident:

```kusto
let new_incident = "Road closed due to snowstorm";
let new_vector = ai_embeddings("azure_openai_deployment_url", new_incident);
truck_logs
| extend similarity = vector_cosine_distance(incident_vector, new_vector)
| top 5 by similarity desc
```

### 5. Summarize with `ai_chat_completion_prompt`

Use `ai_chat_completion_prompt` to generate a summary for dispatchers:

```kusto
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

```kusto
.export async to delta (h@"https://<your_onelake_url>/deliveries/embeddings") <|
truck_logs
| project TimeStamp, incident_description, incident_vector
```

> **Note**: Replace `azure_openai_deployment_url` and `azure_openai_chat_url` with your actual Azure OpenAI endpoint URLs.

## Dashboards - Drone Fleet Dashboard

**Objective:** Build and optimize a real-time dashboard for delivery vehicle telemetry.

### Tasks:

1. Ingest telemetry via Kafka connector into Eventhouse.
2. Design event and status table schema.
3. Use update policies to filter `status changed` events.
4. Build dashboard:
   - Page 1: Fleet summary, 60s refresh.
   - Page 2: Drillthrough per vehicle, 15s refresh.
   - Parameters: vehicle_id, region.
5. Use metrics tab to evaluate tile load.
6. Integrate with Activator to visualize alerts.

> **Tip:** Reuse parameter definitions across dashboards for consistency.
