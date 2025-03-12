FastAPI Chatbot for QA Automation
This project is a FastAPI-based chatbot designed to assist with QA automation scenarios. It uses OpenAI's GPT-4 model and a Retrieval-Augmented Generation (RAG) pipeline to answer questions based on predefined testing scenarios.
Table of Contents
Project Structure

Prerequisites

Setup

Running the Application

Testing the API

API Endpoint

Contributing

License
Project Structure
fastapi_chatbot/
│
├── config/
│   └── config.py          # Configuration file for API keys
│
├── data/
│   ├── queries.json       # JSON file with sample queries
│   └── responses.json     # JSON file to store chatbot responses
│
├── models/
│   └── rag_tool.py        # RAG tool and agent initialization
│
├── utils/
│   └── response_handler.py # Function to handle chatbot responses
│
├── main.py                # FastAPI application
│
├── test_fastapi.py        # Script to test the FastAPI endpoint
│
├── requirements.txt       # Dependencies
│
└── README.md              # This file
Prerequisites
Before running the application, ensure you have the following installed:

Python 3.8 or higher

Poetry (optional, for dependency management)

OpenAI API key (store it in config/config.py)
Setup
Clone the Repository:

bash
Copy
git clone https://github.com/CrazyArunr/pluse-QABOT.git
cd fastapi-chatbot
Install Dependencies:

Install the required Python packages using pip:

bash
Copy
pip install -r requirements.txt
Alternatively, if you're using Poetry:

bash
Copy
poetry install
Add OpenAI API Key:

Create a config/config.py file.

Add your OpenAI API key:

python
Copy
# config/config.py
OPENAI_API_KEY = "your_openai_api_key_here"
Add Sample Queries:

Add your sample queries to data/queries.json. Example:

[
    {"query": "How do I login with valid credentials?"},
    {"query": "What are the steps for user registration?"},
    {"query": "How do I reset my password?"}
]
Running the Application
Start the FastAPI Server:

Run the following command to start the FastAPI application:

bash
Copy
python main.py
The application will be available at http://localhost:8000.

Access the API:

You can interact with the API using the /chat endpoint. 
For example:

bash
Copy
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"query": "How do I login?"}'
Testing the API
To test the API with the sample queries in data/queries.json, run the following script:

bash
Copy
python test_fastapi.py
This will:

Send each query to the /chat endpoint.

Save the responses to data/responses.json.

API Endpoint
POST /chat
Description: Accepts a user query and returns a response from the chatbot.

Request Body:

json
Copy
{
    "query": "How do I login?"
}
Response:

json
Copy
{
    "response": "Feature: Login Functionality\nScenario: Valid login with correct credentials\nGiven open browser 'chrome'\nAnd navigate to the URL 'https://example.com/login'\nAnd maximize the browser window\nWhen enter 'testuser' into the element with locator '#username'\nAnd enter 'password123' into the element with locator '#password'\nAnd click on the element with locator '#login-button'\nThen wait for the element with locator '#dashboard' to be visible\nAnd the element with locator '#dashboard' should have text 'User Dashboard'"
}

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Built with FastAPI.

Powered by OpenAI and LangChain.

This README.md provides a comprehensive guide for setting up, running, and contributing to the project. You can customize it further based on your specific needs.
