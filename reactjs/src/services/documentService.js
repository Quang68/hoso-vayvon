export async function generateDocument(payload) {
    console.log("📦 Gửi lên API:", JSON.stringify(payload));

    const response = await fetch("http://127.0.0.1:8000/generate-document", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errText = await response.text();
        console.error("Server trả về lỗi:", response.status, errText);
        throw new Error("Không tạo được hồ sơ");
    }

    const json = await response.json();
    return json.document;
}
