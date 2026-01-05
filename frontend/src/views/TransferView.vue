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
import { transfer } from "../api/api.js";

export default {
  name: "TransfersView",

  data() {
    return {
      recipientIban: "",
      amount: "",
      loading: false
    };
  },

  methods: {
    async makeTransfer() {
      // Απλό validation — μόνο ότι τα πεδία δεν είναι άδεια
      if (!this.recipientIban || !this.amount) {
        alert("Please fill in all fields.");
        return;
      }

      this.loading = true;

      try {
        // Στέλνουμε τα δεδομένα ΣΤΟ BACKEND
        const data = await transfer(this.recipientIban, money);

        if (data.success) {
          alert(data.message || "Transfer completed successfully.");

          this.recipientIban = "";
          this.amount = "";
        } else {
          // Το backend δίνει το error
          alert(data.message || "Transfer failed.");
        }

      } catch (error) {
        console.error("Transfer error:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
