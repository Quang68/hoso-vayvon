// src/components/LeftPanel/CustomerListItem.jsx
import React from "react";

const CustomerListItem = ({ customer, onClick, selected }) => {
    return (
        <li
            className={`list-group-item list-group-item-action ${selected ? "active" : ""}`}
            onClick={onClick}
            style={{ cursor: "pointer" }}
        >
            {customer.id} - {customer.name}
        </li>
    );
};


export default CustomerListItem;
