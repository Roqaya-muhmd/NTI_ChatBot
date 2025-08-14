from fastapi import FastAPI
from pydantic import BaseModel #make data validation
class query(BaseModel):
    userid: str
    messsage: str
app=FastAPI()
@app.get("/")
def read_root():
    return"hello world"
@app.post("/chat/")
def chat(query: query):
    return{"message":f"user{query.userid }says:{query.messsage}"}
from dotenv import load_dotenv
load_dotenv()
from cohere import ClientV2
import os
x=os.getenv("Together_API_Key")
client = ClientV2(api_key=x)        
client.chat(
	model="command-a-03-2025",
	messages=[],
	temperature=0.3
)