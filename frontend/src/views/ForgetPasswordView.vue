<template>
  <section>
    <h2>Forgot Password</h2>

    <p>Please enter your email address to reset your password.</p>

    <form @submit.prevent="submitEmail">
      <input
        type="text"
        v-model="email"
        placeholder="Enter your email"
        required
      />

      <button type="submit" :disabled="loading">
        {{ loading ? "Sending..." : "Send Reset Link" }}
      </button>
    </form>
  </section>
</template>

<script>
import { forgotPassword } from "../services/api.js";

export default {
  name: "ForgetPasswordView",

  data() {
    return {
      email: "",
      loading: false
    };
  },

  methods: {
    async submitEmail() {
      //Έλεγχος κενής τιμής
      if (!this.email) {
        alert("Please enter your email.");
        return;
      }

      //Βασικός έλεγχος σωστής μορφής email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        alert("Please enter a valid email address (example@domain.com).");
        return;
      }

      //Loading για να μην γίνει διπλό submit
      this.loading = true;

      try {
        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        const data = await forgotPassword(this.email);

        if (data.success) {
          alert("If this email exists, reset instructions were sent.");
          this.email = "";

          // Προαιρετικά: αν θέλετε να πάει σε OTP view
          this.$router.push("/otp");
        } else {
          alert("Request failed. Please try again.");
        }
      } catch (error) {
        console.error("Forgot password error:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>