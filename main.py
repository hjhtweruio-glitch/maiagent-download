from fastapi import FastAPI
from fastapi.responses import FileResponse
from docx import Document
import uuid
import os

app = FastAPI()

os.makedirs("downloads", exist_ok=True)

@app.get("/generate-doc")
def generate_doc():

    filename = f"{uuid.uuid4()}.docx"

    path = f"downloads/{filename}"

    doc = Document()

    doc.add_heading("生理學題目", level=1)

    doc.add_paragraph("1. 人體最大的器官是皮膚")
    doc.add_paragraph("2. 心臟有四個腔室")

    doc.save(path)

    return {
        "message": "檔案已生成",
        "download_url": f"http://127.0.0.1:8000/download/{filename}"
    }

@app.get("/download/{filename}")
def download(filename: str):

    path = f"downloads/{filename}"

    return FileResponse(
        path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )