"""
Backup service khi Google Drive upload bị lỗi
Trả về mock data để frontend vẫn hoạt động được
"""

import tempfile
import os
from datetime import datetime

def backup_save_file(file_path: str, filename: str):
    """Backup: Lưu file local và trả về mock data"""
    try:
        # Tạo thư mục backup
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backup_files')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy file vào backup folder
        backup_path = os.path.join(backup_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        
        # Copy file
        import shutil
        shutil.copy2(file_path, backup_path)
        
        print(f"📁 File được lưu backup tại: {backup_path}")
        
        # Trả về mock data giống Google Drive
        mock_file_id = f"mock_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        mock_web_link = f"file://{backup_path}"
        
        print(f"✅ Backup thành công!")
        print(f"   Mock File ID: {mock_file_id}")
        print(f"   Local Path: {backup_path}")
        
        return mock_file_id, mock_web_link
        
    except Exception as e:
        print(f"❌ Lỗi backup file: {str(e)}")
        raise