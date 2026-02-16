<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->

  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <router-link to="/settings" class="settings" style="text-decoration: none;">
            <img src="/settings.png" alt="settings" class="settings_icon">
            <span class="tooltip">User Settings</span>
      </router-link>
        
      <button class="logout" @click="goToLogout()"><span>Log Out</span></button>
    </header>

    <div class="body_top">
      <h2 class="title">Transactions History</h2>
      <img src="/exit.png" alt="exit" class="exit" @click="goBack" style="cursor: pointer;">
    </div>

    <section class="trans_section">
      <div class="container">
        <h1 class="trans_title">Transactions</h1>
        <div class="table_wrapper">
          <table class="trans_table">
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>From IBAN </th>
                <th>To IBAN </th>
                <th>Amount </th>
                <th>Currency </th>
                <th>Date </th>
                <th>Transaction Type</th>
              </tr>
            </thead>

            <tbody id="trans_body">
              <tr v-if="transactions.length === 0 && !loading">
                <td colspan="7" style="text-align: center;">No transactions found.</td>
              </tr>

              <tr v-for="(t, index) in transactions" :key="index">
                <td>
                  {{ t[0] }}</td> <td>{{ t[1] }}</td> 
                  <td>{{ t[2] }}</td> <td>{{ t[3] }}</td> 
                  <td>{{ t[4] }}</td> <td>{{ t[5] }}</td> 
                  <td :class="t[6] === 'DEBIT' ? 'debit' : 'credit'">
                    {{ t[6] }}
                  </td>
              </tr>
                    
            </tbody>
          </table>
        </div>

        <div v-if="loading" style="text-align: center; padding: 20px; color: white;">
          Loading transactions...
        </div>  
      </div>
    </section>
  </div>

  <!-- 
  <section style="background: gray;">
    <h2>Transactions</h2>

    // Πίνακας συναλλαγών 
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
          <td>{{ t[0] }}</td>
          <td>{{ t[1] }}</td>
          <td>{{ t[2] }}</td>
          <td>{{ t[3] }}</td>
          <td>{{ t[4] }}</td>
          <td>{{ t[5] }}</td>
          <td>{{ t[6] }}</td>
        </tr>
      </tbody>
    </table>

    // Κουμπί επιστροφής 
    <button v-if="transactions.length" @click="goBack">
      ⬅ Back
    </button>
  </section>
  -->
</template>

<script>
// Εισάγουμε τη συνάρτηση getTransactions() από το api.js
import { onMounted } from "vue";
import { getTransactions } from "../services/api.js";

export default {
  name: "TransactionsView",

  data() {
    return {
      transactions: [], // Πίνακας συναλλαγών
      loading: false    // Flag φόρτωσης
    };
  },

  mounted() {
      // Φόρτωση συναλλαγών κατά το mount (προαιρετικό)
      this.fetchTransactions();
  },

  methods: {
    
    /*
      fetchTransactions()
      -------------------
      Φέρνει τη λίστα συναλλαγών από τον Flask backend μέσω api.js.
    */
    async fetchTransactions() {
      this.loading = true;
      console.log("Fetching transactions...");

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND μέσω getTransactions()
        const data = await getTransactions();

        if (data.success) {
          // Επιτυχής φόρτωση
          this.transactions = data.transactions;
          console.log("Transactions loaded:", data.transactions);
        } else {
          // Αποτυχία backend
          alert("Failed to load transactions.");
          console.warn("Backend returned failure.", data);
        }
      } catch (error) {
        // Αποτυχία επικοινωνίας
        console.error("Error loading transactions:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    /*
      goBack()
      -------------------
      Επιστρέφει στη βασική σελίδα (Home ή Transfers).
    */
    goBack() {
      // Αλλάζεις το route σε ό,τι θες
      this.$router.push("/home");
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
    }
  }
};
</script>

<style scoped>
@import "../assets/transaction_style.css";
</style>