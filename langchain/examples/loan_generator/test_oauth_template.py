#!/usr/bin/env python3
"""
Script to test OAuth2 with new scope and verify template file access
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gdrive_oauth_service import get_authenticated_service

def test_oauth_template_access():
    """Test OAuth2 access to template file"""
    try:
        print("🔐 Đang authenticate với OAuth2...")
        service = get_authenticated_service()
        
        # Test basic access
        print("✅ OAuth2 authentication thành công!")
        
        # Test access to template file
        template_file_id = '1DfGBOuJphBKgSR6nFjSP3-LMgY5uFnWJ'
        
        print(f"🔍 Đang kiểm tra truy cập file template: {template_file_id}")
        
        # Get file info
        file_info = service.files().get(
            fileId=template_file_id,
            fields='id,name,mimeType,size,owners'
        ).execute()
        
        print("📄 Thông tin file template:")
        print(f"   - ID: {file_info.get('id')}")
        print(f"   - Name: {file_info.get('name')}")
        print(f"   - MimeType: {file_info.get('mimeType')}")
        print(f"   - Size: {file_info.get('size', 'N/A')} bytes")
        
        # Check owners
        owners = file_info.get('owners', [])
        if owners:
            print(f"   - Owner: {owners[0].get('displayName')} ({owners[0].get('emailAddress')})")
        
        # Test download template
        print("\n🔄 Đang test download template...")
        from services.gdrive_oauth_service import download_template_from_drive
        
        local_path = download_template_from_drive(template_file_id)
        if local_path and os.path.exists(local_path):
            print(f"✅ Download template thành công: {local_path}")
            print(f"   - File size: {os.path.getsize(local_path)} bytes")
        else:
            print("❌ Download template thất bại")
            
        # Test list files in folder
        print("\n📂 Đang test truy cập thư mục...")
        folder_id = '1XUg-J-ycI1i5SFEwgYahyrHuXHfv6dD7'
        
        results = service.files().list(
            q=f"parents in '{folder_id}'",
            fields='files(id,name,mimeType)'
        ).execute()
        
        files = results.get('files', [])
        print(f"📁 Tìm thấy {len(files)} file trong thư mục:")
        for file in files:
            print(f"   - {file.get('name')} ({file.get('id')})")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_oauth_template_access()
