# api_server.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from langchain.prompts import PromptTemplate
from langchain_together import Together
from dotenv import load_dotenv
import re

load_dotenv()

llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    temperature=0.0,
    max_tokens=1024,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

with open("prompt_template.txt", "r", encoding="utf-8") as f:
    template_text = f.read()
template = PromptTemplate.from_template(template_text)

app = FastAPI()

# Cho phép ReactJS gọi API từ localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc thay bằng ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    name: str
    address: str
    amount: str

@app.post("/generate-document")
def generate_doc(data: InputData):
    filled_prompt = template.format(
        name=data.name,
        address=data.address,
        amount=data.amount
    )
    result = llm.invoke(filled_prompt)
    if hasattr(result, "content"):
        result = result.content

    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL)
    result = re.sub(r"</?think>", "", result)
    result = re.sub(r"<?think>", "", result)
    return {"document": result}

# Chạy server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
