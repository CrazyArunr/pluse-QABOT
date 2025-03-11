import json
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain.callbacks.base import BaseCallbackHandler
from pydantic import BaseModel, ConfigDict

# Fix for Pydantic validation error
class CustomCallbackHandler(BaseCallbackHandler):
    model_config = ConfigDict(arbitrary_types_allowed=True)

# Load your JSON data with updated login steps
data = [
    {
        "feature": "Login Functionality",
        "scenarios": [
            {
                "title": "Valid login with correct credentials",
                "steps": [
                    {"step": "open Chrome browser", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/login'", "description": "Navigates to the login page"},
                    {"step": "maximize the browser window", "description": "Maximizes the browser window"},
                    {"step": "enter 'testuser' into the element with locator '#username'", "description": "Enters the username into the input field"},
                    {"step": "enter 'password123' into the element with locator '#password'", "description": "Enters the password into the input field"},
                    {"step": "click on the element with locator '#login-button'", "description": "Clicks the login button"},
                    {"step": "wait for the element with locator '#dashboard' to be visible", "description": "Waits for the dashboard to load"},
                    {"step": "the element with locator '#dashboard' should be displayed", "description": "Verifies if the dashboard is displayed"},
                    {"step": "the page title should be 'User Dashboard'", "description": "Verifies if the title of the page is 'User Dashboard'"},
                    {"step": "the page URL should be 'https://example.com/dashboard'", "description": "Verifies if the URL is correct"}
                ]
            },
            {
                "title": "Unsuccessful login with invalid credentials",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens the Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/login'", "description": "Navigates to the login page"},
                    {"step": "maximize the browser window", "description": "Maximizes the browser window"},
                    {"step": "wait for 2 seconds", "description": "Waits for 2 seconds"},
                    {"step": "enter 'invalid_email@example.com' into the element with locator '#email'", "description": "Enters an invalid email into the email field"},
                    {"step": "enter 'invalidpassword' into the element with locator '#pass'", "description": "Enters an invalid password into the password field"},
                    {"step": "click on the element with locator '#loginbutton'", "description": "Clicks the login button"},
                    {"step": "wait for the element with locator '#error_box' to be visible", "description": "Waits for the error box to be visible"},
                    {"step": "the element with locator '#error_box' should be displayed", "description": "Verifies if the error box is displayed"},
                    {"step": "the element with locator '#error_box' should have text 'The username or password you entered is incorrect.'", "description": "Verifies if the error message is correct"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            },
            {
                "title": "Login attempt with empty fields",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens the Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/login'", "description": "Navigates to the login page"},
                    {"step": "maximize the browser window", "description": "Maximizes the browser window"},
                    {"step": "wait for 2 seconds", "description": "Waits for 2 seconds"},
                    {"step": "clear the input field with locator '#email'", "description": "Clears the email input field"},
                    {"step": "clear the input field with locator '#pass'", "description": "Clears the password input field"},
                    {"step": "click on the element with locator '#loginbutton'", "description": "Clicks the login button"},
                    {"step": "wait for the element with locator '#error_box' to be visible", "description": "Waits for the error box to be visible"},
                    {"step": "the element with locator '#error_box' should be displayed", "description": "Verifies if the error box is displayed"},
                    {"step": "the element with locator '#error_box' should have text 'Please enter both a username and password.'", "description": "Verifies if the error message is correct"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            }
        ]
    },
    {
        "feature": "Profile Update",
        "scenarios": [
            {
                "title": "Profile update with invalid phone number",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/login'", "description": "Navigates to the login page"},
                    {"step": "enter 'testuser' into the element with locator '#username'", "description": "Enters the username"},
                    {"step": "enter 'password123' into the element with locator '#password'", "description": "Enters the password"},
                    {"step": "click on the element with locator '#login-button'", "description": "Clicks the login button"},
                    {"step": "wait for the element with locator '#dashboard' to be visible", "description": "Waits for the dashboard to load"},
                    {"step": "navigate to the URL 'https://example.com/profile'", "description": "Navigates to the profile page"},
                    {"step": "clear the input field with locator '#phone'", "description": "Clears the phone number field"},
                    {"step": "enter 'abcd1234' into the element with locator '#phone'", "description": "Enters an invalid phone number"},
                    {"step": "click on the element with locator '#save-button'", "description": "Clicks the Save button"},
                    {"step": "wait for the element with locator '#error-message' to be visible", "description": "Waits for the error message"},
                    {"step": "the element with locator '#error-message' should have text 'Invalid phone number format'", "description": "Verifies the error message"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            },
            {
                "title": "Profile update with valid phone number",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/login'", "description": "Navigates to the login page"},
                    {"step": "enter 'testuser' into the element with locator '#username'", "description": "Enters the username"},
                    {"step": "enter 'password123' into the element with locator '#password'", "description": "Enters the password"},
                    {"step": "click on the element with locator '#login-button'", "description": "Clicks the login button"},
                    {"step": "wait for the element with locator '#dashboard' to be visible", "description": "Waits for the dashboard to load"},
                    {"step": "navigate to the URL 'https://example.com/profile'", "description": "Navigates to the profile page"},
                    {"step": "clear the input field with locator '#phone'", "description": "Clears the phone number field"},
                    {"step": "enter '1234567890' into the element with locator '#phone'", "description": "Enters a valid phone number"},
                    {"step": "click on the element with locator '#save-button'", "description": "Clicks the Save button"},
                    {"step": "wait for the element with locator '#success-message' to be visible", "description": "Waits for the success message"},
                    {"step": "the element with locator '#success-message' should have text 'Profile updated successfully'", "description": "Verifies the success message"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            }
        ]
    },
    {
        "feature": "User Registration",
        "scenarios": [
            {
                "title": "Successful user registration",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/register'", "description": "Navigates to the registration page"},
                    {"step": "enter 'newuser' into the element with locator '#username'", "description": "Enters a new username"},
                    {"step": "enter 'newemail@example.com' into the element with locator '#email'", "description": "Enters a new email"},
                    {"step": "enter 'password123' into the element with locator '#password'", "description": "Enters a password"},
                    {"step": "enter 'password123' into the element with locator '#confirm-password'", "description": "Confirms the password"},
                    {"step": "click on the element with locator '#register-button'", "description": "Clicks the Register button"},
                    {"step": "wait for the element with locator '#success-message' to be visible", "description": "Waits for success message"},
                    {"step": "the element with locator '#success-message' should have text 'Registration successful'", "description": "Verifies success message"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            },
            {
                "title": "Registration with existing email",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/register'", "description": "Navigates to the registration page"},
                    {"step": "enter 'existinguser' into the element with locator '#username'", "description": "Enters a username"},
                    {"step": "enter 'existingemail@example.com' into the element with locator '#email'", "description": "Enters an existing email"},
                    {"step": "enter 'password123' into the element with locator '#password'", "description": "Enters a password"},
                    {"step": "enter 'password123' into the element with locator '#confirm-password'", "description": "Confirms the password"},
                    {"step": "click on the element with locator '#register-button'", "description": "Clicks the Register button"},
                    {"step": "wait for the element with locator '#error-message' to be visible", "description": "Waits for the error message"},
                    {"step": "the element with locator '#error-message' should have text 'Email already exists'", "description": "Verifies error message for duplicate email"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            }
        ]
    },
    {
        "feature": "Password Reset",
        "scenarios": [
            {
                "title": "Successful password reset",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/reset-password'", "description": "Navigates to the reset password page"},
                    {"step": "enter 'testuser@example.com' into the element with locator '#email'", "description": "Enters a registered email"},
                    {"step": "click on the element with locator '#reset-button'", "description": "Clicks the Reset button"},
                    {"step": "wait for the element with locator '#success-message' to be visible", "description": "Waits for success message"},
                    {"step": "the element with locator '#success-message' should have text 'Password reset link sent'", "description": "Verifies success message"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            },
            {
                "title": "Reset password with unregistered email",
                "steps": [
                    {"step": "open browser 'chrome'", "description": "Opens Chrome browser"},
                    {"step": "navigate to the URL 'https://example.com/reset-password'", "description": "Navigates to the reset password page"},
                    {"step": "enter 'fakeuser@example.com' into the element with locator '#email'", "description": "Enters an unregistered email"},
                    {"step": "click on the element with locator '#reset-button'", "description": "Clicks the Reset button"},
                    {"step": "wait for the element with locator '#error-message' to be visible", "description": "Waits for the error message"},
                    {"step": "the element with locator '#error-message' should have text 'Email not found'", "description": "Verifies error message for non-existent email"},
                    {"step": "close the browser", "description": "Closes the browser"}
                ]
            }
        ]
    }
]

# Convert JSON data to LangChain Documents
documents = []
for feature in data:
    for scenario in feature["scenarios"]:
        content = f"Feature: {feature['feature']}\nScenario: {scenario['title']}\n"
        for step in scenario["steps"]:
            content += f"{step['step']}\n{step['description']}\n"
        documents.append(Document(page_content=content, metadata={"feature": feature["feature"], "scenario": scenario["title"]}))

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key="xxxxx")

# Create FAISS vector store
vector_store = FAISS.from_documents(documents, embeddings)

# Initialize OpenAI LLM
openai_llm = ChatOpenAI(model="gpt-4", temperature=0.1, openai_api_key="xxxxx")

# Create RAG pipeline
rag_pipeline = RetrievalQA.from_chain_type(llm=openai_llm, chain_type="stuff", retriever=vector_store.as_retriever())

# Define a custom tool for the RAG pipeline
class RAGTool(BaseTool):
    name: str = "RAG Pipeline"  # Explicit type annotation
    description: str = "Use this tool to answer questions based on the injected data."  # Explicit type annotation

    def _run(self, query: str) -> str:
        return rag_pipeline.run(query)

# Initialize the agent with the RAG tool
tools = [RAGTool()]
agent = initialize_agent(tools, openai_llm, agent="zero-shot-react-description", verbose=True)

# Function to get response from the chatbot
def get_response(query):
    # Check if the query is a greeting
    if any(greeting in query.lower() for greeting in ["hi", "hello", "who created you", "who made you"]):
        return "Hello! I was created by the Pulse QA team to assist with testing scenarios and answering questions about the application."
    
    # Check if the query is related to the injected data
    if any(keyword in query.lower() for keyword in ["login", "registeration", "profile", "logout", "password"]):
        # Use the RAG pipeline to retrieve relevant steps
        rag_response = rag_pipeline.run(query)
        
        # Debug: Print the raw response from the RAG pipeline
        print("Raw RAG Response:", rag_response)
        
        # Ask the AI to format the RAG response into the desired BDD format
        bdd_prompt = (
            f"Convert the following steps into BDD (Gherkin) format. "
            f"Use the exact locators and steps from the input. "
            f"Do not rephrase or simplify the steps. "
            f"Use a general tone without using 'I'. "
            f"Follow this format:\n\n"
            f"Given open browser 'chrome'\n"  # Explicitly format the first step
            f"And navigate to the URL '<URL>'\n"
            f"And maximize the browser window\n"
            f"When enter '<value>' into the element with locator '<locator>'\n"
            f"And click on the element with locator '<locator>'\n"
            f"Then wait for the element with locator '<locator>' to be visible\n"
            f"And the element with locator '<locator>' should be displayed\n"
            f"And the page title should be '<title>'\n"
            f"And the page URL should be '<URL>'\n\n"
            f"Input:\n{rag_response}"
        )
        bdd_response = openai_llm.predict(bdd_prompt)
        print(bdd_response)
        
        return bdd_response
        
    else:
        # Use the agent for other queries
        return agent.run(query)

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit UI
st.title("Pluse QA Automation Chatbot")

# Display conversation history
for message in st.session_state.conversation_history:
    st.write(f"{message['role']}: {message['content']}")

# Input for user query
user_query = st.text_input("You: ", "")

if user_query:
    # Get response from the chatbot
    response = get_response(user_query)
    
    # Update conversation history
    st.session_state.conversation_history.append({"role": "User", "content": user_query})
    st.session_state.conversation_history.append({"role": "Bot", "content": response})
    
    # Display the response
    st.write(f"Bot: {response}")
