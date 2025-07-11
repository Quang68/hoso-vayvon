from langchain_together import Together
import os
import json
from dotenv import load_dotenv

load_dotenv()

llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    temperature=0.0,
    max_tokens=1024,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

def run_llm(system_prompt, prompt, user_data):
    print("\n🤖 LLM SERVICE - CHI TIẾT XỬ LÝ:")
    print("-" * 50)
    
    # Tạo full prompt
    print("📝 Tạo prompt cho LLM...")
    print("1. System prompt:", system_prompt[:100] + "..." if len(system_prompt) > 100 else system_prompt)
    print("2. User prompt:", prompt[:100] + "..." if len(prompt) > 100 else prompt)
    print("3. User data:", json.dumps(user_data, ensure_ascii=False, indent=2))
    
    # Thay thế variables trong prompt
    combined_prompt = f"{system_prompt}\n\n{prompt}"
    
    # Thay thế {key} bằng value từ user_data
    for key, value in user_data.items():
        placeholder = f"{{{key}}}"
        combined_prompt = combined_prompt.replace(placeholder, str(value))
        print(f"   Thay thế {{{key}}} → {value}")
    
    print("\n📨 FINAL PROMPT gửi cho LLM:")
    print("-" * 30)
    print(combined_prompt)
    print("-" * 30)
    
    # Gọi LLM
    print("\n⏳ Đang gọi LLM...")
    response = llm.invoke(combined_prompt)
    print(f"✅ LLM response length: {len(response)} characters")
    
    print("\n🎯 LLM RESPONSE:")
    print("-" * 30)
    print(response)
    print("-" * 30)
    
    # ✨ Xử lý response để extract giá trị định giá
    processed_data = process_llm_response(response, user_data)
    
    print("\n✨ PROCESSED RESULT (sau khi extract values):")
    print("-" * 30)
    print(json.dumps(processed_data, ensure_ascii=False, indent=2))
    print("-" * 30)
    
    return processed_data

def process_llm_response(llm_response: str, original_data: dict) -> dict:
    """Xử lý response từ LLM để extract các giá trị cần thiết"""
    
    # Bắt đầu với data gốc
    result = {
        "output": llm_response,
        **original_data,
        "processed_prompt": llm_response,
        "llm_model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
    }
    
    # ✨ Extract giá trị định giá từ response
    valuation = extract_valuation(llm_response)
    if valuation:
        result["Valuation"] = valuation
        print(f"💰 Extracted Valuation: {valuation:,} VND")
    
    # ✨ Extract các thông tin khác nếu cần
    result.update(extract_other_values(llm_response))
    
    return result

def extract_valuation(text: str) -> int:
    """Extract giá trị định giá từ text"""
    import re
    
    patterns = [
        r"[Vv]aluation[:\s]*(\d+(?:,\d{3})*)",           # "Valuation: 150,000,000"
        r"[Đđ]ịnh giá[:\s]*(\d+(?:,\d{3})*)",           # "Định giá: 150,000,000"  
        r"[Gg]iá trị[:\s]*(\d+(?:,\d{3})*)",            # "Giá trị: 150,000,000"
        r"[Tt]ài sản.*?(\d+(?:,\d{3})*)\s*VND",         # "Tài sản được định giá: 150,000,000 VND"
        r"(\d+(?:,\d{3})*)\s*VND",                       # "150,000,000 VND"
        r"(\d+(?:\.\d{3})*)\s*triệu",                    # "150.000 triệu"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Lấy số và convert thành int
            number_str = match.group(1).replace(",", "").replace(".", "")
            try:
                value = int(number_str)
                # Nếu đơn vị là triệu thì nhân với 1,000,000
                if "triệu" in pattern:
                    value *= 1000000
                return value
            except ValueError:
                continue
    
    return None

def extract_other_values(text: str) -> dict:
    """Extract các giá trị khác từ response"""
    import re
    result = {}
    
    # Extract diện tích
    area_pattern = r"[Dd]iện tích[:\s]*(\d+(?:,\d{3})*)"
    area_match = re.search(area_pattern, text)
    if area_match:
        try:
            result["DienTich"] = int(area_match.group(1).replace(",", ""))
        except ValueError:
            pass
    
    # Extract giá thị trường
    market_pattern = r"[Gg]iá thị trường[:\s]*(\d+(?:,\d{3})*)"
    market_match = re.search(market_pattern, text)
    if market_match:
        try:
            result["GiaThiTruong"] = int(market_match.group(1).replace(",", ""))
        except ValueError:
            pass
    
    return result