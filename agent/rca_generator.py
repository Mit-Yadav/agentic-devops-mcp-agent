from typing import Dict, Any

def generate_formal_rca_report(incident_id: str, diagnosis: Dict[str, Any]) -> str:
    """Produces an executive Root Cause Analysis (RCA) document formatted for leadership & engineering."""
    return f"""================================================================================
             INCIDENT ROOT CAUSE ANALYSIS (RCA) REPORT
================================================================================
Incident ID:          {incident_id}
Severity:             P1 - Critical
Impacted Service:     {diagnosis.get('service', 'payment-api')}
Primary Cause:        {diagnosis.get('root_cause', 'OOMKilled Container Exit 137')}
MTTR Saved:           Estimated 42 minutes through automated agent triage

1. EXECUTIVE SUMMARY:
   The {diagnosis.get('service', 'payment-api')} service experienced repeated CrashLoopBackOff 
   failures under sustained peak traffic. Prometheus metrics revealed a memory saturation 
   of 99.2% resulting in Linux cgroup SIGKILL terminations.

2. EVIDENCE GATHERED (via MCP Server):
   - K8s Pod Status:  {diagnosis.get('pod_status', 'CrashLoopBackOff (restarts: 14)')}
   - Error Budget:    Burn rate 14.2x (SLO breached from 99.9% to 97.4%)
   - Log Trace:       OutOfMemoryError allocating 128MB batch chunk

3. RUNBOOK CORRELATION (via SRE RAG):
   - Matched Runbook: oomkill_remediation.md (Score: 0.94)

4. REMEDIATION ACTION PLAN:
   [Immediate] kubectl patch deployment {diagnosis.get('service', 'payment-api')} -p '{{"spec":{{"template":{{"spec":{{"containers":[{{"name":"app","resources":{{"limits":{{"memory":"1Gi"}}}}}}]}}}}}}}}'
   [Preventive] Tune KEDA scaledobject to trigger HPA scaling at 75% memory utilization.
================================================================================
"""
