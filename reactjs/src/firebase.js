// Import các module cần thiết từ Firebase
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Dán đoạn cấu hình Firebase bạn đã copy ở bước 2
const firebaseConfig = {
    apiKey: "AIzaSyCi4rCNLsl3r2aysjmx2Bw3xCr9a0pP2Tw",
    authDomain: "hosovayvon-30fa1.firebaseapp.com",
    projectId: "hosovayvon-30fa1",
    storageBucket: "hosovayvon-30fa1.firebasestorage.app",
    messagingSenderId: "906779846144",
    appId: "1:906779846144:web:3922937969341255061ae5",
    measurementId: "G-V7JNCRFC1Y"
};

// Khởi tạo Firebase app
const app = initializeApp(firebaseConfig);

// Khởi tạo Firestore
const db = getFirestore(app);

// Export để dùng ở các file khác
export { db };
