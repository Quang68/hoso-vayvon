import React, { useState } from "react";
import { generateDocument } from "../../services/documentService";
import "./MiddlePanel.css";

const MiddlePanel = () => {
    const [name, setName] = useState("");
    const [address, setAddress] = useState("");
    const [amount, setAmount] = useState("");
    const [output, setOutput] = useState("");
    const [isLoading, setIsLoading] = useState(false); // 👈 trạng thái chờ

    const handleGenerate = async () => {
        setIsLoading(true); // 👈 Bắt đầu chờ
        setOutput("");      // 👈 Xóa kết quả cũ nếu có

        try {
            const result = await generateDocument({ name, address, amount });
            setOutput(result);
        } catch (err) {
            console.error("Lỗi khi gọi API:", err);
            setOutput("❌ Đã xảy ra lỗi khi tạo hồ sơ.");
        } finally {
            setIsLoading(false); // 👈 Kết thúc chờ
        }
    };

    return (
        <div className="middle-panel p-4">
            <h5>Nhập thông tin hồ sơ</h5>
            <input className="form-control mb-2" placeholder="Tên" value={name} onChange={(e) => setName(e.target.value)} />
            <input className="form-control mb-2" placeholder="Địa chỉ" value={address} onChange={(e) => setAddress(e.target.value)} />
            <input className="form-control mb-2" placeholder="Số tiền vay" value={amount} onChange={(e) => setAmount(e.target.value)} />
            <button className="btn btn-success mb-3" onClick={handleGenerate}>
                Tạo hồ sơ
            </button>

            <h6>Kết quả:</h6>

            {/* Thông báo đang xử lý */}
            {isLoading && <p className="text-secondary">⏳ Vui lòng chờ, hệ thống đang soạn thảo hồ sơ...</p>}

            {/* Kết quả */}
            <pre className="bg-light p-3 rounded" style={{ whiteSpace: "pre-wrap" }}>{output}</pre>
        </div>
    );
};

export default MiddlePanel;
