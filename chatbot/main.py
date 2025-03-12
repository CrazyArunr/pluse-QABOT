# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from utils.response_handler import get_response

app = FastAPI()

# Pydantic model for request body
class QueryModel(BaseModel):
    query: str

# API endpoint to handle chatbot queries
@app.post("/chat")
async def chat(query_model: QueryModel):
    query = query_model.query
    response = get_response(query)
    return {"response": response}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)