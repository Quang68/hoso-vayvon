import React, { useEffect, useState } from "react";
import { generateDocument } from "../../services/documentService";
import "./MiddlePanel.css";

const MiddlePanel = ({ selectedLoanType, selectedDocumentContent }) => {
    const [formData, setFormData] = useState({});
    const [output, setOutput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    // Khởi tạo formData dựa trên mảng key từ Firestore
    useEffect(() => {
        if (!selectedLoanType || !Array.isArray(selectedLoanType.key)) return;

        const initialData = {};
        selectedLoanType.key.forEach((item) => {
            const field = Object.keys(item)[0];   // "Customer_Name"
            initialData[field] = "";
        });

        setFormData(initialData);
    }, [selectedLoanType]);

    const handleChange = (field, value) => {
        setFormData((prev) => ({
            ...prev,
            [field]: value,
        }));
    };

    const handleGenerate = async () => {
        setIsLoading(true);
        setOutput("");
        console.log("Dữ liệu gửi đến documentService:", formData);
        try {
            const result = await generateDocument({
                system_prompt: selectedLoanType.system_prompt || "",
                prompt: selectedLoanType.prompt,
                data: {
                    logic: selectedLoanType.logic,
                    ...formData,
                },
            });
            setOutput(result);
        } catch (err) {
            console.error("Lỗi khi gọi API:", err);
            setOutput("Đã xảy ra lỗi khi tạo hồ sơ.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="middle-panel p-4">


            {!selectedDocumentContent && (
                <>
                    <h5>Nhập thông tin hồ sơ</h5>

                    {!selectedLoanType && (
                        <p className="text-muted">⚠️ Vui lòng chọn một loại hồ sơ để bắt đầu.</p>
                    )}

                    {selectedLoanType?.key && (
                        <>
                            {selectedLoanType.key.map((item, index) => {
                                const field = Object.keys(item)[0];
                                const label = item[field];
                                return (
                                    <div className="row mb-3 align-items-center" key={field}>
                                        <label className="col-sm-4 col-form-label text-end pe-2">
                                            {label}
                                        </label>
                                        <div className="col-sm-8">
                                            <input
                                                type="text"
                                                className="form-control"
                                                value={formData[field] || ""}
                                                onChange={(e) => handleChange(field, e.target.value)}
                                            />
                                        </div>
                                    </div>
                                );
                            })}

                            <button
                                className="btn btn-success mb-3"
                                onClick={handleGenerate}
                                disabled={isLoading}
                            >
                                Tạo hồ sơ
                            </button>
                        </>
                    )}

                    <h6>Kết quả:</h6>
                    {isLoading && (
                        <p className="text-secondary">
                            Vui lòng chờ, hệ thống đang soạn thảo hồ sơ...
                        </p>
                    )}

                    <pre className="bg-light p-3 rounded" style={{ whiteSpace: "pre-wrap" }}>
                        {output}
                    </pre>
                </>
            )}

            {/* Hiển thị nội dung hồ sơ đã chọn */}
            {selectedDocumentContent && (
                <>
                    <h5>📄 Nội dung hồ sơ đã chọn:</h5>
                    <pre className="bg-white border p-3 rounded" style={{ whiteSpace: "pre-wrap" }}>
                        {selectedDocumentContent}
                    </pre>
                </>
            )}

        </div>
    );
};

export default MiddlePanel;
