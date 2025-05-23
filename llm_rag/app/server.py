import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import extract_text_from_pdf, get_completion

app = FastAPI()
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat histories per session (simple memory)
chat_histories = {}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = Form(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, f"{session_id}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        chat_histories[session_id] = {"file": file_path, "history": []}
        return {"message": f"File '{file.filename}' uploaded successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/chat")
async def chat(session_id: str = Form(...), user_input: str = Form(...)):
    history = chat_histories.get(session_id)
    if not history:
        return JSONResponse(status_code=400, content={"error": "Session not found or file not uploaded."})

    file_path = history["file"]
    filename = os.path.basename(file_path)

    # Determine how to read the file
    if filename.endswith(".pdf"):
        content = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    # Dummy logic: replace with LLM logic
    # response = f"File has {len(content.splitlines())} lines. You asked: {user_input}"
    response = get_completion(user_input)
    history["history"].append({"user": user_input, "bot": response})
    return {"response": response, "history": history["history"]}
