import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendPasswordResetEmail, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyB0srpcLeNF8nR6DF_fP7_FsemKY4--4wU",
  authDomain: "nexulen-f8790.firebaseapp.com",
  projectId: "nexulen-f8790",
  storageBucket: "nexulen-f8790.firebasestorage.app",
  messagingSenderId: "718749886008",
  appId: "1:718749886008:web:df0563c31aaff0c2e628cd"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const loginButton = document.getElementById('login-button');
const logoutButton = document.getElementById('logout-button');
const userProfile = document.getElementById('user-profile');
const loginArea = document.getElementById('login-area');
const userDisplayName = document.getElementById('user-display-name');

// Modal elements
const loginModal = document.getElementById('login-modal');
const signupModal = document.getElementById('signup-modal');
const forgotPasswordModal = document.getElementById('forgot-password-modal');

// Close buttons
const loginCloseButton = document.getElementById('login-close');
const signupCloseButton = document.getElementById('signup-close');
const forgotPasswordCloseButton = document.getElementById('forgot-password-close');

// Form elements
const loginEmailInput = document.getElementById('login-email');
const loginPasswordInput = document.getElementById('login-password');
const loginSubmitButton = document.getElementById('login-submit');
const loginError = document.getElementById('login-error');

const signupEmailInput = document.getElementById('signup-email');
const signupPasswordInput = document.getElementById('signup-password');
const signupSubmitButton = document.getElementById('signup-submit');
const signupError = document.getElementById('signup-error');

const forgotPasswordEmailInput = document.getElementById('forgot-password-email');
const forgotPasswordSubmitButton = document.getElementById('forgot-password-submit');
const forgotPasswordError = document.getElementById('forgot-password-error');

// Links
const forgotPasswordLink = document.getElementById('forgot-password-link');
const signupLink = document.getElementById('signup-link');
const loginLinkFromSignup = document.getElementById('login-link-from-signup');

// Event listeners for modal actions
loginButton.addEventListener('click', () => {
    loginModal.style.display = 'block';
});

loginCloseButton.addEventListener('click', () => {
    loginModal.style.display = 'none';
    loginError.style.display = 'none';
});

signupLink.addEventListener('click', () => {
    loginModal.style.display = 'none';
    signupModal.style.display = 'block';
    loginError.style.display = 'none';
});

signupCloseButton.addEventListener('click', () => {
    signupModal.style.display = 'none';
    signupError.style.display = 'none';
});

loginLinkFromSignup.addEventListener('click', () => {
    signupModal.style.display = 'none';
    loginModal.style.display = 'block';
    signupError.style.display = 'none';
});

forgotPasswordLink.addEventListener('click', () => {
    loginModal.style.display = 'none';
    forgotPasswordModal.style.display = 'block';
    loginError.style.display = 'none';
});

forgotPasswordCloseButton.addEventListener('click', () => {
    forgotPasswordModal.style.display = 'none';
    forgotPasswordError.style.display = 'none';
});

// Login submit
loginSubmitButton.addEventListener('click', () => {
    const email = loginEmailInput.value;
    const password = loginPasswordInput.value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            loginModal.style.display = 'none';
            loginError.style.display = 'none';
        })
        .catch((error) => {
            console.error("Error during login:", error);
            loginError.style.display = 'block';
            if (error.code === 'auth/wrong-password') {
                loginError.textContent = 'Incorrect password. Please try again.';
            } else if (error.code === 'auth/user-not-found') {
                 loginError.textContent = 'User not found. Please check your email.';
            } else {
                loginError.textContent = 'Login failed. Please check your credentials.';
            }
        });
});

// Signup submit
signupSubmitButton.addEventListener('click', () => {
    const email = signupEmailInput.value;
    const password = signupPasswordInput.value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            signupModal.style.display = 'none';
            signupError.style.display = 'none';
        })
        .catch((error) => {
            console.error("Error during signup:", error);
            signupError.style.display = 'block';
             if (error.code === 'auth/email-already-in-use') {
                signupError.textContent = 'Email already in use. Please use a different email.';
            } else {
                signupError.textContent = 'Signup failed. Please try again.';
            }
        });
});

// Forgot password submit
forgotPasswordSubmitButton.addEventListener('click', () => {
    const email = forgotPasswordEmailInput.value;

    sendPasswordResetEmail(auth, email)
        .then(() => {
            forgotPasswordModal.style.display = 'none';
            forgotPasswordError.style.display = 'none';
            alert("Password reset email sent. Please check your inbox.");
        })
        .catch((error) => {
            console.error("Error during password reset:", error);
            forgotPasswordError.style.display = 'block';
             if (error.code === 'auth/user-not-found') {
                forgotPasswordError.textContent = 'User not found. Please check your email.';
            } else {
                 forgotPasswordError.textContent = 'Failed to send password reset email. Please try again.';
            }
        });
});

logoutButton.addEventListener('click', () => {
    signOut(auth).then(() => {
        // Sign-out successful.
    }).catch((error) => {
        console.error("Error during logout:", error);
    });
});

onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in, show profile and hide login button
        userDisplayName.textContent = user.displayName || user.email;
        userProfile.style.display = 'flex';
        loginArea.style.display = 'none';
    } else {
        // User is signed out, show login button and hide profile
        userProfile.style.display = 'none';
        loginArea.style.display = 'block';
    }
});
