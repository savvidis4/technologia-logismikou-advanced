<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->

<div>
<div class="exchange_wrapper">

  


    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <button class="settings" @click="goToSettings">
        <img src="/settings.png" alt="settings" class="settings_icon" />
        <span class="tooltip">User Settings</span>
      </button>
      <button class="logout" @click="goToLogout"><span>Log Out</span></button>
    </header>

    <div class="body_top">
      <h2 class="title">Currency Exchange</h2>
      <img src="/exit.png" alt="exit" class="exit" @click="$router.push('/home')" style="cursor: pointer;">
    </div>

    <div class="main_wrapper">
      
      <div class="balance-board">
        <h3 class="balance-title">Account Balances</h3>
        <div class="balance-item">
          <span class="curr-name">Euro (€)</span>
          <span class="curr-amount">{{ balances.euro_balance }} €</span>
        </div>
        <div class="balance-item">
          <span class="curr-name">US Dollar ($)</span>
          <span class="curr-amount">{{ balances.usd_balance }} $</span>
        </div>
        <div class="balance-item">
          <span class="curr-name">Japanese Yen (¥)</span>
          <span class="curr-amount">{{ balances.yen_balance }} ¥</span>
        </div>
        <div class="balance-item">
          <span class="curr-name">Chinese Yuan (¥)</span>
          <span class="curr-amount">{{ balances.gbp_balance }} ¥</span>
        </div>
      </div>

      <div class="container">
        <div class="ex_box">
          <div class="row">
            <div class="label">From :</div>
            <div class="currency">
              <div class="dropdown">
                <button class="drop">
                  <img :src="getFlag(currencyFrom)" class="flag">
                  <span class="code">{{ currencyFrom }}</span>
                </button>
                <div class="drop_content">
                  <div v-for="curr in availableCurrencies" :key="curr.code" class="option" @click="currencyFrom = curr.code">
                    <img :src="curr.flag" class="flag">
                    <span>{{ curr.code }}</span>
                  </div>
                </div>
              </div>
            </div>
            <input type="number" v-model="amount" class="input" placeholder="0.00">
          </div>

          <div class="row">
            <div class="label">To :</div>
            <div class="currency">
              <div class="dropdown">
                <button class="drop">
                  <img :src="getFlag(currencyTo)" class="flag">
                  <span class="code">{{ currencyTo }}</span>
                </button>
                <div class="drop_content">
                  <div v-for="curr in availableCurrencies" :key="curr.code" class="option" @click="currencyTo = curr.code">
                    <img :src="curr.flag" class="flag">
                    <span>{{ curr.code }}</span>
                  </div>
                </div>
              </div>
            </div>
            <input type="text" :value="convertedDisplay" class="input" disabled>
          </div>
        </div>
      </div>
    </div> <button type="submit" class="exchange" @click="handleExchange" :disabled="loading">
      <span>{{ loading ? 'Processing...' : 'Exchange' }}</span>
    </button>

    <img src="/scale.png" alt="scale" class="scale_icon">
    <img src="/updown.png" alt="updown" class="updown_icon">
  </div>
  </div>

<!-- 
  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <button class="settings" @click="goToSettings">
        <img src="/settings.png" alt="settings" class="settings_icon" />
        <span class="tooltip">User Settings</span>
      </button>
        
      <button class="logout" @click="goToLogout"><span>Log Out</span></button>
    </header>

    <div class="body_top">
        <h2 class="title">Currency Exchange</h2>
        <router-link to="/home" class="exit">
            <img src="/exit.png" alt="exit">
        </router-link>
    </div>

    <div class="main_wrapper">
      <div class="balance-board">
        <h3 class="balance-title">Account Balances</h3>
        <div class="balance-item">
          <span class="curr-name">Euro (€)</span>
          <span class="curr-amount">{{ balances.euro_balance }} €</span>
        </div>
        <div class="balance-item">
          <span class="curr-name">US Dollar ($)</span>
          <span class="curr-amount">{{ balances.usd_balance }} $</span>
        </div>
        <div class="balance-item">
          <span class="curr-name">Japanese Yen (¥)</span>
          <span class="curr-amount">{{ balances.yen_balance }} ¥</span>
        </div>
        <div class="balance-item">
          <span class="curr-name">Chinese Yuan (¥)</span>
          <span class="curr-amount">{{ balances.gbp_balance }} ¥</span>
        </div>
      </div>
    </div>

    <div class="container">
        <div class="ex_box">
            <div class="row">
                <div class="label">From :</div>
                <div class="currency">
                    <select v-model="currencyFrom" class="vue_select">
                        <option value="EUR">EUR (€) - Bal: {{ balances.euro_balance }}</option>
                        <option value="USD">USD ($) - Bal: {{ balances.usd_balance }}</option>
                        <option value="GBP">CNY (¥) - Bal: {{ balances.gbp_balance }}</option>
                        <option value="JPY">JPY (¥) - Bal: {{ balances.yen_balance }}</option>
                    </select>
                </div>
                <input type="number" v-model="amount" class="input" placeholder="Amount">
            </div>

            <img src="/updown.png" alt="updown" class="updown_icon" @click="swapCurrencies">

            <div class="row">
                <div class="label">To :</div>
                <div class="currency">
                    <select v-model="currencyTo" class="vue_select">
                        <option value="EUR">EUR (€)</option>
                        <option value="USD">USD ($)</option>
                        <option value="CNY">CNY (¥)</option>
                        <option value="JPY">JPY (¥)</option>
                    </select>
                </div>
                <input type="text" :value="convertedResult" class="input" disabled placeholder="Result">
            </div>
        </div>
    </div>

    <button type="button" class="exchange" @click="makeExchange" :disabled="loading">
        <span>{{ loading ? 'Processing...' : 'Exchange' }}</span>
    </button>

    <img src="/scale.png" alt="scale" class="scale_icon">

  </div>
  -->

  <!-- 
  <section>
    <h2>Currency Exchange</h2>

    <p>Available Balances:</p>
    <ul>
      <li>Euro: {{ balances.euro_balance }}</li>
      <li>Dollar: {{ balances.usd_balance }}</li>
      <li>Yen: {{ balances.yen_balance }}</li>
      <li>Pound: {{ balances.gbp_balance }}</li>
    </ul>
    // Φόρμα μετατροπής 
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
  -->
</template>

<script>
import { exchange, getExchange } from "../services/api.js";

export default {
  name: "CurrencyExchangeView",

  data() {
    return {
      amount: "",
      currencyFrom: "EUR",
      currencyTo: "EUR",
      balances: {
        euro_balance: "0.0",
        usd_balance: "0.0",
        gbp_balance: "0.0",
        yen_balance: "0.0"
      },

      loading: false,
      
      availableCurrencies: [
        { code: "EUR", flag: "/greece.png" },
        { code: "USD", flag: "/usa.png" },
        { code: "JPY", flag: "/japan.png" },
        { code: "CNY", flag: "/china.png" } // Πρόσθεσα GBP όπως το API σου
      ]

    };
  },

  mounted() {
    this.getExchange();  // Φορτώνουμε τα στοιχεία μόλις φορτώσει το component
  },

  methods: {
    selectCurrency(code, type) {
      if (type === 'from') this.currencyFrom = code;
      else this.currencyTo = code;
      this.dropdownActive = false;
    },

    getFlag(code) {
      const curr = this.availableCurrencies.find(c => c.code === code);
      return curr ? curr.flag : '';
    },
    
    goToSettings() {
      // Πηγαίνει στο component SettingsView.vue
      this.$router.push("/settings");
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
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

<style scoped>
@import "../assets/currencyex_style.css";


/* Fix για τα Dropdowns που λείπει από το CSS σου */
/*
.dropdown { position: relative; display: inline-block; width: 100%; }
.drop { 
  display: flex; align-items: center; justify-content: space-between;
  width: 100%; background: white; border: 1px solid #ccc; padding: 8px; border-radius: 8px;
}
.dropdown:hover .drop_content { display: block; }
.drop_content {
    display: none; position: absolute; background: white; min-width: 120px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2); z-index: 100; border-radius: 8px;
}
.option { padding: 10px; display: flex; align-items: center; gap: 10px; cursor: pointer; }
.option:hover { background: #f1f1f1; }
.flag { width: 25px; height: auto; }
*/

</style>