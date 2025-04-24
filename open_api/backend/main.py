from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse
from llm_manager import generate_response

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    message = chat_request.message

    if not message.strip():
        raise HTTPException(status_code=400, detail="Message is required.")

    try:
        # Call the LLM response generator function
        generated = await generate_response(message)
        return ChatResponse(response=generated)
    except Exception as e:
        print(f"Error during LLM processing: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response from LLM.")
