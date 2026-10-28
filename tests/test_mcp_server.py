import pytest
from mcp_server.tools_k8s import check_k8s_workload_health, get_pod_logs_snippet
from mcp_server.tools_prometheus import query_golden_signals
from mcp_server.tools_iac import detect_terraform_drift

def test_k8s_health_check():
    health = check_k8s_workload_health("production")
    assert health["cluster_status"] == "Degraded"
    assert len(health["pods"]) > 0
    assert health["pods"][0]["reason"] == "OOMKilled"

def test_prometheus_signals():
    signals = query_golden_signals("payment-api")
    assert signals["service"] == "payment-api"
    assert signals["metrics"]["error_rate_percent"] > 0
    assert "error_budget_burn_rate" in signals["metrics"]["sli_slo_status"]

def test_terraform_drift_detection():
    drift = detect_terraform_drift("prod")
    assert drift["drift_detected"] is True
    assert drift["compliance"] == "FAIL"
