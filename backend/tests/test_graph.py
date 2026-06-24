import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from app.graph.workflow import build_graph


graph = build_graph()

result = graph.invoke(
    {
        "crisis_description": "Ransomware attack",
        "crisis_type": "Cyber Attack",
        "severity": "High",
        "stakeholders": ["Customers"],

        "business_analysis": "Revenue loss",
        "legal_analysis": "Possible compliance issue",
        "operations_analysis": "Servers down",
        "pr_analysis": "Negative media attention",

        "rag_context": ""
    }
)

print(result)