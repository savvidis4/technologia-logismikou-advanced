<template>

  <div class="forgot_wrapper">
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
    </header>

    <div class="forgot_container">
      <h2>Forgot Password</h2>
      <form @submit.prevent="submitEmail">
        <div class="input_row">
          <p class="input_label1">Enter your Email</p>
          <input type="text" v-model="email" placeholder="E-mail" required>
        </div>

        <button type="submit" class="verify" :disabled="loading">
          {{ loading ? "Sending..." : "Verify Email" }}
        </button>

        <router-link to="/login" class="return" style="text-decoration: none; display: flex; align-items: center; justify-content: center; cursor: pointer;">
            <img src="/back.png" alt="return" class="return_icon">
            <span>Back</span>
        </router-link>

        <!-- 
        <div class="return" onclick="window.location.href='login.html'">
          <img src="back.png" alt="return" class="return_icon">
          <span>Back</span>
        </div>
        -->
      </form>
    </div>

    <img src="/pada1.webp" alt="background" class="pada_img">
  </div>



  <!--
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
  -->
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

<style scoped>
@import "../assets/forgot_pass_style.css";
</style>