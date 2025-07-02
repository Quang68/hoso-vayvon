// src/components/LeftPanel/LoanTypeItem.jsx
import React from "react";

const LoanTypeItem = ({ type, onClick }) => {
    return (
        <li
            className="list-group-item list-group-item-action"
            onClick={() => onClick?.(type)}
            style={{ cursor: "pointer" }}
        >
            📄 {type.name}
        </li>
    );
};

export default LoanTypeItem;
