import React from "react";

const DocumentListItem = ({ doc, isSelected, onSelect }) => {
    return (
        <li
            className={`list-group-item ${isSelected ? "active" : ""}`}
            onClick={() => onSelect(doc.id)}
            style={{ cursor: "pointer" }}
        >
            <i className="bi bi-file-earmark-text"></i> {doc.Document_Name}
        </li>
    );
};

export default DocumentListItem;
