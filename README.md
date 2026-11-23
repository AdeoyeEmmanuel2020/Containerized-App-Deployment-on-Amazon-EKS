# Resilient Container Platform Reference on Amazon EKS

This repository is an evidence-driven reference implementation for deploying a small HTTP workload to Amazon EKS. It demonstrates how senior platform engineering connects application behaviour, container hardening, Kubernetes workload policy, availability objectives, security controls, and automated verification.

> **Scope:** The repository supplies a hardened workload and deployment baseline, not an EKS cluster. It does not claim production certification, guaranteed availability, or compliance. A production platform also requires account-level infrastructure, identity federation, secrets management, observability backends, recovery exercises, and organisational controls.

## Research question

**How can a Kubernetes workload be designed so that its reliability and security claims are explicit, testable, and traceable from architecture decision to runtime evidence?**

The working hypothesis is that declarative workload controls, immutable container practices, health semantics, constrained privileges, and fail-closed CI make operational risk more observable and repeatable than ad-hoc deployment. The hypothesis is falsified if the image runs as root, manifests permit privilege escalation, probes do not represent application health, disruption removes all replicas, insecure changes bypass CI, or a clean checkout cannot reproduce validation.

## Architecture

```mermaid
flowchart LR
    classDef actor fill:#F8FAFC,stroke:#334155,stroke-width:1.5px,color:#0F172A
    classDef delivery fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#1E3A8A
    classDef aws fill:#FFF7ED,stroke:#EA580C,stroke-width:1.5px,color:#7C2D12
    classDef k8s fill:#EEF2FF,stroke:#4F46E5,stroke-width:1.5px,color:#312E81
    classDef workload fill:#ECFDF5,stroke:#059669,stroke-width:1.5px,color:#064E3B
    classDef control fill:#FDF4FF,stroke:#A21CAF,stroke-width:1.5px,color:#701A75
    classDef observe fill:#F0FDFA,stroke:#0F766E,stroke-width:1.5px,color:#134E4A

    DEV[Engineer]:::actor
    USER[Client]:::actor

    subgraph DELIVERY[Secure software delivery]
        direction TB
        GH[GitHub pull request]:::delivery
        CI[Tests + Docker build<br/>Trivy policy gates]:::delivery
        ECR[Amazon ECR<br/>immutable image digest]:::aws
        GH --> CI --> ECR
    end

    subgraph AWS[AWS account]
        direction LR
        EDGE[Ingress / AWS Load Balancer<br/>TLS and routing - environment overlay]:::aws

        subgraph EKS[Amazon EKS cluster]
            direction LR
            SVC[ClusterIP Service<br/>ready-endpoint routing]:::k8s

            subgraph WORKLOAD[eks-reference namespace]
                direction TB
                P1[Pod · zone A]:::workload
                P2[Pod · zone B]:::workload
                P3[Pod · zone C]:::workload
            end

            HPA[Horizontal Pod Autoscaler<br/>3-10 replicas]:::control
            PDB[PodDisruptionBudget<br/>minimum 2 available]:::control
            NP[NetworkPolicy<br/>default-deny ingress]:::control
            OBS[Metrics · logs · events]:::observe

            EDGE --> SVC
            SVC --> P1 & P2 & P3
            HPA -. scales .-> WORKLOAD
            PDB -. protects .-> WORKLOAD
            NP -. constrains .-> WORKLOAD
            WORKLOAD --> OBS
        end
    end

    DEV --> GH
    ECR -. image pull by digest .-> WORKLOAD
    USER --> EDGE
```

The Kubernetes layer uses three replicas, rolling updates, topology spread, readiness/liveness/startup probes, requests and limits, a PodDisruptionBudget, autoscaling, a dedicated service account, default-deny ingress, explicit application ingress, and a restricted pod security context.

Detailed trust boundaries and decisions are in [Architecture](docs/architecture.md). Adversary assumptions are in the [Threat model](docs/threat-model.md), and claims-to-evidence traceability is in the [Assurance matrix](docs/assurance-matrix.md).

## Repository structure

```text
.
├── .github/
│   ├── dependabot.yml
│   └── workflows/assurance.yml
├── docs/
│   ├── architecture.md
│   ├── assurance-matrix.md
│   └── threat-model.md
├── k8s/base/
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── network-policy.yaml
│   ├── pdb.yaml
│   ├── service-account.yaml
│   └── service.yaml
├── src/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── tests/test_app.py
└── LICENSE
```

## Control summary

| Quality attribute | Mechanism | Evidence |
|---|---|---|
| Availability | Three replicas, rolling update, topology spread, PDB | Rendered manifests and disruption test |
| Elasticity | CPU-based HPA with bounded replica count | HPA status and load experiment |
| Safe traffic routing | Startup, readiness, and liveness probes | Probe events and negative readiness test |
| Resource governance | CPU/memory requests and limits | Pod specification and runtime metrics |
| Least privilege | Non-root image and pod, dropped capabilities, read-only filesystem, no token mount | Image/config scan and pod security context |
| Network isolation | Default-deny ingress plus explicit same-namespace access | Network-policy test |
| Supply-chain assurance | Pinned dependencies, image build, Trivy scans, manifest rendering | GitHub Actions run |
| Graceful change | Rolling update and termination grace period | Controlled rollout experiment |

## Local validation

Requirements: Python 3.12, Docker, and `kubectl` with Kustomize support.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt pytest
pytest -q

docker build -t eks-reference:local src
docker run --rm -p 8080:8080 eks-reference:local
curl --fail http://localhost:8080/health/live

kubectl kustomize k8s/base > /tmp/eks-reference.yaml
```

## Deployment

Build and push an immutable image to an authorised ECR repository, then replace the placeholder image digest in `k8s/base/deployment.yaml`. Digest pinning is preferred over mutable tags.

```bash
kubectl apply -k k8s/base
kubectl -n eks-reference rollout status deployment/eks-reference
kubectl -n eks-reference get deploy,pods,svc,hpa,pdb,networkpolicy
```

This baseline creates a `ClusterIP` service. External exposure requires an ingress or `LoadBalancer` design selected for the target cluster. That choice is intentionally not hidden behind an unverified annotation.

## Operational verification

```bash
kubectl -n eks-reference get pods -o wide
kubectl -n eks-reference describe deployment eks-reference
kubectl -n eks-reference get hpa eks-reference --watch
kubectl -n eks-reference logs deployment/eks-reference
kubectl -n eks-reference port-forward service/eks-reference 8080:80
```

Evidence should include a rollout, voluntary disruption, failed-readiness experiment, HPA load experiment, and restoration to declared state. Screenshots are supporting material; command output, metrics, events, and versioned configuration are stronger evidence.

## CI assurance

Pull requests and changes to `main` run Python tests, a Docker build, Trivy filesystem/image/configuration scans, Kustomize rendering, and policy checks. Branch rules should require the workflow and independent review. CI does not deploy because identity, approvals, environment protections, and rollback policy are account-specific.

## Explicit limitations and roadmap

- EKS cluster, VPC, ECR, IAM roles for service accounts, ingress controller, DNS, and certificates are outside this repository.
- The demo is stateless; data durability and transactional recovery are not evaluated.
- HPA requires a functioning metrics pipeline.
- NetworkPolicy requires an enforcing CNI implementation.
- Egress restrictions are environment-specific and not defined here.
- No service mesh, admission controller, policy engine, runtime detection, distributed tracing, or chaos platform is included.
- Multi-Region recovery and cluster upgrade procedures require separate infrastructure and exercises.

These boundaries prevent the documentation from presenting a workload example as a complete production platform.

## Cost and cleanup

Apply only to an authorised cluster. EKS, worker capacity, load balancers, NAT gateways, logging, and image storage can incur charges.

```bash
kubectl delete -k k8s/base
```

## Author

**Adeoye Emmanuel**<br>
Cloud Solutions Architect | Cloud Security Architect | DevSecOps Engineer<br>
[LinkedIn](https://linkedin.com/in/adeoyeemmanuel2020) | [GitHub](https://github.com/AdeoyeEmmanuel2020)

## Licence

MIT. See [LICENSE](LICENSE).
