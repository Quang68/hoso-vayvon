// src/components/WelcomeScreen.jsx
import React from "react";
import "./WelcomeScreen.css"; // Nhớ import file CSS

const WelcomeScreen = ({ onSelect }) => {
    return (
        <div className="welcome-container">
            <h2 className="welcome-title">Bạn là khách hàng?</h2>
            <div className="welcome-buttons">
                <button className="welcome-button" onClick={() => onSelect("new")}>
                    👤 Khách hàng mới
                </button>
                <button className="welcome-button" onClick={() => onSelect("existing")}>
                    🔁 Khách hàng cũ
                </button>
            </div>
        </div>
    );
};

export default WelcomeScreen;
