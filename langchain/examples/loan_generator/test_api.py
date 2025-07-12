import requests
import json

# Test data
test_data = {
    "full_name": "Nguyễn Văn Test",
    "age": 30,
    "nationality": "Việt Nam",
    "sex": "Nam",
    "address": "123 Đường Test, Quận 1, TP.HCM",
    "phone": "0123456789",
    "email": "test@example.com",
    "loan_amount": 500000000,
    "loan_purpose": "Mua nhà",
    "monthly_income": 20000000,
    "occupation": "Kỹ sư phần mềm",
    "bank_account": "123456789",
    "collateral": "Sổ đỏ nhà đất",
    "guarantor": "Nguyễn Văn B"
}

def test_loan_application():
    """Test tạo hồ sơ vay vốn"""
    try:
        print("🧪 Testing loan application...")
        
        # Gửi request
        response = requests.post(
            "http://127.0.0.1:8000/generate-loan-document",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Tạo hồ sơ thành công!")
            print(f"📄 File ID: {result.get('file_id')}")
            print(f"🔗 Drive Link: {result.get('drive_link')}")
            print(f"📁 Local Path: {result.get('local_path')}")
            print(f"📊 Status: {result.get('status')}")
            
            # Kiểm tra các trường khác
            if result.get('backup_info'):
                print(f"💾 Backup Info: {result.get('backup_info')}")
                
        else:
            print(f"❌ Lỗi: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Lỗi khi test: {str(e)}")

if __name__ == "__main__":
    test_loan_application()
