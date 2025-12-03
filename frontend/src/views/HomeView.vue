<template>
  <!-- Λογικά εδώ θα μπει ο κώδικας του Λάμπρου -->
   <div>
      <!-- HEADER -->
       <header class="header">
        <img src="logo.png" alt="bank logo" class="img"/>
        <h2 class="logo">Bank of University of West Attica e-Banking</h2>
        <button class="settings" @click="goToSettings">
            <img src="settings.png" alt="settings" class="settings_icon"/>
            <span class="tooltip">User Settings</span>
        </button>
        <button class="logout" @click="goToLogout"><span>Log Out</span></button>
    </header>

    <!-- ΚΟΥΤΙ ΥΠΟΛΟΙΠΟΥ -->
      <section class="container">
        <div class="balance_top">
            <h2>Balance</h2>

            <!-- ΕΔΩ ΕΧΩ ΒΑΛΕΙ ΚΑΡΦΩΤΑ ΤΙΜΕΣ ΤΩΡΑ ΔΕΝ ΞΕΡΩ ΤΙ ΜΠΑΛΙΤΣΑ ΠΑΙΖΕΤΕ -->
            <p class="amount">50,000.75 €</p>
        </div>

        <div class="balance_rest">
            <div class="row">
                <img src="card1.png" alt="iban_icon" class="icon"/>
                <div>
                    <p class="label">IBAN</p>

                    <!-- ΕΔΩ ΕΧΩ ΒΑΛΕΙ ΚΑΡΦΩΤΑ ΤΙΜΕΣ ΤΩΡΑ ΔΕΝ ΞΕΡΩ ΤΙ ΜΠΑΛΙΤΣΑ ΠΑΙΖΕΤΕ -->
                    <p class="value">GR30 0369 3768 4885 8436 2590 002</p>
                </div>
            </div>

            <div class="row">
                <img src="card1.png" alt="card_icon" class="icon"/>
                <div>
                    <p class="label">Card Number</p>

                    <!-- ΕΔΩ ΕΧΩ ΒΑΛΕΙ ΚΑΡΦΩΤΑ ΤΙΜΕΣ ΤΩΡΑ ΔΕΝ ΞΕΡΩ ΤΙ ΜΠΑΛΙΤΣΑ ΠΑΙΖΕΤΕ -->
                    <p class="value">**** **** **** 0001</p>
                </div>
            </div>
        </div>
    </section>


    <!-- SIDEBAR ΜΕ ΚΟΥΜΠΙΑ ΠΛΟΗΓΗΣΗΣ -->
     <aside class="sidebar">
        <div class="item" data-tooltip="Transfers" @click="goTo('/transfers')">
            <img src="transfer.png" alt="transfers"/>
        </div>

        <div class="item" data-tooltip="Transactions" @click="goTo('/transactions')">
            <img src="transaction.png" alt="transactions"/>
        </div>

        <div class="item" data-tooltip="Credit Card" @click="goTo('/card')">
            <img src="card2.png" alt="card"/>
        </div>

        <div class="item" data-tooltip="Graphs" @click="goTo('/graphs')">
            <img src="graphs.png" alt="graph"/>
        </div>

        <div class="item" data-tooltip="Currency Exchange" @click="goTo('/exchange')">
            <img src="exchange.png" alt="exchange"/>
        </div>
    </aside>
   </div>

   <!-- ΕΔΩ ΤΕΛΕΙΩΝΕΙ Ο ΚΩΔΙΚΑΣ ΤΟΥ ΛΑΜΠΡΟΥ  -->

  <section>
    <!-- <h2>BANK OF UNIVERSITY OF WEST ATTICA e-Banking</h2> -->

    <!-- Mock στοιχεία λογαριασμού -->
    <div>
      <p><strong>Balance:</strong> {{ balance }} €</p>
      <p><strong>IBAN:</strong> {{ iban }}</p>
      <p><strong>Card Number:</strong> {{ cardNumber }}</p>
    </div>

    <!-- Κουμπιά πλοήγησης (router-links) -->
    <p>
      <!-- <router-link to="/signin">Sign In</router-link> |
      <router-link to="/signup">Sign Up</router-link> |
      <router-link to="/transfers">Transfers</router-link> |
      <router-link to="/transactions">Transactions</router-link> |
      <router-link to="/currency">Currency Exchange</router-link> |
      <router-link to="/card">Card</router-link> |
      <router-link to="/graphs">Graphs</router-link> |
      <router-link to="/settings">Settings</router-link> |
      <router-link to="/logout">Log Out</router-link> -->
    </p>
  </section>
</template>

<script>
// Εισάγουμε τη συνάρτηση getAccount() από το api.js
import { getAccount } from "../services/api.js";
import { ref } from 'vue'

const data = ref(null)

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
   const token = localStorage.getItem('token')
    if (!token) {
      window.location.href = '/login'
      return
    }

    this.loading = true;
    try {
      const data = await getAccount();

      if (data.success) {
        this.balance = data.euro_balance;
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
  }
};
</script>
