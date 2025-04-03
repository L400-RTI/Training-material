---
published: false # Optional. Set to true to publish the workshop (default: false)
type: workshop # Required.
title: Project Peritus - Real-Time Intelligence expoert training # Required. Full title of the workshop
short_title: Real-Time Intelligence expoert training # Optional. Short title displayed in the header
description: In this deep technical workshop, you will build a complete analytics platform with streaming data using Microsoft Fabric Real-Time Intelligence components and other features of Microsoft Fabric. This is a proctor led worksop in which each section is accompanied by a technical overview of Fabric RTI components. # Required.
level: advanced # Required. Can be 'beginner', 'intermediate' or 'advanced'
authors: # Required. You can add as many authors as needed
  - Frank Geisler
  - Matt Gordon
  - Brian Bønk
contacts: # Required. Must match the number of authors
  - https://aka.ms/fabricblog
duration_minutes: 1000 # Required. Estimated duration in minutes
audience: students, pro devs, analysts # Optional. Audience of the workshop (students, pro devs, etc.)
tags: fabric, kql, realtime, intelligence, event, stream, sql, data, analytics, kusto, medallion, dashboard, reflex, activator # Required. Tags for filtering and searching
---

# Introduction

*intro goes here*

## Modalities

- Total workshop duration is 2-3 days.
- Each section is accompanied with technical explanation of the Fabric Real-Time Intelligence component being used in the tutorial.
- Without the accompanied explanation, the tutorial can be completed in 1-2 days.

## Authors

- [Brian Bønk ](https://www.linkedin.com/in/brianbonk/), Data Platform MVP
- [Frank Geisler](https://www.linkedin.com/in/frank-geisler/), Data Platform MVP
- [Matt Gordon](https://www.linkedin.com/in/sqlatspeed/), Data Platform MVP

## Contributing

- If you'd like to contribute to this lab, report a bug or issue, please feel free to submit a Pull-Request to the [GitHub repo](<link to repo>) for us to review or [submit Issues](<link to repo>) you encounter.

## Prerequisites

To get starated with this training and to understand the baseline of the Real-Time Intelligence suite of services from Microsoft Fabric, it is expected of the audience to have the following certifications:

- [DP-600 Microsoft Certified: Fabric Analytics Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/fabric-analytics-engineer-associate/?practice-assessment-type=certification)
- [DP-700 Microsoft Certified: Fabric Data Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/?practice-assessment-type=certification)
- [Microsoft Applied Skills: Implement a Real-Time Intelligence solution with Microsoft Fabric](https://learn.microsoft.com/en-us/credentials/applied-skills/implement-a-real-time-intelligence-solution-with-microsoft-fabric/)

This training will not help you understand the basics of the suite, and it will start of from the above mentioned knowledge level.

## Overview of the content

The content is built from 3 sections, spanning ingestion of data, manipulation of data when needed using the KQL language and visualize & analyze data using KQL, Real-Time Dashboards and Power BI.

| Section 1 | Section 2 | Section 3|
|-------|-------|------|
| Ingestion of data using Eventstream. Complex structures and advanced data manipulation using Eventstream and the different built-in transformations. Including the use of schemas, reference data, multiple and different sources and how to effectively implement advanced data manipulation. This also includes the use of Rules, Activator and event-driven actions. | Storage in Eventhouse and how to query the data at speed. Advanced KQL query statements, incl., but not limited to, data load patterns using functions, views and updatepolicies, geo-spacial calculations, graph data structures and time series manipulation. Effective KQL query sets with performance tuning and understanding of the underlying metrics to write better queries. Security and governance of the KQL database. | Analyze and visualize data in both queries and using Real-Time Dashboard + Power BI. Using the built-in visualizations for in-query analysis. Building custom visuals using Plotly library and working with Power BI to help model and query data when needed. |

## Section 1 - ingestion and actions

After this section you will know how work with the Eventstream processor and how to use the built-in data manipulations.

You will also know to use multiple sources in the Eventstream and how to leverage the use of schemas, reference data for optimal data loading from source to Eventhouse.

Lastly you will understand the whereabouts of the built-in sources from Microsoft Fabric, how to use and implement the Rules, Activator and event-driven actions and know your way around cost of the service.

### Fabric Events and Business Events

### Activator and Event driven actions

### Custom connectors

### Troubleshooting

### Orchestration and optimization

### Schemas and throughput

### Monitoring

## Section 2 - KQL engine and queries

In this section you will learn the advanced techniques of working with the KQL language in the Eventhouse and KQL database.

You will learn the whereabouts of storage, how it is maintained by the engine, how the streaming of data to tables works and how to leverage the power of the KQL language to perform data manipulation at query time.

This section also covers the advanced techniques of Geo-spacial analytics, analytics on graph data and how to use the built-in data movement processes from functions, views and update policies.

Lastly you will learn the approach of securing and governing your KQL database.

### Storage and the KQL engine

### Streaming tables

### Advanced data manipulation

### Geo-spacial techniques

### Graph data

### Joins, hints and lookups

### Views, functions and policies

### Security and governance

## Section 3 - visualization and apps

In this section you will learn the built-in features of visualizing data at query time and how to implement custom visuals using the Plotly library.

You will learn the usage and implementation of the Real-Time Dashboard, including, but not limited to, the advanved techniques of dashboards (filters, parameters, data source etc.) and a subsection on how to implement Power BI in the solution of using KQL data for analytics.

### Built-in visualization

### Custom visualization using Plotly

### Real-Time Dashboards

### Power BI

### Org Apps

---

# Standard elements (delete before final deployment)

## Note section

<div class="info" data-title="Note">

> **The title can be resized on the dashboard canvas directly, rather than writing code.**

</div>

## Images

![Image alt text](<path to image>)

## code sections

```
This is a code section
// this is a KQL comment within a code section
```

##

`this is a highlight`
