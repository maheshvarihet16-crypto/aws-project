import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="ollama API")

OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL")

class PromptRequest(BaseModel):
  prompt:str
  model:str = OLLAMA_MODEL
  
  
@app.get("/")  
def home():
  return{
    "message":"ollama API is running",
    "endpoints":{
      "health":"/health",
      "models":"/models",
      "health":"/health",
      "generate":"/generate",
    
    }
  }

@app.get("/health")  
async def health():
  try:
    async with httpx.AsyncClient() as Client:
     response=  await Client.get(f"{OLLAMA_BASE_URL}/api/tags")
   
    return{
      "status":"healthy",
      "models":response.json()["models"]
    }
  
  except Exception as e:
    return{
      "status":"unhealthy",
      "error":str(e)
    }
   

@app.get("/models")
async def models():
    async with httpx.AsyncClient() as Client:
     response=  await Client.get(f"{OLLAMA_BASE_URL}/api/tags")
     return response.json()
   
   
@app.post("/generate")
async def generate(request:PromptRequest):
  payload={
    "model":request.model,
    "prompt":request.prompt,
    "streame":False
  }
  
  async with httpx.AsyncClient(timeout=120) as client:
    response=await client.post(
      f"{OLLAMA_BASE_URL}/api/generate",
      json=payload
    )
  
  return response.json()  
  