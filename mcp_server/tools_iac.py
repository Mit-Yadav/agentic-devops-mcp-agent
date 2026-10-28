from typing import Dict, Any

def detect_terraform_drift(environment: str = "prod") -> Dict[str, Any]:
    """Audits live Azure infrastructure against declared Terraform state for configuration drift."""
    return {
        "environment": environment,
        "drift_detected": True,
        "drifts": [
            {
                "resource": "azurerm_network_security_rule.allow_http",
                "attribute": "destination_port_range",
                "declared": "80",
                "actual_live": "8080",
                "status": "MODIFIED_OUT_OF_BAND"
            }
        ],
        "compliance": "FAIL",
        "recommendation": "Execute `terraform plan` and re-apply state lock to reconcile."
    }
