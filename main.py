from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import docx
from io import BytesIO
from chatbot import ask_chatbot

app = FastAPI(title="Writing Assistant API")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bootstrap", StaticFiles(directory="node_modules/bootstrap/dist"), name="bootstrap")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

def extract_text_from_file(content: bytes, filename: str) -> str:
    if filename.lower().endswith('.txt'):
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content.decode('latin-1')
    elif filename.lower().endswith('.docx'):
        doc = docx.Document(BytesIO(content))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    else:
        raise HTTPException(status_code=400, detail="Only .txt and .docx files are supported.")

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = os.path.basename(file.filename)
        content = await file.read()
        plain_text = extract_text_from_file(content, filename)
        with open("latest_plot.txt", "w", encoding="utf-8") as f:
            f.write(plain_text)
        return {
            "filename": filename,
            "status": "saved",
            "reply": f"I've received '{filename}' and saved it to the plot database."
        }
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    plot_data = ""
    if os.path.exists("latest_plot.txt"):
        with open("latest_plot.txt", "r", encoding="utf-8") as f:
            plot_data = f.read()
    reply = ask_chatbot(request.message, plot_context=plot_data)
    return ChatResponse(reply=reply)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')