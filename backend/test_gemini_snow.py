import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

# Mock ServiceNow incident
incident = {
    "number": "INC0010001",
    "short_description": "Payment Gateway is timing out",
    "description": (
        "Multiple users are unable to complete payment transactions. "
        "Application requests are timing out."
    ),
    "priority": "1 - Critical",
    "category": "Application",
    "assignment_group": "Payments Support",
    "recent_errors": [
        "Database connection timeout",
        "Connection pool exhausted",
        "HTTP 504 responses increased"
    ]
}

prompt = f"""
You are an Enterprise IT Incident Insights Agent.

Analyze the following ServiceNow incident.

Incident:
{incident}

Provide the following:

1. Executive Summary
2. Business Impact
3. Likely Root Cause
4. Evidence
5. Recommended Next Actions
6. Risk Level
7. Confidence Score

Do not invent facts that are not present in the incident.
Clearly distinguish between observed evidence and hypotheses.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
)

print("\n" + "=" * 70)
print("GEMINI INCIDENT INSIGHTS")
print("=" * 70)
print(response.text)
print("=" * 70)