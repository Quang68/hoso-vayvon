from services.gdrive_service import upload_file_to_drive
from services.firestore_service import save_document_content

def upload_to_drive(docx_path, filename):
    return upload_file_to_drive(docx_path, filename)

def save_to_firestore(customer_id, document_name, document_type_id, content):
    return save_document_content(customer_id, document_name, document_type_id, content)