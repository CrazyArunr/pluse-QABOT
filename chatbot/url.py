import time
import requests
import subprocess

# Start the FastAPI server in a separate process
server_process = subprocess.Popen(["uvicorn", "Ai:app", "--host", "0.0.0.0", "--port", "5173"])

# Wait for the server to start (adjust the sleep time if needed)
time.sleep(5)

# Define the URL and payload
url = "http://127.0.0.1:5173/chat"
payload = {"query": "How do I login?"}

try:
    # Send a POST request
    response = requests.post(url, json=payload)
    print(response.status_code)
    print(response.json())
except requests.exceptions.ConnectionError as e:
    print(f"Failed to connect to the server: {e}")
finally:
    # Terminate the server process
    server_process.terminate()
