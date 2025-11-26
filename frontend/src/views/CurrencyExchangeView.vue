<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Currency Exchange</h2>

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
        <option>Euro</option>
        <option>Dollar</option>
        <option>Yen</option>
        <option>Yuan</option>
      </select>

      <select v-model="currencyTo" required>
        <option disabled value="">Select to</option>
        <option>Euro</option>
        <option>Dollar</option>
        <option>Yen</option>
        <option>Yuan</option>
      </select>

      <button type="submit" :disabled="loading">
        {{ loading ? "Processing..." : "Exchange" }}
      </button>
    </form>
  </section>
</template>

<script>
import { exchange } from "../api/api.js";

export default {
  name: "CurrencyExchangeView",

  data() {
    return {
      amount: "",
      currencyFrom: "",
      currencyTo: "",

      // Mock balances (μέχρι να κάνουμε endpoint για πραγματικά balances)
      balances: {
        Euro: 500,
        Dollar: 200,
        Yen: 15000,
        Yuan: 1000
      },

      loading: false
    };
  },

  methods: {
    // Μεταφορά Python calc_value → Vue
    calcValue(amount, from, to) {
      const rates = {
        Euro: { Dollar: 1.1463, Yen: 170.4335, Yuan: 8.2176 },
        Dollar: { Euro: 0.8692, Yen: 148.2383, Yuan: 7.1521 },
        Yen: { Euro: 0.0058, Dollar: 0.0067, Yuan: 0.0480 },
        Yuan: { Euro: 0.1202, Dollar: 0.1381, Yen: 20.5003 }
      };

      return parseFloat(amount) * rates[from][to];
    },

    // Έλεγχος υπολοίπου (Python → Vue)
    checkBalance(amount, currency) {
      const available = this.balances[currency];
      if (available < amount) {
        alert("Your balance is too low.");
        return false;
      }
      return true;
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

        if (data.success) {
          // Αν επιτυχής μετατροπή → κάνε update balances (mock)
          const newValue = this.calcValue(value, this.currencyFrom, this.currencyTo);

          this.balances[this.currencyFrom] -= value;
          this.balances[this.currencyTo] += newValue;

          alert(`You exchanged ${value} ${this.currencyFrom} into ${newValue.toFixed(2)} ${this.currencyTo}.`);
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
