// RightPanel.jsx
import React, { useEffect, useState } from "react";
import "./RightPanel.css";
import { fetchCustomerDocuments } from "../../services/firestoreService";
import DocumentListItem from "./DocumentListItem";

const RightPanel = ({ selectedCustomer }) => {
    const [documents, setDocuments] = useState([]);
    const [selectedDocumentId, setSelectedDocumentId] = useState(null);

    const handleSelectDocument = (docId) => {
        setSelectedDocumentId(docId);
    };

    useEffect(() => {
        const loadDocuments = async () => {
            if (selectedCustomer?.id) {
                const result = await fetchCustomerDocuments(selectedCustomer.id);
                setDocuments(result);
            } else {
                setDocuments([]);
            }
        };
        loadDocuments();
    }, [selectedCustomer]);

    return (
        <div className="right-panel">
            <h3>📄 Hồ sơ của khách hàng</h3>
            {selectedCustomer ? (
                documents.length > 0 ? (
                    <ul className="list-group">
                        {documents.map((doc) => (
                            <DocumentListItem
                                key={doc.id}
                                doc={doc}
                                isSelected={selectedDocumentId === doc.id}
                                onSelect={handleSelectDocument}
                            />
                        ))}
                    </ul>
                ) : (
                    <p>⚠️ Khách hàng chưa có hồ sơ nào.</p>
                )
            ) : (
                <p>⚠️ Chưa chọn khách hàng nào.</p>
            )}
        </div>
    );
};

export default RightPanel;