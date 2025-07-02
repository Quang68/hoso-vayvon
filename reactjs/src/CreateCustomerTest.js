// src/CreateCustomerTest.js
import React from "react";
import { db } from "./firebase";
import { doc, setDoc } from "firebase/firestore";

const CreateCustomerTest = () => {
    const handleCreateCustomer = async () => {
        try {
            await setDoc(doc(db, "customers", "KH00123"), {
                name: "Nguyễn Văn A",
                createdAt: new Date(),
                profiles: [],
            });
            alert("Tạo khách hàng thành công!");
        } catch (error) {
            console.error("Lỗi tạo khách hàng:", error);
            alert("Thất bại khi tạo khách hàng!");
        }
    };

    return (
        <div>
            <h2>Test kết nối Firebase</h2>
            <button onClick={handleCreateCustomer}>Tạo khách hàng KH00123</button>
        </div>
    );
};

export default CreateCustomerTest;
