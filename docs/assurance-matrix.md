# Assurance Matrix

| Claim | Implementation | Verification | Limitation |
|---|---|---|---|
| Workload does not require root | Image and pod UID/GID 10001 | `kubectl exec ... -- id` | Runtime/kernel still trusted |
| Privilege escalation is constrained | seccomp, drop ALL, no escalation | Manifest scan and runtime inspection | Admission enforcement external |
| Unready pods do not receive traffic | Readiness endpoint and probe | Toggle `/tmp/not-ready`; inspect EndpointSlice | Probe covers only local readiness |
| Rolling update preserves replicas | maxUnavailable 0, maxSurge 1 | Controlled rollout | Requires spare cluster capacity |
| Voluntary disruption retains service | PDB minAvailable 2 | Eviction experiment | PDB does not prevent involuntary loss |
| Resource use is bounded | Requests and limits | Metrics and throttling observation | Values require workload testing |
| Scaling is bounded | HPA min 3/max 10 | Load experiment | Metrics pipeline required |
| Ingress is restricted | Default deny plus explicit namespace rule | Network-policy test | Enforcing CNI required; egress open |
| Source changes receive automated review | Tests, build, Trivy, render checks | GitHub Actions evidence | Branch protection configured externally |

Framework mappings, if added, are traceability aids and not certification claims.
