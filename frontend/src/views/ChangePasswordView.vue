<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->

  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <button class="settings" @click="goHome()">
        <img src="/home_1.png" alt="settings" class="settings_icon">
        <span class="tooltip">Home</span>
      </button>
      <button class="logout" @click="goToLogout()"><span>Log Out</span></button>
    </header>

    <section class="container">
      <div class="email_top">
        <h2>Change Password</h2> 
        <div class="exit" @click="goBack()" style="cursor: pointer;">
          <img src="/exit.png" alt="exit">
        </div>
      </div>

      <form class="email_form" @submit.prevent="submitPasswordChange">
        <div class="form_group1">
          <label>Old password</label>
          <input type="password" v-model="oldPassword" placeholder="Enter old password" required>
        </div>

        <div class="form_group1">
          <label>New password</label>
          <input type="password" v-model="newPassword" placeholder="Enter new password" required>
        </div>

        <div class="form_group2">
          <label>Verify New password</label>
          <input type="password" v-model="confirmPassword" placeholder="Verify new password" required>
        </div>

        <button type="submit" class="change_btn" :disabled="loading">
          {{ loading ? "Processing..." : "Change Password"}}
        </button>
      </form>
    </section>
  </div>

  <!-- 
  <section>
    <h2>Change Password</h2>

    // Φόρμα αλλαγής password 
    <form @submit.prevent="submitPasswordChange">
      
      <input
        type="password"
        v-model="oldPassword"
        placeholder="Old Password"
        required
      />

      <input
        type="password"
        v-model="newPassword"
        placeholder="New Password"
        required
      />

      <input
        type="password"
        v-model="confirmPassword"
        placeholder="Confirm New Password"
        required
      />

      <button type="submit" :disabled="loading">
        {{ loading ? "Processing..." : "Change Password" }}
      </button>

    </form>

    // Κουμπί Back 
    <button @click="goBack">⬅ Back</button>

  </section>
  -->
</template>

<script>
// Εισάγουμε τη συνάρτηση από το api.js
import { changePassword } from "../services/api.js";

export default {
  name: "ChangePasswordView",

  data() {
    return {
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
      loading: false  // Ενδειξη ότι η διαδικασία τρέχει
    };
  },

  methods: {
    /*
      FRONTEND VALIDATION
      ----------------------
      Αντιστοιχεί στο check_pass() + validation της Python έκδοσης.
    */
    validatePasswordFormat(password) {
      const hasUpper = /[A-Z]/.test(password);
      const hasNumber = /\d/.test(password);
      const hasSymbol = /[!@?#$%*]/.test(password);
      const longEnough = password.length >= 8;

      return hasUpper && hasNumber && hasSymbol && longEnough;
    },

    /*
       submitPasswordChange()
      -------------------------
      Η κύρια συνάρτηση αλλαγής password.
      Περιλαμβάνει:
      - Έλεγχο δεδομένων
      - Validation νέου κωδικού
      - Κλήση στο Flask backend
      - Επεξεργασία απάντησης
    */
    async submitPasswordChange() {
      // 1) Έλεγχος κενών πεδίων
      if (!this.oldPassword || !this.newPassword || !this.confirmPassword) {
        alert("Please fill in all fields.");
        return;
      }

      // 2) Τα δύο νέα passwords πρέπει να ταιριάζουν
      if (this.newPassword !== this.confirmPassword) {
        alert("The new passwords do not match.");
        return;
      }

      // 3) Έλεγχος ασφάλειας νέου password
      if (!this.validatePasswordFormat(this.newPassword)) {
        alert(
          "Password must contain:\n- at least 8 characters\n- a capital letter\n- a number\n- a symbol (!,@,?,#,...)"
        );
        return;
      }

      // 4) Ενεργοποιούμε loading
      this.loading = true;

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND
        const data = await changePassword(this.oldPassword, this.newPassword, this.confirmPassword);

        if (data.success) {
          alert(data.message || "Password changed successfully!");

          // Μετάβαση πίσω στις ρυθμίσεις
          this.$router.push("/settings");
        } else {
          alert(data.message || "Password change failed.");
        }

      } catch (error) {
        console.error("Error during password change:", error);
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
@import "../assets/change_pass_style.css";
</style>