from app.services.retriever import retrieve

query = "How should an organization respond to a cybersecurity incident?"

results = retrieve(query)

print("\nRetrieved Results:\n")

for item in results:
    print(f"Category : {item['category']}")
    print(f"Source   : {item['source']}")
    print(f"Text     : {item['text']}")
    print("-" * 50)