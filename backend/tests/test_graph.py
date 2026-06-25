from app.graph.workflow import build_graph

graph = build_graph()

result = graph.invoke(
    {
        "crisis_description": "A ransomware attack has encrypted company servers.",
        "stakeholders": [],
        "recommendations": []
    }
)

print("\n===== FINAL OUTPUT =====")
print(result)