import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "*" during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
print("API KEY:", os.getenv("GEMINI_API_KEY"))
try:
    gemini_client = genai.Client()
    klaude_chat = gemini_client.chats.create(model="gemini-2.5-flash")
except Exception as e:
    print("Warning: GEMINI_API_KEY environment variable not found.")
    gemini_client = None

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def get_home():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if not klaude_chat:
        raise HTTPException(status_code=500, detail="Klaude Chat Session is not configured.")

    try:
        response = klaude_chat.send_message(user_message)
        return {"response": response.text}

    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get response from Klaude.")

app.mount("/", StaticFiles(directory="."), name="static")