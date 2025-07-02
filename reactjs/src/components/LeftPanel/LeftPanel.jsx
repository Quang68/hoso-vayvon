// src/components/LeftPanel/LeftPanel.jsx
import React, { useEffect, useState } from "react";
import "./LeftPanel.css";
import { fetchLoanTypes, fetchCustomers } from "../../services/firestoreService";
import LoanTypeItem from "./LoanTypeItem";
import CustomerListItem from "./CustomerListItem";

const LeftPanel = ({ onCreateNewCustomer }) => {
    const [loanTypes, setLoanTypes] = useState([]);
    const [customers, setCustomers] = useState([]);

    useEffect(() => {
        const getData = async () => {
            try {
                const types = await fetchLoanTypes();
                const customersData = await fetchCustomers();
                console.log("✅ Loại hồ sơ:", types);
                console.log("✅ Danh sách khách hàng:", customersData);
                setLoanTypes(types);
                setCustomers(customersData);
            } catch (error) {
                console.error("❌ Lỗi khi lấy dữ liệu:", error);
            }
        };

        getData();
    }, []);

    return (
        <div className="left-panel p-3 border-end">
            {/* Khu vực loại hồ sơ */}
            <div className="mb-4">
                <h5><i className="bi bi-folder"></i> Loại hồ sơ</h5>
                <ul className="list-group">
                    {loanTypes.map((type) => (
                        <LoanTypeItem key={type.id} type={type} />
                    ))}
                </ul>
            </div>

            <hr />

            {/* Khu vực khách hàng */}
            <div>
                <h5><i className="bi bi-person-fill"></i> Khách hàng</h5>

                {/* Nút khách hàng mới ở đầu */}
                <button className="btn btn-primary w-100 mb-3" onClick={onCreateNewCustomer}>
                    <i className="bi bi-person-fill-add"></i> Khách hàng mới
                </button>

                {/* Thanh tìm kiếm khách hàng */}
                <input
                    type="text"
                    className="form-control mb-3"
                    placeholder="🔍 Tìm theo tên hoặc mã KH..."
                />

                {/* Danh sách khách hàng */}
                <ul className="list-group">
                    {customers.map((customer) => (
                        <CustomerListItem key={customer.id} customer={customer} />
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default LeftPanel;
