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
        
      <button class="logout" @click="user_logout()"><span>Log Out</span></button>
    </header>

    <section class="container">
      <div class="email_top">
        <h2>Change E-mail</h2> 
      
        <div class="exit" @click="goBackToSettings">
          <img src="/exit.png" alt="exit">
        </div>
      </div>

      <form class="email_form" @submit.prevent="submitEmailChange">
        <div class="form_group1">
          <label>Old E-mail</label>
          <input type="email" v-model="oldEmail" placeholder="Enter old E-mail" required>
        </div>

        <div class="form_group1">
         <label>New E-mail</label>
          <input type="email" v-model="newEmail" placeholder="Enter new E-mail" required>
        </div>

        <div class="form_group2">
          <label>Verify New E-mail</label>
          <input type="email" v-model="confirmNewEmail" placeholder="Verify new E-mail" required>
        </div>

        <button type="submit" class="change_btn" :disabled="loading">
          {{ loading ? "Processing..." : "Change E-mail"}}
        </button>
      </form>
    </section>
  </div>
  <!-- 
  <section>
    <h2>Change Email</h2>

    <div>
      <input
        type="email"
        v-model="oldEmail"
        placeholder="Old Email"
      />

      <input
        type="email"
        v-model="newEmail"
        placeholder="New Email"
      />

      <input
        type="email"
        v-model="confirmNewEmail"
        placeholder="Confirm New Email"
      />

      <button @click="submitEmailChange" :disabled="loading">
        {{ loading ? "Processing..." : "Change Email" }}
      </button>
    </div>

  </section>
  -->
</template>

<script>
import { emailChange } from "../services/api.js";

export default {
  name: "ChangeEmailView",

  data() {
    return {
      oldEmail: "",
      newEmail: "",
      confirmNewEmail: "",
      
      loading: false
    };
  },

  methods: {

    async submitEmailChange() {
      if (!this.oldEmail || !this.newEmail || !this.confirmNewEmail) {
        alert("Please fill in all fields.");
        return;
      }

      // Emails must match
      if (this.newEmail !== this.confirmNewEmail) {
        alert("The new emails do not match.");
        return;
      }

      // Check email format
      if (!this.newEmail.includes("@") || !this.newEmail.includes(".")) {
        alert("Please use a valid email format.");
        return;
      }

      this.loading = true;

      try {
        // ΕΔΩ ΣΤΕΛΝΕΤΑΙ ΤΟ EMAIL ΜΕ ΤΟΝ OTP (BACKEND ΥΛΟΠΟΙΗΣΗ)
        const data = await emailChange(this.oldEmail, this.newEmail, this.confirmNewEmail);

        if (data.success) {
          alert(data.message || "Email changed successfully!");

          // Μετάβαση πίσω στις ρυθμίσεις
          this.$router.push("/settings");
        } else {
          alert(data.message || "Email change failed.");
        }

      } catch (error) {
        console.error("Error during Email change:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    goBackToSettings() {
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
@import "../assets/change_email_styles.css";
</style>