<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section style="background: gray;">
    <h2>Transactions</h2>

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

    <!-- Κουμπί επιστροφής -->
    <button v-if="transactions.length" @click="goBack">
      ⬅ Back
    </button>
  </section>
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
    }
  }
};
</script>
