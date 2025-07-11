// Import các module cần thiết từ Firebase
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Dán đoạn cấu hình Firebase bạn đã copy ở bước 2
const firebaseConfig = {
    apiKey: "AIzaSyBmpc9Sw-ctqA3SPZbP8ZgFaupdpK7n-d8",
    authDomain: "hoso-ce966.firebaseapp.com",
    projectId: "hoso-ce966",
    storageBucket: "hoso-ce966.firebasestorage.app",
    messagingSenderId: "122551702489",
    appId: "1:122551702489:web:104442723011928a237fc8",
    measurementId: "G-HKQB4PTCZ0"
};

// Khởi tạo Firebase app
const app = initializeApp(firebaseConfig);

// Khởi tạo Firestore
const db = getFirestore(app);

// Export để dùng ở các file khác
export { db };
