# FastAPI Chatbot for QA Automation

Getting answers automatically is magic!! It's real AI (remember, the Turing Test?).

This project is a FastAPI-based chatbot designed to assist with QA automation scenarios. It uses OpenAI's GPT-4 model and a Retrieval-Augmented Generation (RAG) pipeline to answer questions based on predefined testing scenarios.

---

## Table of Contents

1. [Application Scope](#application-scope)
2. [Notes](#notes)
3. [The Way It Works](#the-way-it-works)
4. [Scripts](#scripts)
5. [Data](#data)
6. [To Run](#to-run)
7. [API Endpoint](#api-endpoint)
8. [Dependencies](#dependencies)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgments](#acknowledgments)


---

## Application Scope

- **Automation of Mundane Queries**: Automates repetitive QA tasks, saving time and effort.
- **Scalability**: Handles large-scale testing scenarios effortlessly.
- **Security**: All models and data are local, ensuring better security for sensitive data (e.g., HR or Finance).

---

## Notes

- This chatbot uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information and generate responses.
- Built with **FastAPI**, **LangChain**, and **OpenAI's GPT-4**.

---




## The Way It Works

1. **Data Preparation**:
   - You supply FAQs in the form of JSON files containing scenarios and steps (e.g., login, registration, password reset).
   - The data is converted into LangChain Documents and stored in a FAISS vector store for efficient retrieval.

2. **Query Processing**:
   - When a user query comes in, the chatbot uses the RAG pipeline to retrieve the most relevant information.
   - The response is formatted into BDD (Gherkin) format for clarity and usability.

3. **Response Generation**:
   - The chatbot generates a response based on the retrieved information and presents it to the user.

---

## Scripts

- **main.py**: FastAPI application serving the chatbot API.
- **models/rag_tool.py**: Core logic for the RAG pipeline and agent initialization.
- **utils/response_handler.py**: Handles user queries and generates responses.
- **test_fastapi.py**: Script to test the FastAPI endpoint with sample queries.

---

## Data

- **data/queries.json**: Contains sample queries for testing the chatbot.
- **data/responses.json**: Stores the chatbot's responses to the queries.

---

## To Run

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
