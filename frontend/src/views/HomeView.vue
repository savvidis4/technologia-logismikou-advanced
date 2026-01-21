<template>
  <!-- Λογικά εδώ θα μπει ο κώδικας του Λάμπρου -->
  <div>
    <!-- <section>
    <h2>BANK OF UNIVERSITY OF WEST ATTICA e-Banking</h2>

    
    <div>
      <p><strong>Balance:</strong> {{ balance }} €</p>
      <p><strong>IBAN:</strong> {{ iban }}</p>
      <p><strong>Card Number:</strong> {{ cardNumber }}</p>
    </div>

        <div class="row">
          <img src="/card1.png" alt="card_icon" class="icon">
          <div>
            <p class="label">Card Number</p>
            <p class="value">{{ cardNumber }}</p>
          </div>
        </div>
    </section> -->

    <!-- HEADER -->
    <header class="header">
      <img src="/logo.png" alt="bank_logo" class="img" />
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
     

    <!-- SETTINGS -->
    <button class="settings" @click="goToSettings">
      <img src="/settings.png" alt="settings" class="settings_icon" />
      <span class="tooltip">User Settings</span>
    </button>
    

    <!-- LOGOUT -->
    <button class="logout" @click="goToLogout">
      <span>Log Out</span>
    </button>
    </header>

    <!-- MAIN BALANCE CARD -->
    <!-- ΕΔΩ ΥΠΑΡΧΟΥΝ ΚΑΡΦΩΤΕΣ ΤΙΜΕΣ ΓΙΑ ΔΟΚΙΜΗ -->
    <section class="container">
        <div class="balance_top">
            <h2>Balance</h2>
            <p class="amount">{{ balance }} €</p>
        </div>

        <div class="balance_rest">
            <div class="row">
                <img src="/card1.png" alt="iban_icon" class="icon"/>
                <div>
                    <p class="label">IBAN</p>
                    <p class="value">{{ iban }}</p>
                </div>
            </div>

            <div class="row">
                <img src="/card1.png" alt="card_icon" class="icon"/>
                <div>
                    <p class="label">Card Number</p>
                    <p class="value">{{ cardNumber }}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- SIDEBAR -->
    <aside class="sidebar">

      <div class="item" data-tooltip="Transfers">
        <router-link to="/transfers">
          <img src="/transfer.png" alt="transfers">
        </router-link>
      </div>

      <div class="item" data-tooltip="Transactions">
        <router-link to="/transactions">
          <img src="/transaction.png" alt="transactions">
        </router-link>
      </div>

      <div class="item" data-tooltip="Credit Card">
        <router-link to="/card">
          <img src="/card2.png" alt="card">
        </router-link>
      </div>

      <div class="item" data-tooltip="Graphs">
        <router-link to="/graphs">
          <img src="/graphs.png" alt="graph">
        </router-link>
      </div>

      <div class="item" data-tooltip="Currency Exchange">
        <router-link to="/exchange">
          <img src="/exchange.png" alt="exchange">
        </router-link>
      </div>
    </aside>
  </div>
  <!-- ΤΕΛΟΣ ΚΩΔΙΚΑ ΛΑΜΠΡΟΥΚΟΥ-->
</template>

<script>
// Εισάγουμε τη συνάρτηση getAccount() από το api.js
import { getAccount } from "../services/api.js";

export default {
  name: "HomeView",

  data() {
    return {
      balance: null,        // Υπόλοιπο χρήστη
      iban: "",             // IBAN λογαριασμού
      cardNumber: "",       // Κάρτα χρήστη (masked)
      accountLoaded: false, // Flag για το αν έχουν φορτωθεί τα στοιχεία  
    };
  },

  

  async mounted() {
    /*
      ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
      Μόλις "φορτωθεί" η σελίδα (mounted),
      καλούμε τη συνάρτηση getAccount() από το api.js
      για να φέρει τα στοιχεία λογαριασμού του χρήστη.
    */
    this.loading = true;
    try {
      const data = await getAccount();

      if (data.success) {
        this.balance = data.balance;
        this.iban = data.iban;
        this.cardNumber = data.card_number;
        this.accountLoaded = true;
        console.log("Account info loaded successfully:", data);
      } else {
        alert(data.message || "Failed to load account information.");
      }
    } catch (error) {
      console.error("Error loading account info:", error);
      alert("Error connecting to server.");
    } finally {
      this.loading = false;
    }
  },

  methods: {
    goToSettings() {
      // Πηγαίνει στο component SettingsView.vue
      this.$router.push("/settings");
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
    }
  }
}
</script>



<style scoped>
@import "../assets/home_style.css";
</style>
