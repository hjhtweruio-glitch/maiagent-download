from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openpyxl import Workbook
import uuid
import os

app = FastAPI()

os.makedirs("downloads", exist_ok=True)

# 接收使用者輸入
class ChatInput(BaseModel):
    message: str

@app.post("/generate-excel")
def generate_excel(data: ChatInput):

    user_message = data.message

    filename = f"{uuid.uuid4()}.xlsx"
    path = f"downloads/{filename}"

    # 情緒分析
    emotion = "普通"
    score = 50

    if "難過" in user_message or "哭" in user_message:
        emotion = "悲傷"
        score = 20

    elif "壓力" in user_message or "累" in user_message:
        emotion = "壓力過大"
        score = 35

    elif "開心" in user_message or "快樂" in user_message:
        emotion = "快樂"
        score = 90

    # 建立 Excel
    wb = Workbook()

    ws = wb.active
    ws.title = "情緒分析"

    # 標題
    ws["A1"] = "使用者輸入"
    ws["B1"] = "分析情緒"
    ws["C1"] = "情緒分數"
    ws["D1"] = "建議"

    # 資料
    ws["A2"] = user_message
    ws["B2"] = emotion
    ws["C2"] = score

    # 建議
    if emotion == "悲傷":
        ws["D2"] = "建議找信任的人聊聊"

    elif emotion == "壓力過大":
        ws["D2"] = "建議休息與放鬆"

    elif emotion == "快樂":
        ws["D2"] = "保持好心情"

    else:
        ws["D2"] = "持續觀察情緒"

    wb.save(path)

    return {
        "message": "Excel 已生成",
        "download_url": f"https://maiagent-download.onrender.com/download/{filename}"
    }

@app.get("/download/{filename}")
def download(filename: str):

    path = f"downloads/{filename}"

    return FileResponse(
        path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )