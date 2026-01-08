// src/api/api.js
// ===================================================
// ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask API)
// Όλες οι κλήσεις API θα βρίσκονται εδώ συγκεντρωμένες
// ===================================================

// Ορίζουμε τη βάση του API URL (θα αλλάξει όταν το backend ανέβει σε server)
const API_BASE_URL = "http://127.0.0.1:5000";

// ---------------------------------------------------
//  AUTHENTICATION ENDPOINTS
// ---------------------------------------------------

// Home Screen δεδομενα 
export async function getAccount() {
  try {
    const response = await fetch(`${API_BASE_URL}/home`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
    });
    const data = await response.json();
    console.log("Account data fetched:", data);
    return data; // Επιστρέφει balance, iban, card_number
  } catch (error) {
    console.error("Error fetching account info:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

// Σύνδεση χρήστη (Sign In)
export async function login(email, password) {
  try {
    //`${API_BASE_URL}/login` συνδυάζει τη βάση URL του backend (π.χ. `http://127.0.0.1:5000`) με το endpoint `/login`.
    const response = await fetch(`${API_BASE_URL}/login`, {
      //(POST) Αυτό σημαίνει ότι στέλνουμε δεδομένα (το email και password) στο σώμα (body) του request.
      method: "POST",
      //(JSON) Ενημερώνουμε τον server ότι τα δεδομένα που στέλνουμε είναι σε μορφή JSON.
      headers: { "Content-Type": "application/json" },
      //Ορισμός, δεδομένων στο backend και μετατροπή τους σε JSON string.
      body: JSON.stringify({ email, password, success: true })
    });
    const data = await response.json();
    return data; // Επιστρέφουμε την απάντηση στο Vue component
  } catch (error) {
    console.error("Login error:", error);
    return { success: false, message: "Error connecting to server." };
  }
}

// Εγγραφή νέου χρήστη (Sign Up)
export async function register(email, password, ver_password) {
  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, ver_password })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.log("Register error:", error);
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
export async function transfers(recipient, amount, currency) {
  const response = await fetch(`${API_BASE_URL}/transfers`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({ recipient, amount, currency })
  });
  return await response.json();
}

export async function transfer_data() {
  try {
    const response = await fetch(`${API_BASE_URL}/transfers`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
    });
    const data = await response.json();
    console.log("Account data fetched:", data);
    return data; // Επιστρέφει balance, iban, card_number
  } catch (error) {
    console.error("Error fetching account info:", error);
    return { success: false, message: "Error connecting to server." };
  }
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

// Πληροφορίες κάρτας
export async function getCard() {
  const response = await fetch(`${API_BASE_URL}/card`, {
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  });
  return await response.json();
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
