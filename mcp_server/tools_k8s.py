import json
from typing import Dict, Any, List

def check_k8s_workload_health(namespace: str = "default") -> Dict[str, Any]:
    """Inspects Kubernetes namespace for CrashLoopBackOff, OOMKilled pods, and degraded deployments."""
    # Simulated/In-cluster diagnostic adapter
    return {
        "namespace": namespace,
        "cluster_status": "Degraded",
        "pods": [
            {
                "name": "payment-api-7b89fc99b5-4x9l2",
                "status": "CrashLoopBackOff",
                "restart_count": 14,
                "exit_code": 137,
                "reason": "OOMKilled",
                "last_termination": "Container exceeded memory limit of 512Mi",
                "age": "2h41m"
            },
            {
                "name": "order-processor-5847cd67f8-m9z4p",
                "status": "Running",
                "restart_count": 0,
                "ready": "1/1",
                "age": "4d"
            }
        ],
        "events": [
            {
                "type": "Warning",
                "reason": "OOMKilling",
                "message": "Memory cgroup out of memory: Killed process 4128 (python) total-vm:845320kB"
            }
        ]
    }

def get_pod_logs_snippet(pod_name: str, namespace: str = "default", tail_lines: int = 50) -> str:
    """Fetches the latest error log lines from a Kubernetes pod container."""
    return f"""[2026-10-29 00:04:12] INFO: Connecting to Redis cluster cache...
[2026-10-29 00:04:15] INFO: Listening on port 8080 (workers=4)
[2026-10-29 00:04:22] WARN: Memory consumption threshold reached (88% of 512Mi)
[2026-10-29 00:04:29] ERROR: OutOfMemoryError in worker thread 3 allocating 128MB batch chunk
[2026-10-29 00:04:30] FATAL: Process killed by cgroup controller (SIGKILL 9 / exit code 137)"""
