<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Currency Exchange</h2>

    <p>Available Balances:</p>
    <ul>
      <li>Euro: {{ balances.euro_balance }}</li>
      <li>Dollar: {{ balances.usd_balance }}</li>
      <li>Yen: {{ balances.yen_balance }}</li>
      <li>Pound: {{ balances.gbp_balance }}</li>
    </ul>
    <!-- Φόρμα μετατροπής -->
    <form @submit.prevent="makeExchange">
      <input
        type="number"
        v-model="amount"
        placeholder="Amount"
        required
      />

      <select v-model="currencyFrom" required>
        <option disabled value="">Select from</option>
        <option>EUR</option>
        <option>USD</option>
        <option>GBP</option>
        <option>JPY</option>
      </select>

      <select v-model="currencyTo" required>
        <option disabled value="">Select to</option>
        <option>EUR</option>
        <option>USD</option>
        <option>GBP</option>
        <option>JPY</option>
      </select>

      <button type="submit" :disabled="loading">
        {{ loading ? "Processing..." : "Exchange" }}
      </button>
    </form>
  </section>
</template>

<script>
import { exchange, getExchange } from "../services/api.js";

export default {
  name: "CurrencyExchangeView",

  data() {
    return {
      amount: "",
      currencyFrom: "",
      currencyTo: "",
      balances: {
        euro_balance: "0.0",
        usd_balance: "0.0",
        gbp_balance: "0.0",
        yen_balance: "0.0"
      },

      loading: false
    };
  },

  mounted() {
    this.getExchange();  // Φορτώνουμε τα στοιχεία μόλις φορτώσει το component
  },

  methods: {
    

    // Έλεγχος υπολοίπου (Python → Vue)
    checkBalance(amount, currency) {
      const available = this.balances[currency];
      if (available < amount) {
        alert("Your balance is too low.");
        return false;
      }
      return true;
    },

    async getExchange(){
      this.loading = true;
      console.log("Loading exchange data...");

      try {
        const data = await getExchange();   // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND

        if (data.success) {
          this.balances.euro_balance = data.euro_balance;
          this.balances.usd_balance = data.usd_balance;
          this.balances.gbp_balance = data.gbp_balance;
          this.balances.yen_balance = data.yen_balance;
          console.log("Exchange data loaded:", this.balances);
        } else {
          alert("Failed to load exchange data.");
        }
      } catch (error) {
        console.error("Error loading exchange data:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    async makeExchange() {
      if (!this.amount || !this.currencyFrom || !this.currencyTo) {
        alert("Please fill in all fields.");
        return;
      }

      if (this.currencyFrom === this.currencyTo) {
        alert("Currencies must be different.");
        return;
      }

      const value = parseFloat(this.amount);
      if (value <= 0) {
        alert("Amount must be greater than zero.");
        return;
      }

      // CHECK BALANCE
      if (!this.checkBalance(value, this.currencyFrom)) {
        return;
      }

      this.loading = true;

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        /*
          POST /api/exchange
          { amount, currency_from, currency_to }
          
          Flask returns:
          { "success": true } OR { "success": false }
        */
        const data = await exchange(value, this.currencyFrom, this.currencyTo);

        if (data.converted_amount == 0.0) {
          alert(`Exchange failed. ${data.errmsg}`);
          return;
        }

        if (data.success) {
          this.getExchange();  // Ενημερώνουμε τα υπόλοιπα μετά την ανταλλαγή

          alert(`You exchanged ${value} ${this.currencyFrom} into ${data.converted_amount.toFixed(2)} ${this.currencyTo}.`);
        } else {
          alert("Exchange failed. Please try again.");
        }
      } catch (error) {
        console.error("Exchange error:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
