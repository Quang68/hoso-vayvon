from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict
import uvicorn
from langsmith import traceable

# Import các adapter
from adapters import llm_adapter, template_adapter, storage_adapter

# Khởi tạo app FastAPI
app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Cho phép tất cả frontend
    allow_credentials=False,        # Phải False nếu allow_origins = ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa schema nhận từ frontend
class DynamicData(BaseModel):
    system_prompt: str
    prompt: str
    data: Dict[str, str]
    document_name: str
    template_id: str
    document_type_id: str
    customer_id: str

# API endpoint chính
@app.post("/generate-document")
@traceable
async def generate_document(payload: DynamicData):
    print("=" * 60)
    print("🎯 API REQUEST RECEIVED")
    print("=" * 60)
    
    print("✅ TEMPLATE ID nhận từ React:", payload.template_id)
    print("📝 DOCUMENT NAME:", payload.document_name)
    print("👤 CUSTOMER ID:", payload.customer_id)
    print("📄 DOCUMENT TYPE ID:", payload.document_type_id)
    
    print("\n🔧 SYSTEM PROMPT:")
    print("-" * 40)
    print(payload.system_prompt)
    
    print("\n📋 USER PROMPT:")
    print("-" * 40)
    print(payload.prompt)
    
    print("\n📊 INPUT DATA (từ React):")
    print("-" * 40)
    import json
    print(json.dumps(payload.data, ensure_ascii=False, indent=2))
    
    try:
        # 1. Enrich nội dung bằng LLM
        print("\n🤖 BƯỚC 1: Gọi LLM để enrich data...")
        enriched = llm_adapter.enrich_data(
            payload.system_prompt, payload.prompt, payload.data
        )
        
        print("\n✨ ENRICHED DATA (sau khi LLM xử lý):")
        print("-" * 40)
        print(json.dumps(enriched, ensure_ascii=False, indent=2))

        # 2. Render template DOCX từ dữ liệu đã enrich
        print("\n📄 BƯỚC 2: Render template DOCX...")
        print(f"Template ID sử dụng: {payload.template_id}")
        docx_path = template_adapter.render_docx(payload.template_id, enriched)
        print(f"✅ DOCX file tạo tại: {docx_path}")

        # 3. Upload file lên Google Drive, trả về link
        print("\n☁️ BƯỚC 3: Upload lên Google Drive...")
        file_id, file_url = storage_adapter.upload_to_drive(
            docx_path, payload.document_name
        )
        print(f"✅ Upload thành công! File ID: {file_id}")
        print(f"🔗 Link: {file_url}")

        # 4. Storage: React sẽ handle Firebase, không cần lưu ở đây
        print("\n💾 BƯỚC 4: Storage...")
        print("✅ React sẽ handle việc lưu vào Firebase")
        print("📝 LangChain chỉ trả về data cho React")

        print("\n🎉 HOÀN THÀNH!")
        print("=" * 60)
        
        return {
            "status": "success",
            "document_url": file_url,
            "content": enriched["output"],
            "file_id": file_id,
            "enriched_data": enriched,  # ← React có thể dùng để lưu Firebase
            "valuation": enriched.get("Valuation", None),  # ← Extract riêng cho dễ dùng
            "metadata": {
                "customer_id": payload.customer_id,
                "document_name": payload.document_name,
                "document_type_id": payload.document_type_id,
                "template_id": payload.template_id
            }
        }

    except Exception as e:
        print(f"\n❌ LỖI XỬ LÝ: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

# Chạy server nếu gọi trực tiếp
if __name__ == "__main__":
    uvicorn.run("api_server:app", host="127.0.0.1", port=8000, reload=True)
