from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    history: list[list[str]] = []

class ChatResponse(BaseModel):
    response: str
