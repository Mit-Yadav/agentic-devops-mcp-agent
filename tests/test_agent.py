import pytest
from agent.orchestrator import DevOpsAgentOrchestrator

def test_agent_triage_loop():
    agent = DevOpsAgentOrchestrator()
    result = agent.triage_incident("P1: payment-api outage", service="payment-api")
    assert result["status"] == "TRIAGED"
    assert "OOMKilled" in result["diagnosis"]["root_cause"]
    assert "INCIDENT ROOT CAUSE ANALYSIS" in result["rca_report"]
