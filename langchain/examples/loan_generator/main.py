from langsmith import traceable
import os
import re
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_together import Together
from langgraph.graph import StateGraph, END

# Tải biến môi trường
load_dotenv()

# ✅ Dùng Together AI với model miễn phí
llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    temperature=0.0,
    max_tokens=1024,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

# Load prompt từ file

with open("prompt_template.txt", "r", encoding="utf-8") as f:
    template_text = f.read()

template = PromptTemplate.from_template(template_text)
@traceable
def ask_name(state):
    state["name"] = input("Nhập tên khách hàng: ")
    return state
@traceable
def ask_address(state):
    state["address"] = input("Nhập địa chỉ khách hàng: ")
    return state
@traceable
def ask_amount(state):
    state["amount"] = input("Nhập số tiền vay (triệu): ")
    return state



# Bước 4: Sinh hồ sơ và lưu vào file
@traceable
def generate_doc(state):
    print("🔍 DEBUG - Dữ liệu nhận được:", state)  # 👈 THÊM DÒNG NÀY

    # Kiểm tra nếu thiếu key nào thì thông báo lỗi
    missing_keys = [key for key in ["name", "address", "amount"] if key not in state]
    if missing_keys:
        print(f"❌ Thiếu dữ liệu: {missing_keys}. Có thể các bước trước không trả đúng dict.")
        return {}

    # Nếu đầy đủ thì tiếp tục
    filled_prompt = template.format(
        name=state["name"],
        address=state["address"],
        amount=state["amount"]
    )
    print("📨 Prompt gửi tới Together:\n", filled_prompt)


    result = llm.invoke(filled_prompt)
    # Nếu model trả về object kiểu ChatResult, lấy content
    if hasattr(result, 'content'):
        result = result.content

    # Lọc bỏ phần <think>
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL)
    result = re.sub(r"</?think>", "", result)
    result = re.sub(r"<?think>", "", result)
    print("\n📄 Hồ sơ tạo được:\n")
    print(result)

    with open("ho_so_cho_vay.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print("\n✅ Đã lưu file: ho_so_cho_vay.txt")
    return {}


# Xây dựng luồng LangGraph
workflow = StateGraph(dict)
workflow.add_node("ask_name", ask_name)
workflow.add_node("ask_address", ask_address)
workflow.add_node("ask_amount", ask_amount)
workflow.add_node("generate_doc", generate_doc)

workflow.set_entry_point("ask_name")
workflow.add_edge("ask_name", "ask_address")
workflow.add_edge("ask_address", "ask_amount")
workflow.add_edge("ask_amount", "generate_doc")
workflow.add_edge("generate_doc", END)

# Biên dịch và chạy
app = workflow.compile()
app.invoke({})
