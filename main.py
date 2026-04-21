from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import base64
from chatbot import ask_chatbot 

#FastAPI automatically use Swagger UI to visualize API responses. Mount first then Check @app.get("/")
app = FastAPI(title="Writing Assistant API")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bootstrap", StaticFiles(directory="node_modules/bootstrap/dist"), name="bootstrap")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # remove potential ../
        filename = os.path.basename(file.filename)
        
        content = await file.read()
        
        with open(f"latest_plot.txt", "wb") as f:
            f.write(content)
        return {
            "filename": filename, 
            "status": "saved", 
            "reply": f"I've received '{filename}' and saved it to the plot database."
        }
            
        # Base64 encode to go through BaseModel validation
        # encoded = base64.b64encode(content).decode('utf-8')
        
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    plot_data = ""
    if os.path.exists("latest_plot.txt"): 
        with open("latest_plot.txt", "rb") as f:
            plot_data = f.read()

    reply = ask_chatbot(request.message, plot_context=plot_data)
    return ChatResponse(reply=reply)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')