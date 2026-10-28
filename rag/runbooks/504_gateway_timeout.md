# SRE Runbook: 504 Gateway Timeout in Ingress Controller

## Problem Description
Ingress-NGINX or Azure Application Gateway returns HTTP 504. Upstream service failed to respond within `proxy-read-timeout` window.

## Diagnosis Steps
1. Query downstream service P99 latency in Prometheus/Grafana.
2. Check database connection pool saturation or deadlocks in PostgreSQL / Redis.
3. Check pod readiness probes failing under load.

## Remediation Workflow
1. Scale upstream replicas to distribute connection backlog.
2. Increase ingress `proxy-read-timeout` temporarily if batch query is executing.
3. Inspect and scale database connection pooling (PgBouncer / Redis pool).
