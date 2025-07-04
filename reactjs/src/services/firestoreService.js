// src/services/firestoreService.js
import { collection, getDocs, setDoc, doc } from "firebase/firestore";
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

// Hàm tạo mã khách hàng ngẫu nhiên
// VD: KH1234
function generateRandomCustomerId() {
    const randomNum = Math.floor(1000 + Math.random() * 9000); // VD: 1234
    return `KH${randomNum}`; // VD: KH1234
}

// Hàm tạo khách hàng mới với mã ngẫu nhiên và trường name rỗng
// Trả về đối tượng { id: "KH1234", name: "" }
export async function createNewCustomer() {
    const customerId = generateRandomCustomerId();

    // Tạo document chỉ với field name rỗng
    const newCustomer = {
        name: "", // 👈 Để trống
    };

    await setDoc(doc(db, "customers", customerId), newCustomer); // Tạo một document mới trong collection "customers" với ID là customerId

    return { id: customerId, ...newCustomer };
}

// Lấy ra từng loại hồ sơ tương ứng với khách hàng
export async function fetchCustomerDocuments(customerId) {
    const docsRef = collection(db, "customers", customerId, "customer_documents");
    const snapshot = await getDocs(docsRef);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
}