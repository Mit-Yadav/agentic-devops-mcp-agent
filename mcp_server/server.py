from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from mcp_server.tools_k8s import check_k8s_workload_health, get_pod_logs_snippet
from mcp_server.tools_prometheus import query_golden_signals
from mcp_server.tools_iac import detect_terraform_drift

app = FastAPI(
    title="DevOps & SRE Model Context Protocol (MCP) Server",
    description="Exposes structured tools and context for Autonomous AI SRE Agents and LLMs",
    version="1.0.0"
)

# Standard MCP tool schema definitions
TOOLS_CATALOG = [
    {
        "name": "check_k8s_workload_health",
        "description": "Checks Kubernetes cluster/namespace for degraded pods, OOMKills, and CrashLoopBackOff",
        "parameters": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "default": "default"}
            }
        }
    },
    {
        "name": "get_pod_logs_snippet",
        "description": "Retrieves recent termination and crash logs from container stdout/stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "pod_name": {"type": "string"},
                "namespace": {"type": "string", "default": "default"},
                "tail_lines": {"type": "integer", "default": 50}
            },
            "required": ["pod_name"]
        }
    },
    {
        "name": "query_golden_signals",
        "description": "Queries Prometheus for Latency, Traffic, Errors, Saturation and Error Budget burn",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "lookback_minutes": {"type": "integer", "default": 15}
            },
            "required": ["service"]
        }
    },
    {
        "name": "detect_terraform_drift",
        "description": "Compares declared IaC Terraform state against live Azure cloud resources",
        "parameters": {
            "type": "object",
            "properties": {
                "environment": {"type": "string", "default": "prod"}
            }
        }
    }
]

@app.get("/mcp/tools")
def list_tools() -> Dict[str, Any]:
    """Returns MCP tools catalog compliant with Model Context Protocol."""
    return {"tools": TOOLS_CATALOG}

class ToolInvocation(BaseModel):
    tool: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

@app.post("/mcp/call")
def call_tool(req: ToolInvocation) -> Dict[str, Any]:
    """Executes a tool call requested by an LLM or Agentic Orchestrator."""
    if req.tool == "check_k8s_workload_health":
        return check_k8s_workload_health(req.arguments.get("namespace", "default"))
    elif req.tool == "get_pod_logs_snippet":
        return {"logs": get_pod_logs_snippet(req.arguments.get("pod_name", "unknown"))}
    elif req.tool == "query_golden_signals":
        return query_golden_signals(req.arguments.get("service", "unknown"))
    elif req.tool == "detect_terraform_drift":
        return detect_terraform_drift(req.arguments.get("environment", "prod"))
    else:
        raise HTTPException(status_code=404, detail=f"Tool '{req.tool}' not found in MCP catalog")

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}
