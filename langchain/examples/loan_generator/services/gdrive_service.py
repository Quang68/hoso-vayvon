from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import tempfile
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
# Đường dẫn tuyệt đối đến credentials
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

TEMPLATE_FOLDER_ID = "1XUg-J-ycI1i5SFEwgYahyrHuXHfv6dD7"  # thư mục chứa template

def download_template_from_drive(file_id):
    """Download template từ Google Drive bằng file ID"""
    try:
        print(f"🔍 Đang download file với ID: {file_id}")
        
        # Lấy thông tin file trước
        file_metadata = service.files().get(fileId=file_id, fields="id,name").execute()
        file_name = file_metadata.get("name", "unknown")
        print(f"� Tên file: {file_name}")
        
        # Tạo request download
        request = service.files().get_media(fileId=file_id)
        
        # Tạo file tạm thời
        fh = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        
        # Tạo downloader đúng cách
        file_io = io.FileIO(fh.name, 'wb')
        downloader = MediaIoBaseDownload(file_io, request)
        
        # Download file
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"📥 Download progress: {int(status.progress() * 100)}%")
        
        file_io.close()
        print(f"✅ Download hoàn tất: {fh.name}")
        return fh.name
        
    except Exception as e:
        print(f"❌ Lỗi download template: {str(e)}")
        raise

def upload_file_to_drive(file_path: str, filename: str):
    """Upload file lên Google Drive"""
    try:
        # Kiểm tra file tồn tại
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File không tồn tại: {file_path}")
        
        print(f"📤 Uploading file: {filename}")
        
        # Metadata cho file
        file_metadata = {
            'name': filename, 
            'parents': [TEMPLATE_FOLDER_ID]
        }
        
        # Media upload
        media = MediaFileUpload(
            file_path, 
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            resumable=True
        )
        
        # Upload file
        uploaded_file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id,webViewLink,name'
        ).execute()
        
        file_id = uploaded_file.get("id")
        web_link = uploaded_file.get("webViewLink")
        
        print(f"✅ Upload thành công!")
        print(f"   File ID: {file_id}")
        print(f"   Link: {web_link}")
        
        return file_id, web_link
        
    except Exception as e:
        print(f"❌ Lỗi upload file: {str(e)}")
        raise

def test_connection():
    """Test kết nối với Google Drive"""
    try:
        results = service.files().list(pageSize=1).execute()
        print("✅ Kết nối Google Drive thành công!")
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối Google Drive: {str(e)}")
        return False

def list_files_in_folder():
    """List tất cả files trong template folder"""
    try:
        results = service.files().list(
            q=f"'{TEMPLATE_FOLDER_ID}' in parents",
            fields="files(id, name, mimeType, size)"
        ).execute()
        
        items = results.get("files", [])
        print(f"📁 Files trong folder (Total: {len(items)}):")
        
        for item in items:
            print(f"   - {item['name']} (ID: {item['id']})")
            
        return items
        
    except Exception as e:
        print(f"❌ Lỗi list files: {str(e)}")
        return []

def delete_file_from_drive(file_id: str):
    """Xóa file từ Google Drive"""
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"✅ Đã xóa file: {file_id}")
        return True
    except Exception as e:
        print(f"❌ Lỗi xóa file: {str(e)}")
        return False

# Function để test
if __name__ == "__main__":
    print("🧪 Testing Google Drive Service...")
    
    # Test kết nối
    if test_connection():
        # List files
        list_files_in_folder()
        
        # Test download với file ID thực tế
        try:
            # Thử download với file ID có sẵn từ React
            test_file_id = "1DfGBOuJphBKgSR6nFjSP3-LMgY5uFnWJ"
            template_path = download_template_from_drive(test_file_id)
            print(f"📄 Template downloaded to: {template_path}")
            
            # Cleanup
            os.unlink(template_path)
            print("🗑️ Cleaned up temp file")
            
        except Exception as e:
            print(f"⚠️ Không thể test download: {str(e)}")
            
    else:
        print("❌ Không thể kết nối với Google Drive")