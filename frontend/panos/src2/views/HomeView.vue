<template>
  <!-- Λογικά εδώ θα μπει ο κώδικας του Λάμπρου -->
  <section>
    <h2>BANK OF UNIVERSITY OF WEST ATTICA e-Banking</h2>

    <!-- Mock στοιχεία λογαριασμού -->
    <div>
      <p><strong>Balance:</strong> {{ balance }} €</p>
      <p><strong>IBAN:</strong> {{ iban }}</p>
      <p><strong>Card Number:</strong> {{ maskedCard }}</p>
    </div>

    <!-- Κουμπιά πλοήγησης (router-links) -->
    <p>
      <router-link to="/signin">Sign In</router-link> |
      <router-link to="/signup">Sign Up</router-link> |
      <router-link to="/transfers">Transfers</router-link> |
      <router-link to="/transactions">Transactions</router-link> |
      <router-link to="/currency">Currency Exchange</router-link> |
      <router-link to="/card">Card</router-link> |
      <router-link to="/graphs">Graphs</router-link> |
      <router-link to="/settings">Settings</router-link> |
      <router-link to="/logout">Log Out</router-link>
    </p>
  </section>
</template>

<script>
// Εισάγουμε τη συνάρτηση getAccount() από το api.js
import { getAccount } from "../api/api.js";

export default {
  name: "HomeView",

  data() {
    return {
      balance: null,        // Υπόλοιπο χρήστη
      iban: "",             // IBAN λογαριασμού
      cardNumber: "",       // Κάρτα χρήστη (masked)
      accountLoaded: false, // Flag για το αν έχουν φορτωθεί τα στοιχεία  
    };
  },

  async mounted() {
    /*
      ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
      Μόλις "φορτωθεί" η σελίδα (mounted),
      καλούμε τη συνάρτηση getAccount() από το api.js
      για να φέρει τα στοιχεία λογαριασμού του χρήστη.
    */
    this.loading = true;
    try {
      const data = await getAccount();

      if (data.success) {
        this.balance = data.balance;
        this.iban = data.iban;
        this.cardNumber = data.card_number;
        this.accountLoaded = true;
        console.log("Account info loaded successfully:", data);
      } else {
        alert(data.message || "Failed to load account information.");
      }
    } catch (error) {
      console.error("Error loading account info:", error);
      alert("Error connecting to server.");
    } finally {
      this.loading = false;
    }
  }
};
</script>
