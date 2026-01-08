<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2 style="color: black;">Transfers</h2>

    <p style="color: black;">Account IBAN (From): {{myiban}}</p>

    <!-- Φόρμα μεταφοράς χρημάτων -->
    <form @submit.prevent="makeTransfer">
      <input
        type="text"
        v-model="recipientIban"
        placeholder="Recipient IBAN (To)"
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

      <input
        type="text"
        v-model="currency"
        placeholder="Currency"
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
import { transfers, transfer_data } from "../services/api.js";

export default {
  name: "TransfersView",

  data() {
    return {
      recipientIban: "",
      amount: "",
      loading: false,
      myiban: ""
    };
  },

  async mounted() {
      
      const data = await transfer_data();
      this.myiban = data.account_iban;
    
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
        console.log("Initiating transfer to:", this.recipientIban, "Amount:", this.amount);
        const data = await transfers(this.recipientIban, this.amount, this.currency);

        console.log("Transfer response:", data);

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
