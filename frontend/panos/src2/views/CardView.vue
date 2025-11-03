<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Your Card</h2>

    <!-- Κουμπί για εμφάνιση στοιχείων -->
    <button @click="loadCard" :disabled="loading">
      {{ loading ? "Loading..." : "Show Card Details" }}
    </button>

    <!-- Αν υπάρχουν στοιχεία κάρτας, τα εμφανίζουμε -->
    <div v-if="card" class="card-details">
      <p><strong>Card Number:</strong> {{ card.number }}</p>
      <p><strong>Expiration:</strong> {{ card.exp }}</p>
      <p><strong>CVV:</strong> {{ card.cvv }}</p>
      <p><strong>Status:</strong> {{ card.isFrozen ? "Frozen ❄️" : "Active ✅" }}</p>

      <!-- Κουμπί Freeze / Unfreeze -->
      <button @click="toggleFreeze" :disabled="loading">
        {{ card.isFrozen ? "Unfreeze Card" : "Freeze Card" }}
      </button>
    </div>
  </section>
</template>

<script>
// ✅ Εισάγουμε τις συναρτήσεις από το api.js
import { getCard, toggleCardFreeze } from "../api/api.js";

export default {
  name: "CardView",

  data() {
    return {
      card: null,     // Στοιχεία κάρτας
      loading: false  // Flag για ένδειξη φόρτωσης
    };
  },

  methods: {
    /*
      Φορτώνει τα στοιχεία της κάρτας του χρήστη.
      (Αντίστοιχο με το "card_canvas.create_text(...)" του Python.)
    */
    async loadCard() {
      this.loading = true;

      try {
        // 🟦 ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        const data = await getCard(); // 🔹 χρησιμοποιεί το api.js

        if (data.success) {
          // Ενημερώνουμε τοπικά τα δεδομένα της κάρτας
          this.card = data.card;
          console.log("Card data loaded:", data.card);
        } else {
          alert(data.message || "Failed to load card data.");
        }
      } catch (error) {
        console.error("Error loading card:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    /*
      Εναλλάσσει την κατάσταση κάρτας (freeze/unfreeze),
      αντίστοιχο με τις Python συναρτήσεις freeze_card() / unfreeze_card().
    */
    async toggleFreeze() {
      if (!this.card) return;

      const confirmAction = confirm(
        this.card.isFrozen
          ? "Are you sure you want to unfreeze your card?"
          : "Are you sure you want to freeze your card?"
      );
      if (!confirmAction) return;

      this.loading = true;
      try {
        // 🟦 ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        const data = await toggleCardFreeze(!this.card.isFrozen); // 🔹 api.js function

        if (data.success) {
          // Αν επιτυχής ενημέρωση backend, αλλάζουμε την κατάσταση στο UI
          this.card.isFrozen = !this.card.isFrozen;
          alert(
            this.card.isFrozen
              ? "Your card has been frozen successfully."
              : "Your card has been unfrozen successfully."
          );
        } else {
          alert(data.message || "A problem occurred. Please try again later.");
        }
      } catch (error) {
        console.error("Error toggling freeze:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<!-- Δεν χρειάζεται style — θα προστεθεί από το άλλο μέλος -->
