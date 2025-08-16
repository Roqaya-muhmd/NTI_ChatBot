from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import os
from cohere import Client

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def greet():
    return "hello world"

@app.get("/greet")
def greet_user():
    return {"message": "hello"}

@app.post("/chatresponse")
async def get_response(chat_request: ChatRequest):
    try:
        # Initialize Cohere client
        api_key = os.getenv("Together_API_Key")  # Make sure this matches your .env variable name
        if not api_key:
            return {"error": "API key not configured"}
            
        cohere_client = Client(api_key=api_key)
        
        response = cohere_client.chat(
            model="command",  # Using the command model
            message=chat_request.prompt,
            temperature=0.7
        )
        
        return {
            "prompt": chat_request.prompt,
            "response": response.text
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)