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

    <section class="container">
      <div class="card_top">
        <h2>Your Card</h2> 
          <div class="exit" @click="goBack" style="cursor: pointer;">
            <img src="/exit.png" alt="exit">
          </div>
      </div>

        <div class="card_template">
            <div v-if="card" class="your_card">
                <img src="/card_template.png" alt="credit card" class="card_bg">
                <div class="card_overlay">
                  <div class="card_header">
                      <img src="/logo_card.png" alt="logo" class="card_logo">
                      <h3 class="bank_name">Bank of UniWA</h3>
                  </div>

                  <div class="card_number">{{ formatCardNumber(card.number) }}</div>

                    <div class="card_info">
                      <p>EXP: {{ card.exp }}</p>
                      <p>CVV: {{ card.cvv }}</p>
                    </div>
                </div>  
              </div>
            <div v-else style="color: black; text-align: center;">Loading card details...</div>
        </div>

        <button 
            v-if="card"
            type="button" 
            class="freeze" 
            :class="{ 'active': card.isFrozen }"
            @click="toggleFreeze"
            :disabled="loading"
        >
            <span>{{ card.isFrozen ? 'Unfreeze' : 'Freeze' }}</span>
        </button>
    </section>

  </div>

  <!-- 
  <section style="max-width: 400px; margin: auto; background-color: gray;">
    <h2>Your Card</h2>

    // Στοιχεία κάρτας 
    <div v-if="card">
      <p><strong>Card Number:</strong> {{ card.number }}</p>
      <p><strong>Expiration:</strong> {{ card.exp }}</p>
      <p><strong>CVV:</strong> {{ card.cvv }}</p>
      <p><strong>Status:</strong> {{ card.isFrozen ? "Frozen" : "Active" }}</p>

      // Κουμπί Freeze / Unfreeze 
      <button @click="toggleFreeze" :disabled="loading">
        {{ card.isFrozen ? "Unfreeze Card" : "Freeze Card" }}
      </button>
    </div>
  </section>
  -->
</template>

<script>
import { getCard, toggleCardFreeze } from "../services/api.js";

export default {
  name: "CardView",

  data() {
    return {
      card: null,      // εδώ θα μπουν τα στοιχεία της κάρτας από το backend
      loading: false   // για να μπλοκάρουμε κουμπιά όσο μιλάμε με Flask
    };
  },

  mounted() {
    this.loadCard();  // Φορτώνουμε τα στοιχεία μόλις φορτώσει το component
  },

  methods: {
    // ΛΑΜΠΡΟΣ: Προσθήκη συναρτήσεων για να εμφανίζεται η κάρτα και για λογκ αουτ και για Home
    formatCardNumber(num) {
      if (!num) return "0000 0000 0000 0000";
      return num.toString().replace(/\d{4}(?=.)/g, '$& ');
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
    },

    goBack() {
      // Αλλάζεις το route σε ό,τι θες
      this.$router.push("/home");
    },

    // 1) Φόρτωση στοιχείων κάρτας από backend
    async loadCard() {
      this.loading = true;
      console.log("Loading card data...");

      try {
        const data = await getCard();   // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND

        if (data.success) {
          this.card = data;        // π.χ. { number, exp, cvv, isFrozen }
          console.log("Card loaded:", this.card);
        } else {
          alert("Failed to load card data.");
        }
      } catch (error) {
        console.error("Error loading card:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    // 2) Αλλαγή κατάστασης κάρτας (freeze/unfreeze)
    async toggleFreeze() {
      if (!this.card) return;  // αν δεν έχουν φορτωθεί στοιχεία, δεν κάνουμε τίποτα

      const confirmMsg = this.card.isFrozen
        ? "Are you sure you want to unfreeze your card?"
        : "Are you sure you want to freeze your card?";

      if (!confirm(confirmMsg)) {
        console.log("User canceled freeze/unfreeze.");
        return;
      }

      this.loading = true;

      try {
        // Θέλουμε η νέα κατάσταση να είναι το αντίθετο της τωρινής
        const newFreezeState = !this.card.isFrozen;

        const data = await toggleCardFreeze(newFreezeState); // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND

        if (data.success) {
          this.card.isFrozen = newFreezeState;
          alert(
            this.card.isFrozen
              ? "Your card has been frozen."
              : "Your card has been unfrozen."
          );
        } else {
          alert("Failed to update card status.");
        }
      } catch (error) {
        console.error("Error toggling card state:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>


<style scoped>
@import "../assets/card_style.css";
</style>