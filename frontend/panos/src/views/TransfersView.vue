<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Transfers</h2>

    <!-- Φόρμα μεταφοράς χρημάτων -->
    <form @submit.prevent="makeTransfer">
      <input
        type="text"
        v-model="recipientIban"
        placeholder="Recipient IBAN"
        required
      />
      <input
        type="number"
        v-model="amount"
        placeholder="Amount (€)"
        min="1"
        step="0.01"
        required
      />
      <button type="submit" :disabled="loading">
        {{ loading ? "Processing..." : "Send Money" }}
      </button>
    </form>
  </section>
</template>

<script>
// Εισάγουμε τη συνάρτηση transfer() από το api.js
import { transfer } from "../api/api.js";

export default {
  name: "TransfersView",

  data() {
    return {
      recipientIban: "",  // IBAN του παραλήπτη
      amount: "",         // Ποσό μεταφοράς
      userBalance: 1000,  // Mock balance (θα αντικατασταθεί με δεδομένα Flask)
      loading: false      // Flag για φόρτωση
    };
  },

  methods: {
    /*
      makeTransfer()
      -----------------
      Η κύρια συνάρτηση μεταφοράς χρημάτων.
      Είναι το αντίστοιχο του transfer(info, iban_to, value) στο Python desktop app.

      Περιλαμβάνει:
      Έλεγχο εισαγόμενων δεδομένων (IBAN & ποσό)
      Έλεγχο υπολοίπου χρήστη
      Κλήση στο Flask backend μέσω api.js
      Επεξεργασία απάντησης (επιτυχία ή αποτυχία)
      Ενημέρωση UI
    */
    async makeTransfer() {
      // Έλεγχος πεδίων
      if (!this.recipientIban || !this.amount) {
        alert("Please fill in all fields.");
        return;
      }

      const money = parseFloat(this.amount);

      // Έλεγχος ότι το ποσό είναι θετικό
      if (money <= 0) {
        alert("Amount must be greater than zero.");
        return;
      }

      // Έλεγχος υπολοίπου (όπως check_balance στο Python)
      if (this.userBalance < money) {
        alert("Your balance is too low. Please select a lower amount.");
        return;
      }

      // Ενεργοποιούμε το flag φόρτωσης
      this.loading = true;
      console.log(`Attempting transfer: ${money}€ → ${this.recipientIban}`);

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        /*
          Η συνάρτηση transfer() στο api.js στέλνει:
            POST /api/transfer
          με body:
            { recipient: recipientIban, amount: money }

          Ο Flask backend αναμένεται να επιστρέψει JSON της μορφής:
            {
              "success": true,
              "message": "Transfer completed",
              "new_balance": 870.00
            }
        */
        const data = await transfer(this.recipientIban, money);

        // Έλεγχος απάντησης από Flask
        if (data.success) {
          // Αν η μεταφορά ήταν επιτυχής
          console.log("Transfer successful:", data);

          // Ενημέρωση mock υπολοίπου (προσωρινά)
          this.userBalance = data.new_balance || this.userBalance - money;

          // Ενημέρωση χρήστη
          alert(data.message || `You have successfully transferred ${money}€ to ${this.recipientIban}.`);

          // Καθαρισμός πεδίων
          this.recipientIban = "";
          this.amount = "";
        } else {
          // Αν ο server επιστρέψει σφάλμα (π.χ. IBAN δεν υπάρχει)
          console.warn("Transfer failed:", data);
          alert(data.message || "Account does not exist. Please check the IBAN.");
        }
      } catch (error) {
        // Αν παρουσιαστεί σφάλμα επικοινωνίας (π.χ. server down)
        console.error("Error during transfer:", error);
        alert("Error connecting to server.");
      } finally {
        // Απενεργοποίηση ένδειξης φόρτωσης
        this.loading = false;
      }
    }
  }
};
</script>
