# Architecture and Decision Record

## System boundary

The repository owns the application image and Kubernetes workload objects. It assumes, but does not provision, an EKS cluster, nodes, ECR, ingress, DNS, certificates, metrics pipeline, logging backend, and AWS identity controls.

## Quality-attribute priorities

1. Safe rollout and disruption tolerance
2. Least privilege and workload isolation
3. Reproducibility and traceable evidence
4. Bounded resource consumption and elasticity
5. Operability through explicit health contracts

## Trust boundaries

| Boundary | Risk | Treatment |
|---|---|---|
| Developer to GitHub | Malicious or accidental change | Review, required CI, versioned source |
| GitHub to image registry | Image substitution or credential theft | OIDC and digest pinning are required in target environment |
| Registry to cluster | Untrusted image execution | Scanner gate, digest, admission policy recommended |
| Service to pod | Unready endpoint receives traffic | Readiness probe and selector contract |
| Pod to kernel/node | Container escape or privilege abuse | Non-root, seccomp, dropped capabilities, read-only root |

## Decisions

### ADR-001: Managed Kubernetes is an external platform dependency

EKS reduces control-plane operations, but does not operate workloads, nodes, add-ons, policies, or recovery automatically. This repository therefore avoids claiming that managed control plane equals production readiness.

### ADR-002: Availability is expressed as constraints, not a percentage

Three replicas, topology spread, rolling update, probes, and a PDB improve availability. They do not prove 99.9% uptime. An SLO requires measured request availability, an observation window, error-budget policy, and dependency analysis.

### ADR-003: The workload is non-root and immutable by default

The container and pod use UID/GID 10001, RuntimeDefault seccomp, dropped Linux capabilities, disabled privilege escalation, read-only root filesystem, and a bounded temporary volume.

### ADR-004: External exposure is left to an environment overlay

Ingress class, TLS, WAF, DNS, and load-balancer annotations depend on the target cluster. The base exposes only a ClusterIP service so it remains honest and portable.

### ADR-005: Scaling is bounded

The HPA ranges from three to ten replicas and uses CPU utilisation. Production should evaluate request rate, latency, queue depth, startup time, and node capacity before selecting a scaling signal.

## Failure modes

| Failure | Expected behaviour | Evidence |
|---|---|---|
| One pod terminates | Service continues through remaining ready pods | Events, endpoints, request success |
| Pod is not ready | Endpoint is removed from Service routing | EndpointSlice and probe events |
| Node unavailable | Replacement schedules subject to capacity/topology | Deployment and scheduler events |
| CPU demand rises | HPA increases desired replicas if metrics/capacity exist | HPA status and metrics |
| Bad image digest | Rollout fails without replacing all healthy replicas | Rollout status and ReplicaSet state |
| Voluntary disruption | PDB retains at least two available pods | Eviction result and PDB status |

## Production extensions

Use IaC for EKS/VPC/ECR, IRSA or EKS Pod Identity, admission policy, signed images and provenance, managed add-ons, workload metrics, central logs/traces, GitOps, backup/recovery procedures, cluster-autoscaling design, and periodic resilience experiments.
