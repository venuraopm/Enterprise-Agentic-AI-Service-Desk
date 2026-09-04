from typing import TypedDict
from backend.app.aiops.aiops_service import analyze_incident_with_aiops
from backend.app.rag.rag_service import retrieve_incident_knowledge


from langgraph.graph import StateGraph, START, END


class IncidentState(TypedDict, total=False):
    incident: str

    # AIOps
    aiops_analysis: str
    aiops_priority: str
    aiops_anomalies: list[str]
    correlated_events: list[dict]
    noise_analysis: dict

    # RAG
    rag_context: str

    # AI analysis
    incident_analysis: str
    root_cause: str
    resolution: str


def aiops_node(state: IncidentState):
    """
    AIOps layer:
    Performs anomaly detection, event correlation,
    noise reduction and priority assessment.
    """

    incident = state.get("incident", "")

    # POC operational metrics
    metrics = {
        "cpu_percent": 94,
        "memory_percent": 91,
        "error_rate_percent": 18,
        "latency_seconds": 7.2,
    }

    # POC operational events
    events = [
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
        incident=incident,
        metrics=metrics,
        events=events,
    )

    return {
        "aiops_analysis": str(result),
        "aiops_priority": result["priority"],
        "aiops_anomalies": result["anomalies"],
        "correlated_events": result["correlated_events"],
        "noise_analysis": result["noise_analysis"],
    }


def rag_node(state: IncidentState):
    """
    RAG layer:
    Uses LangChain + ChromaDB to retrieve
    relevant enterprise knowledge for the incident.
    """

    incident = state.get("incident", "")

    documents = retrieve_incident_knowledge(
        incident,
        k=4
    )

    if not documents:
        return {
            "rag_context": "No relevant enterprise knowledge found."
        }

    context_parts = []

    for document in documents:
        source = document.metadata.get(
            "source",
            "Unknown"
        )

        content = document.page_content

        context_parts.append(
            f"Source: {source}\n"
            f"Content:\n{content}"
        )

    rag_context = "\n\n---\n\n".join(
        context_parts
    )

    return {
        "rag_context": rag_context
    }


def incident_analysis_node(state: IncidentState):
    """
    Incident analysis:
    This will later use LangChain + LLM
    to analyze the incident using the AIOps
    and RAG context.
    """

    return {
        "incident_analysis": (
            "Incident analysis completed using "
            "AIOps information and retrieved knowledge."
        )
    }


def rca_node(state: IncidentState):
    """
    Root Cause Analysis.
    """

    return {
        "root_cause": (
            "Probable root cause identified from "
            "incident context and available evidence."
        )
    }


def resolution_node(state: IncidentState):
    """
    Resolution recommendation.
    """

    return {
        "resolution": (
            "Recommended resolution generated. "
            "Human approval will be required before "
            "production action."
        )
    }


def build_incident_graph():
    """
    Builds the LangGraph workflow for the INC Agent.
    """

    graph = StateGraph(IncidentState)

    # Register nodes
    graph.add_node("aiops", aiops_node)
    graph.add_node("rag", rag_node)
    graph.add_node("incident_analysis", incident_analysis_node)
    graph.add_node("rca", rca_node)
    graph.add_node("resolution", resolution_node)

    # Define workflow
    graph.add_edge(START, "aiops")
    graph.add_edge("aiops", "rag")
    graph.add_edge("rag", "incident_analysis")
    graph.add_edge("incident_analysis", "rca")
    graph.add_edge("rca", "resolution")
    graph.add_edge("resolution", END)

    return graph.compile()


# Create the compiled INC Agent
inc_agent = build_incident_graph()


if __name__ == "__main__":
    test_incident = {
        "incident": (
            "Payment application is returning HTTP 503 errors "
            "for multiple users."
        )
    }

    result = inc_agent.invoke(test_incident)

    print("\n========== INC AGENT RESULT ==========\n")

    for key, value in result.items():
        print(f"{key}:")
        print(value)
        print()