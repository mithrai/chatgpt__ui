from fastapi import FastAPI
from pydantic import BaseModel
from app.model import generate_response

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def chat(request: PromptRequest):
    response = generate_response(request.prompt)
    return {"response": response}
