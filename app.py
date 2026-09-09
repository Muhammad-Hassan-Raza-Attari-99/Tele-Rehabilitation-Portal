import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "coffee-spark-ai-barista-c2c81.firebaseapp.com",
  projectId: "coffee-spark-ai-barista-c2c81",
  storageBucket: "coffee-spark-ai-barista-c2c81.firebasestorage.app",
  messagingSenderId: "306480378237",
  appId: "telerehabilitation-portal"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Services
export const auth = getAuth(app);
export const db = getFirestore(app);
