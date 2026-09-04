from typing import Any


def detect_anomalies(metrics: dict[str, float]) -> list[str]:
    """
    Basic rule-based anomaly detection for the POC.
    In production, this can be replaced with ML/statistical
    anomaly detection from enterprise monitoring platforms.
    """

    anomalies = []

    if metrics.get("cpu_percent", 0) >= 85:
        anomalies.append(
            f"High CPU utilization: {metrics['cpu_percent']}%"
        )

    if metrics.get("memory_percent", 0) >= 85:
        anomalies.append(
            f"High memory utilization: {metrics['memory_percent']}%"
        )

    if metrics.get("error_rate_percent", 0) >= 10:
        anomalies.append(
            f"High error rate: {metrics['error_rate_percent']}%"
        )

    if metrics.get("latency_seconds", 0) >= 5:
        anomalies.append(
            f"High application latency: "
            f"{metrics['latency_seconds']} seconds"
        )

    return anomalies


def correlate_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Basic event correlation.

    Events belonging to the same service are considered
    related for this POC.
    """

    grouped: dict[str, list[dict[str, Any]]] = {}

    for event in events:
        service = event.get("service", "unknown")

        grouped.setdefault(service, []).append(event)

    correlated_events = []

    for service, service_events in grouped.items():

        if len(service_events) > 1:
            correlated_events.append(
                {
                    "service": service,
                    "event_count": len(service_events),
                    "events": service_events,
                    "correlation": "RELATED_EVENTS",
                }
            )

    return correlated_events


def detect_noise(events: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Basic duplicate/noise detection.

    Events with the same service + message are treated
    as duplicates for the POC.
    """

    seen = set()
    unique_events = []
    duplicate_count = 0

    for event in events:

        key = (
            event.get("service"),
            event.get("message"),
        )

        if key in seen:
            duplicate_count += 1
        else:
            seen.add(key)
            unique_events.append(event)

    return {
        "total_events": len(events),
        "unique_events": len(unique_events),
        "duplicate_events": duplicate_count,
        "noise_reduction_percent": (
            round(
                duplicate_count / len(events) * 100,
                2
            )
            if events
            else 0
        ),
    }


def calculate_priority(
    anomalies: list[str],
    correlated_events: list[dict[str, Any]],
) -> str:

    if len(anomalies) >= 3 or len(correlated_events) >= 2:
        return "P1 - Critical"

    if len(anomalies) >= 2 or len(correlated_events) >= 1:
        return "P2 - High"

    if len(anomalies) == 1:
        return "P3 - Medium"

    return "P4 - Low"


def analyze_incident_with_aiops(
    incident: str,
    metrics: dict[str, float],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Main AIOps analysis function.

    Produces operational intelligence that will be passed
    to the LangGraph INC Agent.
    """

    anomalies = detect_anomalies(metrics)

    correlated_events = correlate_events(events)

    noise_analysis = detect_noise(events)

    priority = calculate_priority(
        anomalies,
        correlated_events,
    )

    return {
        "incident": incident,
        "anomalies": anomalies,
        "correlated_events": correlated_events,
        "noise_analysis": noise_analysis,
        "priority": priority,
        "operational_impact": (
            "HIGH" if anomalies else "NORMAL"
        ),
    }


if __name__ == "__main__":

    test_incident = (
        "Payment application is returning HTTP 503 "
        "errors for multiple users."
    )

    test_metrics = {
        "cpu_percent": 94,
        "memory_percent": 91,
        "error_rate_percent": 18,
        "latency_seconds": 7.2,
    }

    test_events = [
        {
            "service": "payment-api",
            "message": "HTTP 503 error spike",
        },
        {
            "service": "payment-api",
            "message": "API latency above baseline",
        },
        {
            "service": "payment-api",
            "message": "HTTP 503 error spike",
        },
        {
            "service": "database",
            "message": "Connection pool utilization high",
        },
    ]

    result = analyze_incident_with_aiops(
        incident=test_incident,
        metrics=test_metrics,
        events=test_events,
    )

    print("\n========== AIOPS ANALYSIS ==========\n")

    for key, value in result.items():
        print(f"{key}:")
        print(value)
        print()