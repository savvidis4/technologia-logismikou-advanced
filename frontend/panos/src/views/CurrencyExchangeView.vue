<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Currency Exchange</h2>

    <!-- Φόρμα ανταλλαγής νομισμάτων -->
    <form @submit.prevent="makeExchange">
      <input
        type="number"
        v-model="amount"
        placeholder="Amount"
        min="0.01"
        step="0.01"
        required
      />

      <!-- Επιλογή από νομίσματα -->
      <select v-model="currencyFrom" required>
        <option disabled value="">Select from currency</option>
        <option>Euro</option>
        <option>Dollar</option>
        <option>Yen</option>
        <option>Yuan</option>
      </select>

      <select v-model="currencyTo" required>
        <option disabled value="">Select to currency</option>
        <option>Euro</option>
        <option>Dollar</option>
        <option>Yen</option>
        <option>Yuan</option>
      </select>

      <button type="submit" :disabled="loading">
        {{ loading ? "Processing..." : "Convert" }}
      </button>
    </form>

    <!-- Εμφάνιση αποτελέσματος -->
    <p v-if="convertedAmount">
      {{ amount }} {{ currencyFrom }} = 
      <strong>{{ convertedAmount.toFixed(2) }} {{ currencyTo }}</strong>
    </p>
  </section>
</template>

<script>
// Εισάγουμε τη συνάρτηση exchange από το api.js
import { exchange } from "../api/api.js";

export default {
  name: "CurrencyExchangeView",

  data() {
    return {
      amount: "",           // Ποσό για μετατροπή
      currencyFrom: "",     // Νόμισμα προέλευσης
      currencyTo: "",       // Νόμισμα προορισμού
      convertedAmount: null,// Αποτέλεσμα μετατροπής (εμφανίζεται στο template)
      loading: false        // Ένδειξη "φόρτωσης"
    };
  },

  methods: {
    /*
      makeExchange()
      -----------------
      Η κύρια συνάρτηση που υλοποιεί τη λογική της ανταλλαγής νομίσματος.
      Είναι το ισοδύναμο του exchange(info, iban_to, value, ...) στο Python desktop app.
      
      Περιλαμβάνει:
       Έλεγχο δεδομένων (αν έχουν συμπληρωθεί όλα)
       Κλήση στο Flask backend (μέσω api.js)
       Εμφάνιση του αποτελέσματος
    */
    async makeExchange() {
      // Έλεγχος αν όλα τα πεδία είναι συμπληρωμένα
      if (!this.amount || !this.currencyFrom || !this.currencyTo) {
        alert("Please fill in all fields.");
        return;
      }

      // Έλεγχος ότι δεν έχει επιλεγεί ίδιο νόμισμα (από / προς)
      if (this.currencyFrom === this.currencyTo) {
        alert("Please select different currencies for exchange.");
        return;
      }

      //  Ενεργοποίηση ένδειξης φόρτωσης
      this.loading = true;
      const value = parseFloat(this.amount);

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        /*
          Κλήση του Flask API μέσω της συνάρτησης exchange() από το api.js.
          Το api.js στέλνει:
            POST /api/exchange
          με body:
            {
              amount: value,
              currency_from: this.currencyFrom,
              currency_to: this.currencyTo
            }
        */
        const data = await exchange(value, this.currencyFrom, this.currencyTo);

        // Αν το backend επιστρέψει επιτυχία
        if (data.success) {
          /*
            Ο Flask backend θα πρέπει να επιστρέφει π.χ.:
            {
              "success": true,
              "converted_value": 113.45,
              "message": "Exchange successful"
            }
          */

          // Ενημερώνουμε τοπικά την τιμή που θα εμφανιστεί στο template
          this.convertedAmount = data.converted_value;

          // Ενημερωτικό μήνυμα στο χρήστη
          alert(
            `You have successfully exchanged ${value} ${this.currencyFrom} into ${data.converted_value.toFixed(
              2
            )} ${this.currencyTo}.`
          );

          console.log("Exchange successful:", data);
        } else {
          // Αν αποτύχει η ανταλλαγή (π.χ. χαμηλό υπόλοιπο, λάθος νόμισμα)
          alert(data.message || "Exchange failed. Please try again.");
          console.warn("Exchange failed:", data);
        }
      } catch (error) {
        // Σε περίπτωση αποτυχίας επικοινωνίας με το backend
        console.error("Error during exchange:", error);
        alert("Error connecting to server.");
      } finally {
        // Τέλος: επαναφορά του κουμπιού (φόρτωση = false)
        this.loading = false;
      }
    }
  }
};
</script>

