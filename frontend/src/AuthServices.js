import { auth } from "./Firebase";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  RecaptchaVerifier,
  signInWithPhoneNumber
} from "firebase/auth";

// Email signup
export const signUp = (email, password) => {
  return createUserWithEmailAndPassword(auth, email, password);
};

// Email login
export const login = (email, password) => {
  return signInWithEmailAndPassword(auth, email, password);
};

// Google login
export const loginWithGoogle = () => {
  const provider = new GoogleAuthProvider();
  return signInWithPopup(auth, provider);
};

// Logout
export const logout = () => {
  return signOut(auth);
};

// Setup phone login
export const setupRecaptcha = (phoneNumber) => {
  window.recaptchaVerifier = new RecaptchaVerifier(
    "recaptcha-container",
    { size: "invisible" },
    auth
  );

  const appVerifier = window.recaptchaVerifier;
  return signInWithPhoneNumber(auth, phoneNumber, appVerifier);
};