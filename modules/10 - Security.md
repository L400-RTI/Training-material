# Module 10: Securing Microsoft Fabric Real-Time Intelligence

## 1. Introduction

This module provides a comprehensive deep dive into securing Microsoft Fabric Real-Time Intelligence components, including Eventhouse, OneLake, Eventstream, and more. It covers existing capabilities, upcoming improvements, and actionable best practices for enterprise scenarios.

It is important to note that this content only covers the security capabilities of the product as of Microsoft Build 2025. In addition, during the creation of this training material, it was repeatedly noted and discussed that much of the work to secure real-time intelligence components relies on overall Fabric platform security so it remains integrated with the rest of the platform. As Fabric security evolves and improves, the ability to secure the real-time intelligence components will evolve and improve as well.

---

## 2. Architectural Deep Dive

### Security Surface Areas

- **Data ingestion** (e.g., Eventstream, ADX ingestion)
- **Data storage** (OneLake, Eventhouse)
- **Data access** (KQL queries, Power BI integration)
- **Control plane interactions** (Fabric portal, APIs)

### Key Components

- **OneSecurity**: A unified model for table-level, row-level, and column-level security.
- **Private Endpoints**:
  - Tenant-level
  - Workspace-scoped (preferred)

### Key Components Deep Dive

Two pivotal constructs define the security capabilities: OneSecurity, which offers a unified approach to data-level security, and Private Endpoints, which govern network-level access controls. Both mechanisms are core to safeguarding data across the real-time intelligence pipeline, particularly within Eventhouse and OneLake.

#### OneSecurity: Unified Data-Level Security

OneSecurity is Microsoft's strategy to unify and simplify access control over data stored within the OneLake ecosystem and accessed through Eventhouse. It represents a progression from the fragmented models of table, row, and column security, into a single, centralized framework that supports scalable, fine-grained access management.

As of May 2025, table-level security is fully available and enforced in Fabric Real-time Intelligence. This means organizations can control access to entire tables within OneLake or Eventhouse based on user or group identities. When shortcuts are created to OneLake from Eventhouse, the system respects the underlying table-level permissions, ensuring consistency between storage and query layers. This enforcement also extends to query-accelerated data, making it viable to protect performance-sensitive data workloads without compromising security.

For architects planning Real-Time Intelligence solutions today, the practical implication is clear: use table-level security for current deployments and design schemas and queries to accommodate RLS/CLS in the near future. This may involve partitioning data across logical tables based on access domains and defining security predicates early in schema design.

#### Private Endpoints: Controlling Network Access

Complementing data-level security is the Fabric platform’s support for Private Endpoints, which enforce network-level isolation and access control. Two primary models exist today: tenant-level private endpoints and workspace-scoped private endpoints.

Tenant-level private endpoints are the only generally available option as of May 2025. These endpoints restrict Fabric service traffic to an organization’s private network boundary. While functionally adequate for small to medium environments, they present serious limitations for enterprises. A single tenant-level endpoint applies to all Fabric workspaces within that tenant. In complex organizations—such as global conglomerates with segmented business units or regulated industries with strict separation between departments—this broad scope leads to overexposure. For example, granting access to a finance workspace might unintentionally allow a manufacturing division access to the same network scope, violating principle-of-least-privilege designs and regulatory requirements.

There are still some limitations under the current implementation. For instance, queued ingestion—typically used for high-throughput scenarios—is not yet fully supported over Fabric’s private endpoints because of the absence of queue and table storage endpoints in Fabric’s abstraction model. Instead, organizations must use streaming ingestion, which is supported and performant for many Real-Time Intelligence scenarios.

---

## 3. Technical Deep Dive

### OneSecurity Model

- **Current**: Only table-level security enforced when querying OneLake via Eventhouse.
- **Limitations**:
  - Dynamic RLS not yet supported
  - RLS in mirrored tables not yet available

### Private Endpoint Model

- **Tenant-level**: Available today, not ideal for segmented enterprises

---

## 4. Implementations

### Best Practices

- Avoid tenant-level endpoints in enterprise deployments
- Use **streaming ingestion** over private endpoints (queued ingestion has limitations)
- Apply **table-level security now**; prepare for RLS/CLS
- Incorporate **predicate filtering** into OneLake security design

### Secure Implementation Pattern

1. Secure Fabric workspaces
2. Attach Eventhouse to scoped endpoints
3. Apply OneSecurity predicates
4. Query via KQL under enforced policies

---

## 5. Troubleshooting

| Issue                      | Cause                                             | Recommendation                        |
| -------------------------- | ------------------------------------------------- | ------------------------------------- |
| Ingestion fails            | Using queued ingestion with tenant-level endpoint | Use streaming or DM-based ingestion   |
| Security rules not working | Using unsupported RLS/CLS                         | Use table-level security; wait for GA |
| Unauthorized access        | Improper endpoint scope                           | Enforce workspace-scoped endpoints    |

---

## 6. Orchestration and Optimization

- Align access with **least privilege** principle using RBAC + OneSecurity
- Automate group/workspace management via PowerShell or Microsoft Graph API
- Re-architect ingestion flows to support endpoint capabilities and minimize exposure

---

## 7. Schemas and Throughput

### Secure Schema Design Principles

- Partition data by security domain (e.g., HR, Finance)
- Define column-level masks in advance
- Avoid property bag overloads; normalize with update policies

---

## 8. Monitoring and Pricing

### Monitoring

- Audit sensitive KQL queries
- Monitor ingestion flow effectiveness during endpoint transitions
- Track predicate enforcement (once released)

### Pricing

- Scoped endpoints may impact data egress/ingress costs
- Predicate filtering incurs no extra runtime charges

---

## 9. Hands-on Lab Example

### Lab Title

**Securing a Real-Time Intelligence Solution with OneSecurity and Private Endpoints**

### Objectives

- Configure table-level security in OneLake
- Set up a scoped private endpoint for a Fabric workspace
- Ingest data into Eventhouse via streaming ingestion
- Enforce OneSecurity predicates
- Validate access control for multiple user identities
