// src/services/firestoreService.js
import { collection, getDocs } from "firebase/firestore";
import { db } from "../firebase"; // đường dẫn tới firebase.js của bạn

export const fetchLoanTypes = async () => {
    const querySnapshot = await getDocs(collection(db, "loantypes"));
    return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
    }));
};
// ✅ Thêm hàm lấy danh sách khách hàng
export const fetchCustomers = async () => {
    const querySnapshot = await getDocs(collection(db, "customers"));
    return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
    }));
};