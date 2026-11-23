# Threat Model

## Method and assets

The model uses STRIDE to evaluate source, image, workload identity, Kubernetes configuration, service availability, and operational evidence.

| ID | Category | Scenario | Current control | Residual risk |
|---|---|---|---|---|
| T1 | Spoofing | Stolen GitHub identity changes workload | Review and required CI are external requirements | Administrator bypass |
| T2 | Tampering | Registry tag is replaced | Deployment requires digest pinning | Build provenance/signing not implemented |
| T3 | Repudiation | Actor denies deployment action | Git and Kubernetes audit evidence expected | Cluster audit export outside scope |
| T4 | Disclosure | Pod reads credentials or sensitive filesystem | Token automount disabled; read-only root; no secret in manifest | Node/runtime compromise |
| T5 | Denial of service | Bad rollout or disruption removes capacity | Three replicas, maxUnavailable zero, PDB, probes | Shared dependencies and regional failures |
| T6 | Elevation | Container gains host capability | Non-root, seccomp, no privilege escalation, all capabilities dropped | Kernel vulnerability |
| T7 | Lateral movement | Compromised pod reaches peer workloads | Default-deny ingress and explicit allow | Egress unrestricted in base |
| T8 | Supply chain | Vulnerable dependency or CI action executes | Pinned Python packages, Trivy, Dependabot | Base image/action provenance review remains |

## Validation experiments

- Replace the image digest with a nonexistent digest and observe safe rollout failure.
- Create `/tmp/not-ready` and confirm removal from ready endpoints.
- Attempt to write outside `/tmp` and confirm the read-only filesystem.
- Inspect effective UID, capabilities, token mount, and seccomp profile.
- Evict one pod and confirm the PDB/Deployment preserve service capacity.
- Generate load and observe HPA behaviour without exceeding the maximum.

Review after architecture, identity, dependency, exposure, data-classification, or cluster-policy changes, and after any security incident.
