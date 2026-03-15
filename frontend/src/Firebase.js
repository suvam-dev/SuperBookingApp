// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCb6yoqJLHL3scxEpZ3Wn9yOgO7oeEPQ54",
  authDomain: "start-up-fbbcc.firebaseapp.com",
  projectId: "start-up-fbbcc",
  storageBucket: "start-up-fbbcc.firebasestorage.app",
  messagingSenderId: "6994123335",
  appId: "1:6994123335:web:bb360921da019497ddaf62"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);