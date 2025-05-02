## Module 12 - Networking

### Introduction

### Architectural deep dive

### Technical deep dive

Eventstream - meeting Xu Jiang April 14

![Eventstream 2](./assets/images/Eventstream2.png)

PL = Private Link.

When a workspace is closed to public accesss the Eventstream will use the ASA job to pull data from the Azure Event Hub from the vNET using the network protector library.

MS for now is calling this a "private link bypass" using contracts in the request to enable the trusted handshake between the "outside" ASA and the internal Eventhub in the Eventstream in the workspace not open to the public (in a vNET).

For destionation inside a vNET in Fabric, the Eventstream is also using the "private link bypass" for Lakehouse, Eventhouse in (push to EH). But here is a problem for EH pulling data from the Eventstream.

![Private vNET injection](./assets/images/Private%20vNET%20injection.png)

This image was a part of the networking discussion. Around the work on getting data from on-prem data sets.

### Implementations

### Troubleshooting

### Orchestration and optimization

### Schemas and throughput

### Monitoring and pricing

### Hands-on lab

---
