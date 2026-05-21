from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from docx import Document
import uuid
import os

app = FastAPI()

os.makedirs("downloads", exist_ok=True)

# 接收使用者輸入
class ChatInput(BaseModel):
    message: str

@app.post("/generate-doc")
def generate_doc(data: ChatInput):

    user_message = data.message

    filename = f"{uuid.uuid4()}.docx"
    path = f"downloads/{filename}"

    # 情緒分析（簡易版）
    emotion = "普通"

    if "難過" in user_message or "哭" in user_message:
        emotion = "悲傷"

    elif "壓力" in user_message or "累" in user_message:
        emotion = "壓力過大"

    elif "開心" in user_message or "快樂" in user_message:
        emotion = "快樂"

    # 建立 Word
    doc = Document()

    doc.add_heading("情緒分析報告", level=1)

    doc.add_paragraph(f"使用者輸入：{user_message}")

    doc.add_paragraph(f"分析情緒：{emotion}")

    # 不同情緒給不同建議
    if emotion == "悲傷":
        doc.add_paragraph("建議：可以找信任的人聊聊，適當休息。")

    elif emotion == "壓力過大":
        doc.add_paragraph("建議：深呼吸、放鬆、安排休息時間。")

    elif emotion == "快樂":
        doc.add_paragraph("建議：保持這份好心情！")

    else:
        doc.add_paragraph("建議：持續觀察自己的情緒變化。")

    doc.save(path)

    return {
        "message": "情緒分析完成",
        "download_url": f"https://maiagent-download.onrender.com/download/{filename}"
    }

@app.get("/download/{filename}")
def download(filename: str):

    path = f"downloads/{filename}"

    return FileResponse(
        path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )