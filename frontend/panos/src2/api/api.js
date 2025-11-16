// src/api/api.js
// ===================================================
// ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask API)
// Όλες οι κλήσεις API θα βρίσκονται εδώ συγκεντρωμένες
// ===================================================

// Ορίζουμε τη βάση του API URL (θα αλλάξει όταν το backend ανέβει σε server)
const API_BASE_URL = "http://127.0.0.1:5000/api";

// ---------------------------------------------------
//  AUTHENTICATION ENDPOINTS
// ---------------------------------------------------

// Home Screen δεδομενα 
export async function getAccount() {
  try {
    const response = await fetch(`${API_BASE_URL}/account`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
    });
    const data = await response.json();
    return data; // Επιστρέφει balance, iban, card_number
  } catch (error) {
    console.error("Error fetching account info:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

// Σύνδεση χρήστη (Sign In)
export async function login(email, password) {
  try {
    //`${API_BASE_URL}/login` συνδυάζει τη βάση URL του backend (π.χ. `http://127.0.0.1:5000/api`) με το endpoint `/login`.
    const response = await fetch(`${API_BASE_URL}/login`, {
      //(POST) Αυτό σημαίνει ότι στέλνουμε δεδομένα (το email και password) στο σώμα (body) του request.
      method: "POST",
      //(JSON) Ενημερώνουμε τον server ότι τα δεδομένα που στέλνουμε είναι σε μορφή JSON.
      headers: { "Content-Type": "application/json" },
      //Ορισμός, δεδομένων στο backend και μετατροπή τους σε JSON string.
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    return data; // Επιστρέφουμε την απάντηση στο Vue component
  } catch (error) {
    console.error("Login error:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

// Εγγραφή νέου χρήστη (Sign Up)
export async function register(name, email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Register error:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

// Αποσύνδεση (Logout)
export async function logout() {
  try {
    const response = await fetch(`${API_BASE_URL}/logout`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Logout error:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

// -------------- BANKING FEATURES -----------------

// Μεταφορά χρημάτων
export async function transfer(recipient, amount) {
  const response = await fetch(`${API_BASE_URL}/transfer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({ recipient, amount })
  });
  return await response.json();
}

// Ανταλλαγή νομισμάτων
export async function exchange(amount, from, to) {
  const response = await fetch(`${API_BASE_URL}/exchange`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({ amount, currency_from: from, currency_to: to })
  });
  return await response.json();
}

// =======================
//   CARD API FUNCTIONS
// =======================

// Παίρνουμε τα στοιχεία της κάρτας του χρήστη
export async function getCard() {
  try {
    const response = await fetch(`${API_BASE_URL}/card`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
    });

    const data = await response.json();
    return data;        // Περιμένουμε { success: true, card: {...} }
  } catch (error) {
    console.error("Get card error:", error);
    return { success: false };
  }
}

// Αλλάζουμε κατάσταση κάρτας: freeze ή unfreeze
export async function toggleCardFreeze(freeze) {
  try {
    const endpoint = freeze ? "freeze_card" : "unfreeze_card";

    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
      // δεν χρειάζεται body, ο server βρίσκει την κάρτα από το token
    });

    const data = await response.json();
    return data;        // Περιμένουμε { success: true } ή { success: false }
  } catch (error) {
    console.error("Toggle card freeze error:", error);
    return { success: false };
  }
}


// Freeze / Unfreeze κάρτας
export async function toggleCardFreeze(freeze) {
  const endpoint = freeze ? "freeze_card" : "unfreeze_card";
  const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  });
  return await response.json();
}

// Συναλλαγές
export async function getTransactions() {
  const response = await fetch(`${API_BASE_URL}/transactions`, {
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  });
  return await response.json();
}

//Change Password
export async function changePassword(old_password, new_password) {
  try {
    const response = await fetch(`${API_BASE_URL}/change_password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ old_password, new_password })
    });

    return await response.json();
  } catch (error) {
    console.error("Password change error:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

//Change PIN
export async function changePin(old_pin, new_pin) {
  try {
    const response = await fetch(`${API_BASE_URL}/change_pin`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ old_pin, new_pin })
    });

    return await response.json();
  } catch (error) {
    console.error("PIN change error:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

//Change Email
// Ζητάμε αλλαγή email (παράγει OTP και το στέλνει)
export async function requestEmailChange(old_email, new_email) {
  try {
    const response = await fetch(`${API_BASE_URL}/request_email_change`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ old_email, new_email })
    });

    return await response.json();
  } catch (error) {
    console.error("Request email change error:", error);
    return { success: false };
  }
}

// Επαληθεύουμε το OTP
export async function verifyEmailOTP(otp) {
  try {
    const response = await fetch(`${API_BASE_URL}/verify_email_otp`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ otp })
    });

    return await response.json();
  } catch (error) {
    console.error("Verify OTP error:", error);
    return { success: false };
  }
}

