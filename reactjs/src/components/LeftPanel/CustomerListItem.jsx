// src/components/LeftPanel/CustomerListItem.jsx
import React from "react";

const CustomerListItem = ({ customer, onClick }) => {
    return (
        <li
            className="list-group-item list-group-item-action"
            onClick={() => onClick?.(customer)}
            style={{ cursor: "pointer" }}
        >
            {customer.id} - {customer.name}
        </li>
    );
};

export default CustomerListItem;
