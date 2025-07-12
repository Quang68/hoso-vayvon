# Mock Firestore service - tạm thời không lưu vào database
import datetime
import json
import os

def save_document_content(customer_id, document_name, document_type_id, content):
    """Tạm thời lưu vào file local thay vì Firestore"""
    try:
        # Tạo thư mục logs nếu chưa có
        os.makedirs("logs", exist_ok=True)
        
        # Tạo log entry
        log_entry = {
            "customer_id": customer_id,
            "document_name": document_name,
            "document_type_id": document_type_id,
            "created_at": datetime.datetime.now().isoformat(),
            "content": content[:200] + "..." if len(content) > 200 else content  # Cắt ngắn content
        }
        
        # Lưu vào file log
        log_file = f"logs/documents_{datetime.date.today().isoformat()}.json"
        
        # Đọc file cũ (nếu có)
        logs = []
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        # Thêm log mới
        logs.append(log_entry)
        
        # Ghi lại file
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã lưu log document: {document_name} cho customer: {customer_id}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi lưu log: {str(e)}")
        return False