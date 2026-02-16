<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->

  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <button class="settings" @click="goToSettings">
        <img src="/settings.png" alt="settings" class="settings_icon" />
        <span class="tooltip">User Settings</span>
      </button>
        
      <button class="logout" @click="user_logout">
        <span>Log Out</span>
      </button>
    </header>

    <section class="container">
      <div class="transfer_top">
        <h2>Transfers</h2> 
        
        <router-link to="/home" class="exit">
          <img src="/exit.png" alt="exit">
        </router-link>
      </div>

      <form class="transfer_form" @submit.prevent="makeTransfer">
        <div class="form_row">
          <label for="form">From</label>
          <span class="iban">{{ myiban || 'Loading...' }}</span>
        </div>

        <div class="form_row">
          <label for="to">To</label>
          <input type="text" v-model="recipientIban" placeholder="Recipient IBAN" required>
        </div>

        <div class="form_row">
          <label for="amount">Amount (€)</label>
          <input type="number" step="0.01" v-model="amount" id="amount" placeholder="Enter amount" required>
        </div>

        <button type="submit" class="send" :disabled="loading">
          <span>{{ loading ? "Processing..." : "Transfer" }}</span>
        </button>
      </form>
    </section>
  </div>



  <!-- 
  <section>
    <h2 style="color: black;">Transfers</h2>

    <p style="color: black;">Account IBAN (From): {{myiban}}</p>

     //Φόρμα μεταφοράς χρημάτων 
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
  -->
</template>

<script>
import { transfers, transfer_data } from "../services/api.js";

export default {
  name: "TransfersView",

  data() {
    return {
      recipientIban: "",
      amount: "",
      currency: "EUR",
      loading: false,
      myiban: ""
    };
  },

  async mounted() {
      
      const data = await transfer_data();
      this.myiban = data.account_iban;
    
  },

  methods: {
    
    goToSettings() {
      // Πηγαίνει στο component SettingsView.vue
      this.$router.push("/settings");
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
    },


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

<style scoped>
@import "../assets/transfer_style.css";
</style>