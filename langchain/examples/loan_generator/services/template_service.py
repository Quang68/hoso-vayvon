from docxtpl import DocxTemplate
import tempfile
import json
import os
from services.gdrive_service import download_template_from_drive

def render_docx_from_template(template_id: str, context: dict) -> str:
    print("\n📄 TEMPLATE SERVICE - CHI TIẾT RENDER:")
    print("-" * 50)
    print(f"📥 Template ID: {template_id}")
    
    # Download template
    print("⬇️ Downloading template từ Google Drive...")
    template_path = download_template_from_drive(template_id)
    print(f"✅ Template downloaded: {template_path}")
    
    # Kiểm tra file size
    file_size = os.path.getsize(template_path)
    print(f"📊 Template file size: {file_size} bytes")
    
    # Load template
    print("📂 Loading DocxTemplate...")
    doc = DocxTemplate(template_path)
    
    # Log context data sẽ được dùng để render
    print("\n🔧 CONTEXT DATA dùng để render template:")
    print("-" * 30)
    print(json.dumps(context, ensure_ascii=False, indent=2))
    print("-" * 30)
    
    # Kiểm tra các key trong context
    print(f"📋 Tổng số keys trong context: {len(context)}")
    for key, value in context.items():
        value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
        print(f"   {key}: {value_preview}")
    
    # ✨ Hiển thị template variables sẽ được thay thế
    print(f"\n🏷️ TEMPLATE VARIABLES sẽ được map:")
    for key in context.keys():
        print(f"   {{{{{key}}}}} → {context[key]}")
    
    # Render template
    print("\n🎨 Rendering template với context...")
    print(f"📋 Đang áp dụng {len(context)} variables vào template...")
    try:
        doc.render(context)  # ← ĐÂY LÀ CHỖ JSON ĐƯỢC GỬI CHO TEMPLATE
        print("✅ Template render thành công!")
        print(f"✅ Đã thay thế {len(context)} variables trong document")
    except Exception as e:
        print(f"❌ Lỗi render template: {str(e)}")
        print("🔍 Chi tiết lỗi có thể do:")
        print("   - Template variable không tồn tại trong context")
        print("   - Format variable sai trong template Word")
        print("   - Context data type không đúng")
        raise
    
    # Save rendered document
    tmp_path = tempfile.mktemp(suffix=".docx")
    doc.save(tmp_path)
    
    # Kiểm tra file output
    output_size = os.path.getsize(tmp_path)
    print(f"✅ Rendered document saved: {tmp_path}")
    print(f"📊 Output file size: {output_size} bytes")
    
    return tmp_path