// src/components/RightPanel.jsx
import React from "react";
import "./RightPanel.css";

const RightPanel = ({ selectedCustomer }) => {
    return (
        <div className="right-panel">
            <h3>📄 Hồ sơ của khách hàng</h3>
            {selectedCustomer ? (
                <ul>
                    <li>Hồ sơ vay tiêu dùng - 01/07/2025</li>
                    <li>Hồ sơ vay mua tài sản - 30/06/2025</li>
                </ul>
            ) : (
                <p>⚠️ Chưa chọn khách hàng nào.</p>
            )}
        </div>
    );
};

export default RightPanel;
