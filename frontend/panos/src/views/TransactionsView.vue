<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Transactions</h2>

    <!-- Κουμπί φόρτωσης συναλλαγών -->
    <button @click="fetchTransactions" :disabled="loading">
      {{ loading ? "Loading..." : "Load Transactions" }}
    </button>

    <!-- Πίνακας συναλλαγών -->
    <table v-if="transactions.length">
      <thead>
        <tr>
          <th>Transaction ID</th>
          <th>From IBAN</th>
          <th>To IBAN</th>
          <th>Amount</th>
          <th>Currency</th>
          <th>Date</th>
          <th>Transaction Type</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in transactions" :key="t.id">
          <td>{{ t.id }}</td>
          <td>{{ t.from_iban }}</td>
          <td>{{ t.to_iban }}</td>
          <td>{{ t.amount }}</td>
          <td>{{ t.currency }}</td>
          <td>{{ t.date }}</td>
          <td>{{ t.type }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Κουμπί Back -->
    <button v-if="transactions.length" @click="goBack">⬅ Back</button>
  </section>
</template>

<script>
// Εισάγουμε τη συνάρτηση getTransactions() από το api.js
import { getTransactions } from "../api/api.js";

export default {
  name: "TransactionsView",

  data() {
    return {
      transactions: [], // Πίνακας με συναλλαγές
      loading: false    // Ένδειξη φόρτωσης
    };
  },

  methods: {
    /*
      fetchTransactions()
      -------------------
      Καλεί το Flask backend και φέρνει τη λίστα συναλλαγών του χρήστη.

      Περιλαμβάνει:
      Ενεργοποίηση φόρτωσης
      Κλήση στο api.js -> Flask endpoint /api/transactions
      Αποθήκευση αποτελεσμάτων στον πίνακα
      Ενημέρωση UI
    */
    async fetchTransactions() {
      // Ενεργοποιούμε το flag φόρτωσης
      this.loading = true;
      console.log("Fetching transactions...");

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        /*
          Η συνάρτηση getTransactions() στο api.js στέλνει:
            GET /api/transactions
          με header:
            Authorization: Bearer <token>

          Ο Flask backend αναμένεται να επιστρέψει JSON:
            {
              "success": true,
              "transactions": [
                {
                  "id": 32,
                  "from_iban": "...",
                  "to_iban": "...",
                  "amount": 100,
                  "currency": "Euro (€)",
                  "date": "2025-09-17 18:58:41",
                  "type": "DEBIT"
                },
                ...
              ]
            }
        */
        const data = await getTransactions(); // 🔹 Κλήση μέσω api.js

        // Αν η απάντηση είναι επιτυχής
        if (data.success) {
          this.transactions = data.transactions;
          console.log("Transactions loaded:", data.transactions);
        } else {
          // Αν αποτύχει (π.χ. μη έγκυρο token ή σφάλμα server)
          alert(data.message || "Failed to load transactions.");
          console.warn("Transactions fetch failed:", data);
        }
      } catch (error) {
        // Αν υπάρξει σφάλμα επικοινωνίας
        console.error("Error loading transactions:", error);
        alert("Error connecting to server.");
      } finally {
        // Απενεργοποίηση ένδειξης φόρτωσης
        this.loading = false;
      }
    },

    /*
      goBack()
      -------------------
      Επιστρέφει στην προηγούμενη σελίδα (όπως το "Back" κουμπί στο Python app).
      Αντίστοιχο με show_main_screen(info[0]) στο desktop.
    */
    goBack() {
      this.$router.push("/transfers"); // ή όπου βρίσκεται η αρχική σελίδα του χρήστη
    }
  }
};
</script>

