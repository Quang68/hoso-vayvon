import React, { useEffect, useState } from "react";
import { generateDocument } from "../../services/documentService";
import "./MiddlePanel.css";

const MiddlePanel = ({ selectedLoanType }) => {
    const [formData, setFormData] = useState({});
    const [output, setOutput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (!selectedLoanType) return;

        const keys = Object.keys(selectedLoanType).filter(key => key.startsWith("key"));
        const initialData = {};
        keys.forEach(k => {
            const fieldName = selectedLoanType[k];
            initialData[fieldName] = "";
        });

        setFormData(initialData);
    }, [selectedLoanType]);

    const handleChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleGenerate = async () => {
        setIsLoading(true);
        setOutput("");

        try {
            const result = await generateDocument(formData);
            setOutput(result);
        } catch (err) {
            console.error("Lỗi khi gọi API:", err);
            setOutput("❌ Đã xảy ra lỗi khi tạo hồ sơ.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="middle-panel p-4">
            <h5>Nhập thông tin hồ sơ</h5>

            {!selectedLoanType && <p className="text-muted">⚠️ Vui lòng chọn một loại hồ sơ để bắt đầu.</p>}

            {selectedLoanType && (
                <>
                    {Object.entries(formData).map(([field, value]) => (
                        <div className="row mb-3 align-items-center" key={field}>
                            <label className="col-sm-4 col-form-label text-end pe-2">
                                {field}
                            </label>
                            <div className="col-sm-8">
                                <input
                                    type="text"
                                    className="form-control"
                                    value={value}
                                    onChange={(e) => handleChange(field, e.target.value)}
                                />
                            </div>
                        </div>
                    ))}


                    <button className="btn btn-success mb-3" onClick={handleGenerate}>
                        Tạo hồ sơ
                    </button>
                </>
            )}

            <h6>Kết quả:</h6>
            {isLoading && <p className="text-secondary">⏳ Vui lòng chờ, hệ thống đang soạn thảo hồ sơ...</p>}

            <pre className="bg-light p-3 rounded" style={{ whiteSpace: "pre-wrap" }}>{output}</pre>
        </div>
    );
};

export default MiddlePanel;
