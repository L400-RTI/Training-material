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

The Microsoft Fabric Real-Time Intelligence (RTI) platform represents a pivotal shift in how enterprises handle
streaming data, automation, and action-oriented analytics. As adoption grows, so too does the need for real-world
expertise that goes beyond the surface-level feature set.

## Why This Course Was Created

Across the Microsoft data ecosystem, we are seeing a recurring pattern: Partners and customers are building
real-time solutions using Fabric—but too often with architectural blind spots, implementation mistakes, or
fundamental misunderstandings of how services like Activator, Eventstream, and Reflex are meant to interoperate at scale.

For example:

- Partners report difficulty staffing RTI engagements due to a lack of L400–500-skilled professionals.
- Suboptimal implementations are leading to production disruptions,
- Customers are building real-time automation flows without fully understanding how detection
  rules interact with stream federation, delays, and failure states.
- Fundamental concepts such as pattern detection, state change management, and
  throughput handling are either misapplied or ignored.

These are not theoretical issues—they are impacting live deployments and increasing the burden on
support and engineering teams. We must address this gap in expertise now to avoid scale-limiting friction
across the RTI customer base.

## What This Course Provides

This course was built to:

- Equip senior engineers, architects, and partners with advanced technical insight into Fabric RTI’s architecture,
  performance characteristics, and behavioral nuances.
- Demystify complex real-time patterns, including dynamic schema handling,
  alert suppression strategies, federated stream orchestration, and event-driven pipeline execution.
- Enable best-practice implementations by showcasing what should happen in production—and what often
  goes wrong when you miss key details.
- Accelerate onboarding of RTI experts to ensure Microsoft’s ecosystem can meet the growing customer
  demand for high-fidelity real-time solutions.

The content is driven directly by interviews with Microsoft’s product engineering leaders, distilled into
actionable knowledge and guided labs.

## Modalities

- Total workshop duration is 2-3 days.
- Each module is accompanied with technical explanation of the Fabric Real-Time
  Intelligence component being used in the tutorial.
- Without the accompanied explanation, the tutorial can be completed in 1-2 days.

## Authors

- [Brian Bønk](https://www.linkedin.com/in/brianbonk/), Data Platform MVP
- [Frank Geisler](https://www.linkedin.com/in/frank-geisler/), Data Platform MVP
- [Matt Gordon](https://www.linkedin.com/in/sqlatspeed/), Data Platform MVP

## Contributing

- If you'd like to contribute to this lab, report a bug or issue, please feel free to submit a Pull-Request
  to the ==[GitHub repo](<link to repo>)== for us to review or ==[submit Issues](<link to repo>)== you encounter.

## Prerequisites

To get starated with this training and to understand the baseline of the Real-Time Intelligence suite of
services from Microsoft Fabric, it is expected of the audience to have the following certifications:

- [DP-600 Microsoft Certified: Fabric Analytics Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/fabric-analytics-engineer-associate/?practice-assessment-type=certification)
- [DP-700 Microsoft Certified: Fabric Data Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/?practice-assessment-type=certification)
- [Microsoft Applied Skills: Implement a Real-Time Intelligence solution with Microsoft Fabric](https://learn.microsoft.com/en-us/credentials/applied-skills/implement-a-real-time-intelligence-solution-with-microsoft-fabric/)

This training will not help you understand the basics of the suite, and it will start of from the above mentioned knowledge level.

## Overview of the content

The content is built from 13 modules + 1 appendix, spanning ingestion of data, manipulation of data when
needed using the KQL language, visualize and analyze data using KQL, Real-Time Dashboards and Power BI, CI/CD and
architectural approaches, Security and Networking.

1. [Introduction to RTI](./01%20-%20Introduction.md) (Frank)
2. [Real-Time Hub](./02%20-%20Real-Time%20Hub.md) (Matt)
3. [Connectors](./03%20-%20Connectors.md) (Brian)
4. [Ingestion](./04%20-%20Ingestion.md) (Brian)
5. [Data modelling](./05%20-%20Data%20modelling.md) (Frank)
6. [Analytics](./06%20-%20Analytics.md) (Brian)
7. [AI + Copilot](./07%20-%20AI%20+%20Copliot.md) (Matt)
8. [Dashboards](./08%20-%20Dashboards.md) (Matt)
9. [Rules (Activator)](#module-9---rules-activator) (Frank)
10. [Actions](./10%20-%20Actions.md) (Frank)
11. [Security](./11%20-%20Security.md) (Matt)
12. [Networking](./12%20-%20Networking.md) (Brian)
13. [CI/CD and ALM](./13%20-%20CICD%20and%20ALM.md) (Frank)
14. [Appendix](./14%20-%20Appendix.md) (all)

![Real-Time Intelligence in Microsoft Fabric](/assets/images/Real-Time%20Intelligence%20in%20Microsoft%20Fabric.png)

Each module has the same overall structure:

| Structure                         | Content                                                                                                                                                                                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Introduction to the module     | Gives the fly-in to the module, the content and the business value of the module and area of RTI.                                                                                                                                                                  |
| 2. Architectural deep dive        | Introduces the module and the connection to the rest of the RTI suite in Microsoft Fabric. Also contains elements on how the architecture could work in conjunction with other parts of the RTI service.                                                           |
| 3. Technical deep dive            | Dive into the whereabouts of the service. Seen from the backend, with a deep technical walktthrough of how things are working behind the scenes and what makes the specific part of the service connect with the rest.                                             |
| 4. Implementations                | How should the specific part of the service be implemented and what to look out for when working with it. Also a deep walktrough of the details in functionality and outcome of the service.                                                                       |
| 5. Troubleshooting                | How to read error messages and error codes. How to debug issues. How to best help Microsoft support in case of need.                                                                                                                                               |
| 6. Orchestration and optimization | How does the service best fit with an entire architecture around orchestration, how to execute the processes. How to optimize the loads, speeds and querytimes.                                                                                                    |
| 7. Schemas and throughout         | How to handle schemas in the service and what to know when working with structured, semi-structured and unstructured data. A walkthrough of the limitations, configuration options and whereabouts of throughput                                                   |
| 8. Monitoring and pricing         | How to monitor the service and find the bottlenecks and other needed information of the performance. A deep learning element on how to calculate and estimate cost of a service and an entire implementation. How to monitor cost and optimize for cost reduction. |
| 9. Hands-on lab                   | A hands on lab with guides, to try out the specific service and to learn some of the L400 features.                                                                                                                                                                |

<div class="info" data-title="Note">

> **In some modules, you will not find all of the sections above. This is by intent, and shows that this specific section does not apply to this module, or the module does not contain any information about the section.**

</div>
