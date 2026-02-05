<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
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
    }
  }
};
</script>
