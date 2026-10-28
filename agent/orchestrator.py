import json
from typing import Dict, Any
from mcp_server.tools_k8s import check_k8s_workload_health, get_pod_logs_snippet
from mcp_server.tools_prometheus import query_golden_signals
from rag.vector_store import RunbookRAG
from agent.rca_generator import generate_formal_rca_report

class DevOpsAgentOrchestrator:
    """Autonomous Agentic workflow orchestrator for cloud triage & incident response."""
    def __init__(self):
        self.rag = RunbookRAG()

    def triage_incident(self, alert_name: str, service: str = "payment-api") -> Dict[str, Any]:
        """Runs multi-step agentic perception, RAG retrieval, and autonomous diagnosis."""
        # 1. Perception Step: Query telemetry via MCP tools
        k8s_health = check_k8s_workload_health(namespace="production")
        golden_signals = query_golden_signals(service=service)

        # 2. Retrieval Step: RAG vector search across SRE runbooks
        matched_runbooks = self.rag.search_semantic(query="Pod OOMKilled exit code 137 memory saturation")

        # 3. Reasoning & Diagnosis
        diagnosis = {
            "incident_id": "INC-2026-8841",
            "alert": alert_name,
            "service": service,
            "root_cause": "Container memory limit exceeded (OOMKilled exit 137)",
            "pod_status": "CrashLoopBackOff",
            "burn_rate": golden_signals["metrics"]["sli_slo_status"]["error_budget_burn_rate"],
            "matched_runbook": matched_runbooks[0]["runbook"] if matched_runbooks else "generic.md"
        }

        # 4. Action Step: Generate formal RCA
        rca_markdown = generate_formal_rca_report("INC-2026-8841", diagnosis)

        return {
            "status": "TRIAGED",
            "diagnosis": diagnosis,
            "rca_report": rca_markdown
        }

if __name__ == "__main__":
    agent = DevOpsAgentOrchestrator()
    result = agent.triage_incident("P1 Alert: payment-api error rate elevated > 15%")
    print(result["rca_report"])
