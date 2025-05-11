# Module 8: Deep Dive into Real-Time Dashboards in Microsoft Fabric RTI

## 1. Introduction to the Module

This Level 400/500 module is designed for experienced practitioners of Microsoft Fabric Real-Time Intelligence. It explores advanced capabilities, performance tuning, and best practices in designing and operating real-time dashboards. This module is performance-focused, with real-world examples to help optimize your implementation and architecture. Where applicable, there are recommendations for optimizing cost while using real-time dashboards. 

## 2. Architectural Deep Dive

- **Source to Surface Flow:**
  - Data ingested via Eventstream, Event Hub, or connectors like Kafka into Eventhouse.
  - KQL Database used with materialized views and update policies used to filter and transform data.
  - Dashboards query prepared data through KQL, optimizing latency and performance using Eventhouse.

- **Core Architectural Elements:**
  - **KQL Database:** Fast, scalable, real-time query engine.
  - **Parameters and Filters:** Declarative, dynamic filtering.
  - **Continuous Refresh Engine:** User-configurable refresh intervals.
  - **Visual Layer:** Native Fabric integration for real-time UX.

- **Design Tip:** Use modular dashboard pages segmented by business role or scenario. Avoid overloading dashboards with generalized data. Real-time dashboards can and should be very lightweight, so ensure that the data presented is fit for purpose for the user.

## 3. Technical Deep Dive

- **Performance Considerations:**
  - Avoid filtering in Eventstream for high-frequency signals; prefer update policies in KQL.
  - Use "value changed" conditions instead of `value > threshold` for event-triggered tiles.
  - Limit visual complexity per tile and pre-aggregate where feasible.
  - Configure staggered auto-refresh (e.g., every 15s with 5s cooldown).

- **Advanced Configuration:**
  - Implement hierarchical parameters.
  - Use role-based access controls on dashboard editing and viewing.
  - Import/export dashboard configurations via JSON.

## 4. Implementations and Sharing

- **Use Case: Cold Storage Monitoring**
  - Use Activator to alert on state transitions, not continuous thresholds.
  - Dashboard tiles show real-time temperature with single-alert logic.

- **Use Case: Forza Telemetry**
  - Issue: Latency in gear shift visualization due to filtering in Eventstream.
  - Fix: Stream raw data into KQL and apply filtering via update policies.

- **Use Case: Drillthrough Capabilities**

## Drillthrough in Real-Time Dashboards

Drillthrough is a critical feature in real-time dashboards that enables users to move from aggregated, high-level visualizations to detailed, contextual views. While it is familiar to those with a Power BI background, it may be new to many Fabric users unfamiliar with Power BI. In the context of Real-Time Intelligence, drillthrough enhances operational decision-making by allowing users to investigate anomalies, diagnose root causes, and trace event trajectories without navigating away from the live environment.

Real-time dashboards typically present summary tiles—KPIs, charts, or alert counts—that reflect system-wide metrics. While these tiles provide visibility, they are insufficient when an operator needs to understand *why* a metric spiked or *which* entities contributed to a threshold breach. Drillthrough solves this by enabling context-sensitive navigation to pages filtered by selected values, such as device ID, site name, or event type.

Technically, drillthrough in Fabric dashboards is implemented using **parameters**. When a user clicks on a visual (e.g., a bar in a chart or a cell in a table), the dashboard captures that value and passes it to a target page as a parameter. That target page is preconfigured to filter its visuals based on that parameter—typically using KQL queries that reference it in `where` clauses. Multiple parameters can be passed, allowing for multi-dimensional filtering (e.g., region + device ID + alert type). Data exploration can be taken many different directions from here.

### Best Practices for Drillthrough

- **Predefine investigative paths:** Pages should be purpose-built for drillthrough, with visuals optimized for rapid root cause analysis (e.g., log tables, trace plots, recent state transitions).
- **Use parameter naming conventions:** Consistent parameter names help maintain query reliability and reduce debugging overhead across dashboards.
- **Limit parameter cardinality:** Avoid drillthrough on fields with millions of unique values unless accompanied by throttling or pagination mechanisms.
- **Pair with Activator diagnostics:** Drillthrough can lead directly to the history of an alert condition firing, displaying Activator rule evaluation logs or event payloads.

### Real-World Example

A common use case is in industrial IoT monitoring. A dashboard may show a count of temperature alerts per site. Clicking on a specific site can drill into a second page that shows a timeline of telemetry from that site, device-level diagnostics, and a table of recent alerts with timestamps and values. This provides operators with the immediate context needed to respond intelligently.

### User Experience Considerations

Drillthrough supports incident post-mortem workflows. By navigating from an event summary to historical logs and visual traces, analysts can reconstruct failure sequences and identify precursors to service disruptions.

It also minimizes context-switching and avoids overloading a single dashboard with excessive detail. It helps focus the post-morten investigation as well: users only see detail when they need it, and only for the entity they selected.


- **Use Case: Sharing via Organizational Apps**

In Microsoft Fabric, sharing real-time dashboards via organizational apps ("org apps") is a recommended practice for scalable, secure, and user-friendly distribution. Org  apps act as curated, packaged content collections that can include dashboards, reports, and datasets, all bundled with predefined navigation and access control settings. Org apps also help support an organization's goal of implementing enterprise-grade deployment and change management workflows.

By embedding real-time dashboards within an org app, admins can manage permissions centrally—ensuring viewers only see the pages and tiles relevant to their role. Dashboards within an app retain their configured functionality, including auto-refresh, parameterization, and drillthrough capabilities. The app shell provides an intuitive user experience with minimal onboarding friction, especially for business users unfamiliar with navigating to assets within the Fabric workspace model.

Versioning is another advantage. Updates to the app can be staged and validated in the background, then pushed to users without disrupting active sessions. Additionally, integrating dashboards into org apps supports governance workflows—such as requiring approval before app publishing—and allows telemetry tracking to monitor usage and performance to assist in capacity monitoring and planning.

**Best practices for sharing include:**
- Assigning view-only permissions for non-technical roles.
- Using workspace-based access to protect underlying datasets.
- Configuring dashboard refresh intervals conservatively to manage capacity consumption.

For customer-facing solutions, deploying dashboards through org apps ensures consistent branding and experience across tenants.


## 5. Troubleshooting

### Symptoms, Causes, and Recommended Corrections

- **Data not updating**
  - **Likely Causes:**
    - Misconfigured dashboard refresh intervals (e.g., set too infrequently or disabled).
    - Errors or latency in the underlying KQL query or data source (e.g., stale materialized views).
  - **Recommended Actions:**
    - Verify auto-refresh settings on the dashboard and page level.
    - Check the data source connection and validate the KQL query in the editor.
    - Ensure update policies or streaming ingestion are functioning as expected.

- **Unreadable time labels**
  - **Likely Causes:**
    - Low-resolution display (e.g., browser-based VM with 1024x768 or similar).
    - Overcrowded X-axis due to long time spans or dense time intervals.
  - **Recommended Actions:**
    - Shorten the default time range shown or use `bin()` to reduce label density.
    - Format date/time strings with abbreviations or rotate axis labels selectively.
    - Test dashboard responsiveness on lowest resolution display likely to be used and optimize the layout for that space.

- **Excessive cost**
  - **Likely Causes:**
    - Overuse of real-time auto-refresh, especially with short intervals (<10s).
    - High-cardinality queries or unfiltered scans over large datasets.
  - **Recommended Actions:**
    - Increase refresh interval or enforce a minimum refresh rate using dashboard settings.
    - Pre-aggregate metrics in KQL or materialize heavy queries to reduce runtime load.
    - Optimize filters to limit scan size (e.g., index predicates on time or ID dimensions).


- **Diagnostic Tools:**
  - KQL to track last update timestamps.
  - System monitoring dashboards to analyze tile query counts.

- **Creating a System Monitoring Dashboard for Real-Time Dashboards**

To create a system monitoring dashboard in Microsoft Fabric that provides visibility into dashboard tile behavior—such as query counts, refresh frequency, and performance—you'll first need to enable telemetry at the query level and then build a dashboard to visualize those insights.

Start by instrumenting each tile query with metadata that helps identify the dashboard and tile being executed. For example, you can append fields to each query that include the dashboard name, tile identifier, and a timestamp. These fields can be included using simple `extend` statements in KQL, which effectively tag each query for logging purposes.

Next, ensure diagnostic logging is enabled in the KQL database. This includes reviewing query logs, which may be accessed via internal monitoring commands or custom diagnostic tables. For more detailed performance analysis, consider enabling query tracing to capture execution metrics. These features help track query execution time, error rates, and data scanned—critical for understanding resource consumption over time.

If you're capturing this telemetry into a centralized table (note: this is recommended) —such as a `DashboardQueryLog`—you should define consistent fields like dashboard name, tile ID, user identity (if relevant), timestamp of execution, and duration. This table will serve as the foundation for your monitoring dashboard.

Once the log data is being captured, create a real-time dashboard that visualizes this data. Key visuals might include a time series visual showing how many queries are run per dashboard or tile over a given interval, bar charts ranking dashboards by their query load, and summary metrics such as average query duration. If you are having problems with "stale" dashboards, include visuals that show the most recent refresh timestamp per tile, which can help identify non-refreshing or failing visuals.

To keep this monitoring dashboard relevant, it is recommended to configure it to auto-refresh every one to five minutes. This interval balances performance cost with timeliness, providing current insights without excessive backend load.

For more advanced scenarios, you can integrate this monitoring logic with Activator. For example, if a particular tile's query duration consistently exceeds a performance threshold or if query volume spikes unexpectedly, Activator can trigger an alert or downstream automation.

## 6. Orchestration and Optimization

- **Refresh Orchestration:**
  - Avoid refresh stampedes; stagger tiles across time intervals.
  - Centralize policy control to enforce refresh resource "budgets".

- **Query Optimization:**
  - Precompute and materialize expensive joins.
  - Use `bin()`, `make-series`, `render` intelligently to support the goal of the visual/dashboard.
  - Cache intermediate queries in temporary tables if needed.

- **Activator Integration:**
  - Visualize Activator state in dashboards.
  - Enable drillthrough from tiles to Activator logs with parameterized links to enable those real-time intelligence components to collaboratively assist in data exploration.

## 7. Schemas and Throughput

- **Schema Design:**
  - Use narrow-wide schema pattern for flexible slicing.
  - Normalize values to support slicers (regions, states, event types).

- **What a Narrow-wide Schema Is and When To Use It:**

    - This is a deliberate design pattern in data modeling for real-time analytics, particularly when building dashboards in Microsoft Fabric using KQL.
    - **Narrow Schema:** Each row captures a single measurement or attribute, and multiple rows may represent the same entity at a single timestamp. Common columns include `entity_id`, `timestamp`, `metric_name`, and `value`.
    - **Wide Schema:** Each row represents one entity at one point in time, and each metric is stored as a separate column.

#### Example Comparison:

**Narrow Schema**
| entity_id | timestamp           | metric_name | value  |
|-----------|---------------------|-------------|--------|
| sensor_01 | 2024-01-01 10:00:00 | temperature | 21.5   |
| sensor_01 | 2024-01-01 10:00:00 | humidity    | 58     |

**Wide Schema**
| entity_id | timestamp           | temperature | humidity |
|-----------|---------------------|-------------|----------|
| sensor_01 | 2024-01-01 10:00:00 | 21.5        | 58       |

---

- **Why Use This Pattern in Real-Time Dashboards?**

- **Flexible Slicing:** Narrow schema supports dynamic filtering and grouping using `metric_name`, allowing visuals to slice by metric type without schema changes.
- **Extensibility:** Adding new metrics doesn’t require schema evolution. You simply ingest new `metric_name` values.
- **Tile Parameterization:** Tiles can be parameterized to show different metrics (e.g., CPU, latency, error rate) with a single KQL query.

- **Best Practice Recommendations:**

Use a **hybrid** approach:
- Store operational telemetry in **narrow schema** for dashboarding and alerting.
- Maintain a **wide materialized view** for performant multi-metric aggregation when needed, especially for pages that compare multiple metrics at once.

This pattern ensures real-time dashboards are **scalable**, **modular**, and **responsive** to schema changes.

- **Throughput Strategy:**
  - Support high ingestion rates with bounded visual complexity.
  - Evaluate concurrency against workspace capacity and KQL tier.

## 8. Monitoring and Pricing

- **Monitoring Tips:**
  - Use native dashboard diagnostics to trace query load.
  - Cross-check tile refresh impact in System Overview dashboard.

- **Cost Management:**
  - Costs driven by refresh frequency, data volume, concurrency.
  - Recommendations:
    - Avoid <10s refresh unless mission critical.
    - Pre-aggregate high-cardinality data.
    - Avoid slicers on unindexed fields.

## 9. Example Hands-On Lab: Drone Fleet Dashboard

**Objective:** Build and optimize a real-time dashboard for delivery drone telemetry.

### Tasks:
1. Ingest telemetry via Kafka connector into Eventhouse.
2. Design event and status table schema.
3. Use update policies to filter `status changed` events.
4. Build dashboard:
   - Page 1: Fleet summary, 60s refresh.
   - Page 2: Drillthrough per drone, 15s refresh.
   - Parameters: drone_id, region.
5. Use metrics tab to evaluate tile load.
6. Integrate with Activator to visualize alerts.

---

> **Tip:** Reuse parameter definitions across dashboards for consistency.
