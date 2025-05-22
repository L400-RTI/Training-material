# L400 Hands-On Lab

## Setup

- Validate Access
- Create Workspace
- Create Eventhouse*

  *To accelerate the process of the Eventhouse and Eventstream creation, you can use the following script to deploy those items: [L400 Training Setup.ipynb](https://github.com/L400-RTI/Training-material/blob/main/HOL/setup/L400%20Training%20Setup.ipynb)

## Real-Time Hub

### Exercise:

- Create a new subscription to the Fabric Workspace Item Events using the Real-Time Hub and send events to your Eventhouse.

- Create an activator item directly in the Eventstream and configure a an activity rule on the item. You choose what the rule is.

### Expected Outcome:

- Eventstream
- Eventhouse table
- Activator

## Connectors

### Exercise:

- Create a connection to the connectionstring “L400-SalesOrder-EventHub" (connection contains SalesOrders)

- Route the data using the “rapidDelivery” property and save each stream to your Eventhouse with the most performant ingestion mode.

- The Datasource TruckLocations is streamed to an EventHub. Use the notebook “Generate Truck Data” to generate data and save the data using an Eventstream to your Eventhouse.

### Expected Outcome:

- Two eventstreams (SalesOrders and Truck Locations)
- Three Eventhouse tables (RapidDelivery, NotRapidDelivery, TruckLocations)

## Ingestion

### Exercise:

- Create an accelerated shortcut to the Customer table

  - Lakehouse: AdventureWorksDW
  - Table: dbo.Customers
  - Verify that the acceleration has completed

- Create a shortcut to the Customer table without Query Acceleration

  - Lakehouse: AdventureWorksDW
  - Table: dbo.Customers

- Create an external table against the FabrikamCustomer table in the SQL DB

  - Server: pragmaticworkspublic.database.windows.net
  - Databse: AdventureWorksDW"
  - Table: dbo.FabrikamCustomers
  - User: PWStudent
  - PW5tud3nt

- Create shortcut for the following tables in the lakehouse:

  - Lakehouse: AdventureWorksDW
  - Tables:
    - `dbo.DeliveryTruck`
    - `dbo.DeliveryTruck`
    - `dbo.Products`
    - `dbo.ResellerInventory`
    - `dbo.Resellers`

- Read data from JSON file to Eventhouse

  - In this task, you will build an ingestion process directly in the KQL database. So, no use of Eventstream, shortcuts or other "built-in" connectors.
  - The JSON file has a floating schema, and the existing schema is as follows:
    `{ ProductKey ,age ,name ,email ,phone ,address ,about ,registered ,latitude ,longitude ,tags ,friends ,greeting ,favoriteFruit }`

- Your task is:

  - Create a connection to the JSON file and make sure to expand the needed business columns from the JSON file.
  - The needed buisness columns are:
    - Name
    - email
  - For all other columns, the JSON payload must be loaded to the KQL database in the same table.
  - Every new key-value pair from the JSON must also be accepted in the connection and be stored in the destination table
  - Use [this file](https://github.com/L400-RTI/Training-material/blob/main/modules/assets/datafiles/import.json) to complete the task described above.

- Build ingestion with a mapping transformation of a JSON file

- Using the JSON file from the Module 3 - connectors, import the file using mapping transformations which does the following:

- Drop the 3 columns: friends, registered and favoriteFruit

- Ingest the rest of the columns as normal "exploded" columns - one for each key/value pair

- Handles any changes in the future structure of the file and makes sure to add a new column which holds new key/value pairs in case of schema drift

- You can find the file [here](https://github.com/L400-RTI/Training-material/blob/main/modules/assets/datafiles/import.json).

### Expected Outcome:

- Customer tables: 2 shortcuts and an external table on the same data

- Shortcuts for 4 remaining tables

- Table containing mapped JSON data (fruits/customer)

## Data Model

### Exercise

- Update Policies and Materialized Views

  - Move the “SalesOrder” and “TruckLocations” data tables to a “Bronze” folder.

  - Create Update Policies from “SalesOrder” and “TruckLocations” data tables and assign them to a “Silver” folder

  - Create Materialized Views against the “Silver” data

    - Last sale per customer
    - Sales aggregated by hour

  - Come up with the transformations of the Update Policies and the aggregations of the Materialized Views

- Compare the performance of the different external table options for Customer

- Build some queries against the Silver tables and Materialized Views, check the statistics of the queries and compare them

- Create some partition policies on “SalesOrder” and “TruckLocations” data

  - What would be the recommended partition columns and values?

  - Check extents statistics

- Create some KQL queries with different Joins and Join Hints

  - Look at the statistics

- Explore the diagnostic commands that we have in Eventhouse

  - .show ingestion failures

  - .show materialized-views

  - .show queries

  - .show operations

  - .show extents

  - .show cluster

  - .show diagnostics

- Explore which other commands we can use with .show

### Expected Outcomes:

- Two tables in Bronze folder

- Two tables in Silver folder from update policies

- Two materialized views

## Analytics

### Exercise

**Geospatial analytics on data**

- Using the ingestion made in Module 3, use the same dataset to do the following:

- Calculate the clustering of latitude and longitude of the dataset, grouped by the [H3](https://h3geo.org/) algorithm in resolution 10. Return the number of observations

  - Select a random H3 cell and calculate the H3 center

- Given the two points in the world

  - Lat: 51 Long: 0 (Heathrow, London)

  - Lat: 47 Long: -122 (Redmond, Seattle)

  - Calculate the shortest route between the two points as if it was an airline calculating the route to save fuel.

**Anomaly detection and forecasting**

- Create a standalone KQL queryset and connect to the Azure Data Explorer help cluster and the database SampleLogs

- Use the table RawSysLogs

- You are interested in the avg_cpu_percent by timestamp

- Create a timeseries by make-series using 10 Minute bins and plot a timechart

- FInd a spike and focus on the spike (shrink the timespan and the bins), rerender the timechart again

- Count the exceptions in this timespan

- Sample

### Expected Outcome:

- A KQL Queryset with the different queries and visualisations

## Dashboard

- Create a Real-Time Dashboard with the following structure:

  - Number of orders
  - Orders every 5min
  - A map with position from the Json import

- Create some interaction between the visualizations

- Make sure to re-use the base queries

### Expected Outcome:

- A Real-Time dashboard with 3 visuals

- Interactive filtering between at least three visuals

## Activator

### Exercises

- Create a Fabric Job Event to the “Generate Truck Data”, if the job stops, make it run the notebook again

- Create Activator with Factory Data

  - Create Eventstream for FactoryData

    - Use Event Hub Source
    - Select connection string “L400-FactoryData-EventHub”

  - Create an alert if the average temperature for the past 5min surpass 88ºC

### Expected Outcome:

- Two activators from this step, three in total
