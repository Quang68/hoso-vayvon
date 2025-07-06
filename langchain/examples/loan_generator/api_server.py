from langsmith import traceable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import uvicorn
import os
from langchain_together import Together
from dotenv import load_dotenv
import re

# Load biến môi trường
load_dotenv()

# Khởi tạo LLM
llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    temperature=0.0,
    max_tokens=1024,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

# Khởi tạo app FastAPI
app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khai báo schema nhận từ frontend
class DynamicData(BaseModel):
    system_prompt: str  # 👈 thêm system prompt
    prompt: str          # nội dung prompt chính
    data: Dict[str, str] # dữ liệu người dùng nhập

# Endpoint tạo hồ sơ
@app.post("/generate-document")
@traceable
def generate_doc(request_data: DynamicData):
    # Ghép prompt
    combined_prompt = f"{request_data.system_prompt.strip()}\n\n{request_data.prompt.strip()}"

    # Thay thế biến {key} trong prompt
    for key, value in request_data.data.items():
        combined_prompt = combined_prompt.replace(f"{{{key}}}", value)

    # Gọi LLM sinh nội dung
    result = llm.invoke(combined_prompt)
    if hasattr(result, "content"):
        result = result.content

    # Xử lý loại bỏ tag <think> nếu có
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL)
    result = re.sub(r"<?think>", "", result)
    result = re.sub(r"</?think>", "", result)
     # ✅ Lấy từ "Thông tin:" trở đi
    match = re.search(r"Thông tin:(.|\n)*", result)
    if match:
        result = match.group(0)
    else:
        result = result.strip()

    return {"document": result}

# Khởi động server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
