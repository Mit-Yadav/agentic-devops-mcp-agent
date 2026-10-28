# SRE Runbook: Kubernetes OOMKilled (Exit Code 137)

## Problem Description
Pod terminated abruptly with Reason: OOMKilled and Exit Code 137. Occurs when memory allocation exceeds `resources.limits.memory` cgroup boundary.

## Diagnosis Steps
1. Check container events: `kubectl describe pod <pod_name>`
2. Inspect Prometheus saturation metric: `container_memory_working_set_bytes` vs `kube_pod_container_resource_limits`
3. Correlate with traffic spike or memory leak in application runtime (e.g., Python heap, JVM heap size).

## Remediation Workflow
1. Immediate Mitigation: Patch deployment memory limit (e.g. increase from 512Mi to 1Gi) or scale horizontal replicas (HPA).
2. Permanent Fix: Enable KEDA memory-based scaling or optimize application payload buffering.
