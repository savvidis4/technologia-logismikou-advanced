<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Your Card</h2>

    <!-- Κουμπί για φόρτωση στοιχείων κάρτας -->
    <button @click="loadCard" :disabled="loading">
      {{ loading ? "Loading..." : "Show Card Details" }}
    </button>

    <!-- Στοιχεία κάρτας -->
    <div v-if="card">
      <p><strong>Card Number:</strong> {{ card.number }}</p>
      <p><strong>Expiration:</strong> {{ card.exp }}</p>
      <p><strong>CVV:</strong> {{ card.cvv }}</p>
      <p><strong>Status:</strong> {{ card.isFrozen ? "Frozen" : "Active" }}</p>

      <!-- Κουμπί Freeze / Unfreeze -->
      <button @click="toggleFreeze" :disabled="loading">
        {{ card.isFrozen ? "Unfreeze Card" : "Freeze Card" }}
      </button>
    </div>
  </section>
</template>

<script>
import { getCard, toggleCardFreeze } from "../api/api.js";

export default {
  name: "CardView",

  data() {
    return {
      card: null,      // εδώ θα μπουν τα στοιχεία της κάρτας από το backend
      loading: false   // για να μπλοκάρουμε κουμπιά όσο μιλάμε με Flask
    };
  },

  methods: {
    // 1) Φόρτωση στοιχείων κάρτας από backend
    async loadCard() {
      this.loading = true;
      console.log("Loading card data...");

      try {
        const data = await getCard();   // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND

        if (data.success) {
          this.card = data.card;        // π.χ. { number, exp, cvv, isFrozen }
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
