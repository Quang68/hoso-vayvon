from services.gdrive_service import upload_file_to_drive
from services.firestore_service import save_document_content
from services.backup_service import backup_save_file

def upload_to_drive(docx_path, filename):
    """Upload file lên Google Drive với fallback"""
    try:
        # Thử upload Google Drive trước
        return upload_file_to_drive(docx_path, filename)
    except Exception as e:
        print(f"⚠️ Google Drive upload thất bại: {str(e)}")
        print("🔄 Chuyển sang backup mode...")
        
        # Fallback: Lưu file local
        return backup_save_file(docx_path, filename)

def save_to_firestore(customer_id, document_name, document_type_id, content):
    return save_document_content(customer_id, document_name, document_type_id, content)