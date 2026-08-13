import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from web_screenshot import capture_website

app = FastAPI()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "saved_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class Item(BaseModel):
    url: str

@app.get("/api")
def health():
    return 'Server is running'

@app.post("/capture/")
def capture_site(item: Item):
    file_name = capture_website(item.url, output_dir=UPLOAD_DIR)

    if file_name is None:
        raise HTTPException(status_code=400, detail="웹사이트 캡처에 실패했습니다.")

    file_path = os.path.join(UPLOAD_DIR, file_name)
    return FileResponse(
        path=file_path,
        media_type="image/png",
        filename=file_name,
    )