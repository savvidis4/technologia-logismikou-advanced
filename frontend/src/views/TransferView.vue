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
import { transfer } from "../services/api.js";

export default {
  name: "TransfersView",

  data() {
    return {
      recipientIban: "",
      amount: "",
      userBalance: 0,  

      // Χρησιμοποιείται για να αποτρέπει πολλαπλά κλικ στο κουμπί
      // ενώ η μεταφορά βρίσκεται σε εξέλιξη. Αν είναι true, το κουμπί "κλειδώνει".
      loading: false
    };
  },

  methods: {
    async makeTransfer() {
      // Έλεγχος ότι όλα τα πεδία είναι συμπληρωμένα
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

      // Έλεγχος υπολοίπου χρήστη (mock)
      if (this.userBalance < money) {
        alert("Your balance is too low.");
        return;
      }

      // Ξεκινάμε loading για να μην μπορεί να πατήσει ξανά
      this.loading = true;
      console.log("Attempting transfer:", this.recipientIban, money);

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        const data = await transfer(this.recipientIban, money);

        // Επεξεργασία απάντησης από Flask
        if (data.success) {
          alert(`Transfer of ${money}€ completed.`);
          this.userBalance -= money;
          this.recipientIban = "";
          this.amount = "";
        } else {
          alert("Transfer failed. Invalid IBAN or insufficient balance.");
        }
      } catch (error) {
        console.error("Error during transfer:", error);
        alert("Error connecting to server.");
      } finally {
        // Σταματάμε το loading 
        this.loading = false;
      }
    }
  }
};
</script>