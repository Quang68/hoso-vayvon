// src/components/LeftPanel/LoanTypeItem.jsx
import React from "react";

const LoanTypeItem = ({ type, onClick, selected }) => {
    return (
        <li
            className={`list-group-item list-group-item-action ${selected ? "active" : ""}`}
            onClick={onClick}
            style={{ cursor: "pointer" }}
        >
            📄 {type.name}
        </li>
    );
};

export default LoanTypeItem;
