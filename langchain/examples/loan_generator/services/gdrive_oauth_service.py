from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import tempfile
import io
import json

# Scopes cần thiết - sử dụng drive scope để truy cập tất cả file
SCOPES = ['https://www.googleapis.com/auth/drive']

# Đường dẫn tới OAuth2 credentials
OAUTH_CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'oauth_credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token.json')

TEMPLATE_FOLDER_ID = "1XUg-J-ycI1i5SFEwgYahyrHuXHfv6dD7"

def get_authenticated_service():
    """Lấy service đã authenticated với OAuth2"""
    creds = None
    
    # Kiểm tra token đã lưu
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Nếu không có credentials hợp lệ, authenticate lại
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Đang refresh token...")
            creds.refresh(Request())
        else:
            print("🔐 Cần authenticate lại với Google...")
            if not os.path.exists(OAUTH_CREDENTIALS_FILE):
                raise FileNotFoundError(f"Không tìm thấy file OAuth credentials: {OAUTH_CREDENTIALS_FILE}")
            
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Lưu credentials để dùng lần sau
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def download_template_from_drive(file_id):
    """Download template từ Google Drive bằng OAuth2"""
    try:
        print(f"🔍 Đang download file với ID: {file_id}")
        
        service = get_authenticated_service()
        
        # Lấy thông tin file
        file_metadata = service.files().get(fileId=file_id, fields="id,name").execute()
        file_name = file_metadata.get("name", "unknown")
        print(f"📄 Tên file: {file_name}")
        
        # Tạo request download
        request = service.files().get_media(fileId=file_id)
        
        # Tạo file tạm thời
        fh = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        
        # Download file
        file_io = io.FileIO(fh.name, 'wb')
        downloader = MediaIoBaseDownload(file_io, request)
        
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
    """Upload file lên Google Drive bằng OAuth2"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File không tồn tại: {file_path}")
        
        print(f"📤 Uploading file: {filename}")
        
        service = get_authenticated_service()
        
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

def test_oauth_connection():
    """Test kết nối OAuth2"""
    try:
        service = get_authenticated_service()
        results = service.files().list(pageSize=1).execute()
        print("✅ Kết nối OAuth2 thành công!")
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối OAuth2: {str(e)}")
        return False

def list_files_in_folder():
    """List files trong folder"""
    try:
        service = get_authenticated_service()
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