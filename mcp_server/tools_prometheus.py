from typing import Dict, Any

def query_golden_signals(service: str, lookback_minutes: int = 15) -> Dict[str, Any]:
    """Queries Prometheus for the 4 Golden Signals (Latency, Traffic, Errors, Saturation)."""
    return {
        "service": service,
        "window": f"{lookback_minutes}m",
        "metrics": {
            "error_rate_percent": 18.4,
            "p95_latency_ms": 1420.0,
            "p99_latency_ms": 3890.0,
            "throughput_rps": 620.5,
            "cpu_saturation_percent": 42.1,
            "memory_saturation_percent": 99.2,
            "sli_slo_status": {
                "target_slo": "99.9%",
                "current_sli": "97.4%",
                "error_budget_burn_rate": "14.2x (CRITICAL - Fast Burn)"
            }
        }
    }
