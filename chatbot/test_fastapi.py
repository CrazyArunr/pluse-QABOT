# test_fastapi.py

import requests
import json

# Load queries from the JSON file
with open("data/queries.json", "r") as file:
    queries = json.load(file)

# FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8000/chat"

# Function to send a query to the FastAPI endpoint
def send_query(query):
    response = requests.post(FASTAPI_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Test all queries and store results
results = []
for query_data in queries:
    query = query_data["query"]
    response = send_query(query)
    results.append({"query": query, "response": response})

# Save results to a JSON file
with open("data/responses.json", "w") as file:
    json.dump(results, file, indent=4)

print("Responses saved to data/responses.json")