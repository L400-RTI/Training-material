## Module 6 - Analytics

### Introduction

One of the huge benefits of the Kusto engine is the power to do complex analytics with a more simple approach than compared to other database engines.

This module can quiclky become huge if we are to dive into all aspects of the analytical capabilites in the KQL world.

We also do expect you to be proofecient in the KQL language, as you have already passed the DP-600 and DP-700 exams and passed the Applied Skils for Real-Time Intelligence.
Profeciencny to be able to work deeply with this level 400 training material is to know how to write KQL queries to handle:

- Time series
- Windowing functions
- Rendering
- Basic aggregration, manipulation and joins
- Entry level performance tuning

With that also to understand the Kusto engine, how it works and hwo the data is structured inside the engine. This is also dived into in module 5 for Data Modelling.

If you need to get up to speed, then here are some links for you to use:

- [Kusto Query Language (KQL) from Scratch - Pluralsight](https://www.pluralsight.com/courses/kusto-query-language-kql-from-scratch)
- [Data analysis with Kusto Query Language - Microsoft Learn](https://learn.microsoft.com/en-us/training/paths/kusto-query-language/)
- [Rod Trent's Must Learn KQL course](https://github.com/rod-trent/MustLearnKQL)
- [Kusto Detecive agency](https://detective.kusto.io/)
- [KQL common operators - Microsoft Learn](https://learn.microsoft.com/en-us/kusto/query/tutorials/learn-common-operators?view=azure-data-explorer&preserve-view=true)
- [KQL aggregations - Microsoft Learn](https://learn.microsoft.com/en-us/kusto/query/tutorials/use-aggregation-functions?view=azure-data-explorer&preserve-view=true)
- [KQL Geospacial visualizations - Microsoft Learn](https://learn.microsoft.com/en-us/kusto/query/tutorials/create-geospatial-visualizations?view=azure-data-explorer&preserve-view=true)

The KQL language leverages built-in functionalities like geospacial analytics, distance between two (or more) points, anomoly detection and forecasting, parsing data and handling JSON structures and much much more. All wohte implemented with one single line of code.

This capabilty is key to handle and master when working with the timeseries data and this module will dive deep into the possiblities and jump pass the basic knowledge like filters, row based calculations etc.

### Architectural deep dive

For the architectural context of this module, we will use the same information as the one from the Data modelling module.

### Technical deep dive

For the technical context of this module, we will use the same information as the one from the Data modelling module.

### Implementations

Each of the analytics capabilities from the Kusto engine is implemented with an ease-of-use perspective and is very often used in a "spoken language" format.

An example, before we dive into the details is the one used for IP-adress lookup to get the Latitude and Longitude of an IP-adress:

```kql
print ip_location = geo_info_from_ip_address('20.53.203.50')
```

Output:

| ip_location                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------- |
| {"country": "Australia", "state": "New South Wales", "city": "Sydney", "latitude": -33.8715, "longitude": 151.2006} |

As you see from above statement the _geo_info_from_ip_address_ is just as you would say it when you have a dialogue with another person.

We can't list all the capabitlities in this module, so we have chosen a list of functions and will walk you through each of them:

- Multivariate anomoly detection
- Scan operator
- Geospacial analytics
- Anomoly detection and forecasting
- JSON and XML parsing

#### Multivariate anomoly detection

Multivariate anomaly detection in Microsoft Fabric Real-Time Intelligence leverages advanced machine learning models to monitor and analyze data streams with multiple interrelated variables. Unlike univariate methods that track anomalies in a single metric, this technique detects patterns across correlated variables to identify subtle, complex anomalies that might otherwise go unnoticed. It continuously learns the normal behavior of these variables in real-time and flags deviations that are statistically or behaviorally abnormal, offering deeper insights into operational, business, or IT systems.

You can enable the built-in multivariate anomaly detection model by specifying a set of correlated metrics and a training window, after which Fabric automatically trains and applies the model. Configuration typically involves selecting key dimensions, defining a historical window for learning baseline behavior, and optionally tuning sensitivity thresholds. The system then produces an anomaly score or tag per time window, which can be visualized or acted upon through real-time dashboards, alerts, or downstream workflows.

When using this feature, it's crucial to ensure that the selected metrics are indeed correlated; feeding unrelated signals can degrade the accuracy of anomaly detection. Data quality is another critical factor—missing values, outliers, or inconsistent time stamps can distort the learning process. Additionally, model sensitivity should be carefully calibrated to avoid false positives or missed anomalies, especially in high-volume data environments. Monitoring model drift and periodically retraining with updated data can help maintain detection accuracy as system behaviors evolve over time.

Example usage of the multivariate anomoly detection can be found [here](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/multivariate-anomaly-detection)

##### Key capabilities

- Real-Time Processing
  - Detect anomalies on streaming data in real time, enabling instant insights and rapid response to unusual system or business behaviors.

- Multivariate Correlation Analysis
  - Analyzes multiple interrelated metrics simultaneously, allowing detection of complex anomalies that univariate methods might miss.

- No-Code Configuration
  - Integrates seamlessly with the Fabric Real-Time Analytics pipeline with minimal setup—ideal for users without deep data science expertise.

- Anomaly Scoring and Tagging
  - Outputs structured anomaly scores and tags, enabling easy integration into alerting systems, dashboards, or downstream automation.

- Customizable Sensitivity and Detection Windows
  - Allows tuning of detection sensitivity, historical training windows, and data granularity to optimize performance for different scenarios.

- Visual Anomaly Exploration
  - Enables visualization of detected anomalies across metrics and time windows using Microsoft Fabric dashboards and Power BI integration.

#### Scan operator

The Scan operator in Microsoft Fabric Real-Time Intelligence is a powerful construct used in Real-Time Analytics pipelines to perform stateful operations across streaming data. It processes each incoming event in sequence while maintaining contextual memory (state) across events, enabling users to compute running aggregates, detect patterns, or flag anomalies over time. Unlike stateless transformations, the Scan operator allows for evaluating each event in the context of prior events—making it ideal for use cases like session tracking, cumulative computations, and real-time monitoring scenarios where temporal or sequential logic is required.

To implement the Scan operator, users define a custom KQL-based expression within a streaming pipeline in Fabric. This expression typically includes a state declaration, initialization, update logic, and an optional output condition. When the pipeline runs, the Scan operator evaluates incoming events against the state logic in a user-defined, windowed, or continuous context. Developers can control how and when to emit results (e.g., only when a condition is met or on every event). The implementation is declarative and runs fully managed in Fabric, without requiring external compute resources or manual orchestration.

When using the Scan operator, attention must be paid to state management—improper or unbounded state can lead to performance issues or memory overhead. Also, because Scan operates on event order, ensure that the input stream is time-ordered or logically grouped to avoid inconsistent outputs. Careful design of initialization and update logic is critical to avoid incorrect accumulation or event leakage. Additionally, watch for edge cases such as null values or out-of-order events, and always test the operator with representative data to validate its real-time behavior before deploying to production.

##### Key capabilities

- Stateful Event Processing
  - Maintains and updates custom state across streaming events, enabling powerful context-aware logic.

- Windowed and Continuous Mode Support
  - Supports both fixed windows (time or event count) and continuous scanning, adaptable to various use cases.

- Event-Level Granularity
  - Operates on each individual event in real time, supporting high-frequency and low-latency data processing.

- Flexible Output Conditions
  - Emit results conditionally or on every event, supporting both event detection and continuous metric tracking.

- Support for Complex Event Processing
  - Useful for detecting sequences, computing rolling statistics, or implementing sessionization logic.

#### Geospacial analytics

Geospatial analytics in Kusto Query Language (KQL) enables powerful location-based querying and analysis across large datasets. Using native support for geographic data types such as points, polygons, and lines—expressed in formats like GeoJSON or KQL allows analysts to work with spatial data efficiently. Common use cases include asset tracking, service coverage validation, geofencing, and mobility trend analysis. Built-in functions like geo_point_in_polygon() and geo_distance_2points() provide mechanisms for spatial filtering and proximity calculations without the need for external geospatial tools.

KQL supports a range of spatial operations, allowing users to calculate distances between coordinates, test spatial relationships, and group spatial events by geohash for clustering or heatmap generation. For example, to find users within 1 kilometer of a store, you can use geo_distance_2points() to compare each user's coordinates against the store’s location. Similarly, geo_point_in_polygon() helps determine whether an event occurred within a defined geographic boundary, such as a delivery zone or security perimeter. These operations are often used in combination with filtering, aggregation, and time-based analysis to surface patterns or detect anomalies in spatial data.

To work effectively with geospatial data in KQL, it's essential to structure your input correctly—typically by packing coordinates into GeoJSON format using pack_array() and pack(). Queries can be extended further by generating geohashes using geo_point_to_geohash() for grid-based aggregation, useful for map visualizations. These capabilities integrate seamlessly with Azure dashboards and external tools like Power BI or Grafana, making it easy to visualize spatial insights in real-time. Whether you're monitoring vehicle routes or analyzing regional sales trends, KQL’s geospatial functions provide a scalable and expressive solution for location-aware analytics.

##### Key Capabilities

- Geospatial Data Types

  - geo_point: Represents a location using latitude and longitude.
  - geo_polygon: Represents a closed area using a list of geo points.
  - geo_line: Represents a series of connected points (e.g., a path).
  - These are typically stored as WKT (Well-Known Text) or GeoJSON strings.

- Distance and Proximity

  - geo_distance_2points(): Calculates the distance between two geo points in meters.
  - Use case: Track proximity of a mobile user to a point of interest (e.g., store, hospital).

- Spatial Relationships

  - geo_point_in_polygon(): Checks if a point lies within a polygon.
  - Use case: Determine if a delivery driver entered a restricted area or service zone.
  - geo_polygon_intersects_polygon(): Check if two regions overlap.

- Clustering and Grouping

  - Geohashing: KQL allows geohashing using geo_point_to_geohash(), grouping nearby points spatially.
  - Use case: Cluster user activity for heatmap generation or anomaly detection.

- Rendering and Visualization

With tools like Azure Monitor Workbooks or Power BI, results from KQL queries can be rendered on maps (e.g., choropleths, heatmaps, marker maps).

##### Common Use Cases and Example Queries

1. Calculate Distance Between Two Points

```kql
let point1 = dynamic({"type":"Point","coordinates":[-122.12, 47.67]});
let point2 = dynamic({"type":"Point","coordinates":[-122.33, 47.61]});
print DistanceInMeters = geo_distance_2points(point1, point2)
```

2. Filter Events Within a Radius

```kql
let center = dynamic({"type":"Point","coordinates":[-122.33, 47.61]});
let radius = 1000; // in meters
MyGeoTable
| extend location = pack("type", "Point", "coordinates", pack_array(longitude, latitude))
| where geo_distance_2points(center, location) <= radius
```

3. Check If a Point is in a Polygon

```kql
let polygon = dynamic({
  "type":"Polygon",
  "coordinates":[[
    [-122.35, 47.60], [-122.35, 47.70], [-122.20, 47.70], [-122.20, 47.60], [-122.35, 47.60]
  ]]
});
MyGeoTable
| extend location = pack("type", "Point", "coordinates", pack_array(longitude, latitude))
| where geo_point_in_polygon(location, polygon)
```

4. Cluster Events by Geohash

```kql
MyGeoTable
| extend geohash = geo_point_to_geohash(longitude, latitude, 5)
| summarize Count = count() by geohash
```

#### Anomoly detection and forecasting

Anomaly detection and forecasting in Kusto Query Language (KQL) are powerful tools for identifying unusual behavior and predicting future trends in time-series data. These capabilities are essential in use cases like application performance monitoring, security event detection, telemetry analysis, and resource usage forecasting. KQL provides native support for statistical methods such as moving averages, time series decomposition, and seasonality detection, which can be used in real-time or retrospective analysis of large-scale datasets.

At the core of anomaly detection in KQL is the series_decompose_anomalies() function, which helps identify statistically significant outliers in a dataset. When used in combination with make-series, you can transform rows of raw data into a time-aligned series, making it easier to apply anomaly detection and visualize deviations from expected behavior. For example, you can detect sudden spikes in CPU usage, traffic drops in a web service, or irregular transaction volumes over time. These functions are especially useful when analyzing metrics with strong periodic patterns, as they can account for trends and seasonality automatically.

For forecasting, KQL provides the series_decompose_forecast() function, which projects future values based on historical trends. This is particularly helpful for capacity planning and operational readiness, such as forecasting server load or estimating sales in upcoming weeks. By pairing forecasting with visualizations (e.g., time charts in Azure Monitor Workbooks or Power BI), teams can proactively identify capacity risks or set thresholds for alerting. Together, KQL’s anomaly detection and forecasting tools empower users to move from reactive monitoring to proactive analytics, reducing downtime and improving operational efficiency.

##### Key capabilities

1. Time-Series Preparation
   Before you can detect anomalies or forecast trends, you need to structure your data using make-series. This aggregates metrics over a time grain:

```kql
MyMetricsTable
| make-series avgCPU=avg(CPU_Usage) on Timestamp in range(startofday(ago(7d)), now(), 1h)
```

2. Anomaly Detection with series_decompose_anomalies()

This function flags values that deviate from the normal pattern:

```kql
MyMetricsTable
| make-series avgCPU=avg(CPU_Usage) on Timestamp in range(startofday(ago(7d)), now(), 1h)
| extend anomalies = series_decompose_anomalies(avgCPU, 3, -1, 'linefit')
```

- 3: sensitivity (lower means more anomalies)
- -1: auto-detect seasonality
- 'linefit': decomposition method

3. Forecasting with series_decompose_forecast()

You can predict future metric values using historical data:

```kql
MyMetricsTable
| make-series avgCPU=avg(CPU_Usage) on Timestamp in range(startofday(ago(14d)), now(), 1h)
| extend (forecast, lower, upper) = series_decompose_forecast(avgCPU, 24)
```

- 24: number of time bins to forecast into the future (e.g., next 24 hours)

#### JSON and XML parsing

Kusto Query Language (KQL) offers built-in capabilities for parsing and querying semi-structured data formats like JSON and XML, which are commonly found in logs, telemetry, and API responses. These features allow users to extract meaningful values from complex or nested data without needing to preprocess the data outside of KQL. JSON is particularly prevalent in modern cloud-native environments (e.g., application logs, Azure diagnostics), while XML may appear in legacy systems or structured logging frameworks.

For JSON data, KQL provides intuitive operators such as parse_json(), extractjson(), and dot notation (myjson.key1.key2) for navigating nested structures. This makes it easy to flatten and access deeply nested values, arrays, or dynamically structured content. XML parsing, while less flexible than JSON handling, is supported via the parse_xml() and extract() functions, which allow for basic XPath-style retrieval of nodes and values. These capabilities are useful for handling structured data in custom log formats, policy documents, or system configurations.

To work effectively with JSON and XML in KQL, it's important to understand the data schema and apply parsing functions at query time. For JSON, storing data as dynamic type allows KQL to interpret it as an object, enabling filtering, projection, and aggregation directly on nested fields. With XML, while deeper traversal requires more manual string manipulation, KQL still enables extraction of key values through regex and XPath-like expressions. These tools allow analysts to treat complex, semi-structured data as first-class queryable entities in their analytics workflows.

##### Key capabilities

1. JSON Parsing
   Example 1 – Parse a JSON string:

```kql
datatable(log: string)
[
  '{"user":"alice","action":"login","meta":{"ip":"192.168.1.1","device":"mobile"}}'
]
| extend log_json = parse_json(log)
| project user = log_json.user, ip = log_json.meta.ip, device = log_json.meta.device
```

Example 2 – Extract a value using extractjson():

```kql
MyLogs
| extend ipAddress = extractjson("$.meta.ip", logField)
Dot notation shortcut (when field is dynamic):
```

```kql
MyTable
| extend userAgent = myjsonfield.device.os
```

2. XML Parsing

Example – Extract value from XML using regex-style extract:

```kql
let xml = "<log><user>bob</user><action>logout</action></log>";
print user = extract("<user>(.*?)</user>", 1, xml)
```

Parsing XML into a structure (less common):

```kql
print data = parse_xml("<config><key>value</key></config>")
```

##### Working Tips

- Dynamic Columns: Store JSON as dynamic type in ingestion for efficient querying.
- Schema Discovery: Use print or take 1 to inspect raw nested structures.
- Performance: Avoid overusing extractjson() on large text fields—prefer parse_json() and project from dynamic.
- Validation: Use isnull() or typeof() to safely handle missing or malformed fields.
- XML Caution: XML parsing is less performant and lacks full XPath support—use for light or shallow parsing only.

### Hands-on lab

#### Geospacial analytics on data

Using the ingestion made in Module 3, use the same dataset to do the following:

1. Calculate the clustering of latitude and logitude of the dataset, grouped by the [H3](https://h3geo.org/) algorithm in resolution 10. Return the number of observations
2. Select two polygons from the above task and calcuclate the distance between the two in kilometers
3. Given the two points in the world
   1. Lat: 51.470020 Long: -0.454296 (Heathrow, London)
   2. Lat: 35.698700 Long: -97.494659 (Redmond, Seattle)
   3. Calculate the shortest route between the two points as if it was an airline calculating the route to save fuel.

#### Anomoly detection and forecasting

Import [this file](/modules/assets/datafiles/art_load_balancer_spikes.csv) into your KQL database.

Create KQL statement which find and points out the anomolies found in the dataset.

Visualize the findings in a chart in the KQL statement.

#### (Extra) Built-in datasets which can be used

Using the imported data set from module 3, try to play around with the convertion features. For instance between KG to stones, pounds, etc. Or from CM to Miles, Inches etc.

---
