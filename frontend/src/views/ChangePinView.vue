<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->

  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <button class="settings" @click="goHome">
        <img src="/home_1.png" alt="settings" class="settings_icon">
        <span class="tooltip">Home</span>
      </button>
        
        <button class="logout" @click="goToLogout()"><span>Log Out</span></button>
    </header>

    <section class="container">
      <div class="email_top">
        <h2>Change Card PIN</h2> 
            
        <div class="exit" @click="goBack" style="cursor: pointer;">
          <img src="/exit.png" alt="exit">
        </div>
      </div>

      <form class="email_form" @submit.prevent="submitPinChange">
        <div class="form_group1">
          <label>Old PIN</label>
          <input type="password" v-model="oldPin" placeholder="Enter old PIN" required>
        </div>

        <div class="form_group1">
          <label>New PIN</label>
          <input type="password" v-model="newPin" placeholder="Enter new PIN" required>
        </div>

        <div class="form_group2">
          <label>Verify New PIN</label>
          <input type="password" v-model="confirmPin" placeholder="Verify new PIN" required>
        </div>

        <button class="change_btn" :disabled="loading">
          {{ loading ? "Processing..." : "Change PIN" }}
        </button>
      </form>
    </section>
  </div>

  <!-- 
  <section>
    <h2>Change Card PIN</h2>

    // Φόρμα αλλαγής PIN 
    <form @submit.prevent="submitPinChange">
      
      <input
        type="password"
        v-model="oldPin"
        placeholder="Old PIN"
        required
      />

      <input
        type="password"
        v-model="newPin"
        placeholder="New PIN (4 digits)"
        required
      />

      <input
        type="password"
        v-model="confirmPin"
        placeholder="Confirm New PIN"
        required
      />

      <button type="submit" :disabled="loading">
        {{ loading ? "Processing..." : "Change PIN" }}
      </button>

    </form>

    // Κουμπί Back 
    <button @click="goBack">⬅ Back</button>

  </section>
  -->
</template>

<script>
// Εισάγουμε τη συνάρτηση από το api.js
import { changePin } from "../services/api.js";

export default {
  name: "ChangePinView",

  data() {
    return {
      oldPin: "",
      newPin: "",
      confirmPin: "",
      loading: false // Flag για ένδειξη φόρτωσης
    };
  },

  methods: {
    /*
      validatePinFormat()
      --------------------
      Ελέγχει αν το PIN:
      - έχει μήκος 4
      - αποτελείται ΜΟΝΟ από ψηφία
    */
    validatePinFormat(pin) {
      const isFourDigits = /^\d{4}$/.test(pin); // regex: ακριβώς 4 digits
      return isFourDigits;
    },

    /*
      submitPinChange()
      -----------------
      Κύρια συνάρτηση αλλαγής PIN.
      Περιλαμβάνει:
      - έλεγχο δεδομένων
      - validation νέου PIN
      - επικοινωνία με backend
      - ενημέρωση χρήστη
    */
    async submitPinChange() {
      // 1) Έλεγχος κενών πεδίων
      if (!this.oldPin || !this.newPin || !this.confirmPin) {
        alert("Please fill in all fields.");
        return;
      }

      // 2) Τα δύο νέα PIN πρέπει να ταιριάζουν
      if (this.newPin !== this.confirmPin) {
        alert("The PINs you entered do not match.");
        return;
      }

      // 3) Validation: το νέο PIN πρέπει να είναι 4 ψηφία
      if (!this.validatePinFormat(this.newPin)) {
        alert("PIN must be exactly 4 digits (0–9).");
        return;
      }

      // 4) Ενεργοποίηση ένδειξης φόρτωσης
      this.loading = true;
      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        /*
          Η συνάρτηση changePin() στο api.js στέλνει:
            POST /api/change_pin
          με body:
            { old_pin, new_pin }

          Το Flask αναμένεται να επιστρέψει:
            { success: true, message: "PIN updated" }
        */
        const data = await changePin(this.oldPin, this.newPin, this.confirmPin);
        console.log("Response from server:", data);

        if (data.success) {
          alert(data.message || "PIN changed successfully!");
          this.$router.push("/settings"); // Επιστροφή στο Settings
        } else {
          alert(data.message || "PIN change failed.");
        }

      } catch (error) {
        console.error("Error during PIN change:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    // Κουμπί επιστροφής
    goBack() {
      this.$router.push("/settings");
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
    },

    goHome() {
      // Επιστροφή στο home screen (ή όπου έχεις ορίσει)
      this.$router.push("/home");
    }
  }
};
</script>


<style scoped>
@import "../assets/change_pin_style.css";
</style>