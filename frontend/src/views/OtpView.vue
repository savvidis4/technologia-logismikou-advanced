<template>

<div class="otp-page">
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <button class="settings" @click="$router.push('/home')">
        <img src="/home_1.png" alt="home" class="settings_icon">
        <span class="tooltip">Home</span>
      </button>
      <button class="logout" @click="handleLogout"><span>Log Out</span></button>
    </header>

    <section class="container">
      <div class="email_top">
        <h2>Verify E-mail</h2> 
        <div class="exit" @click="$router.push('/settings')" style="cursor: pointer;">
          <img src="/exit.png" alt="exit">
        </div>
      </div>

      <form class="email_form" @submit.prevent="verifyOtpCode">
        <div class="form_group1">
          <label>Please enter the 6-digit code sent to your email.</label>
          <input 
            type="text" 
            v-model="otp_code" 
            maxlength="6" 
            pattern="\d*" 
            inputmode="numeric"
            placeholder="******"
            required
          >
        </div>

        <button type="submit" class="change_btn" :disabled="loading">
          <span>{{ loading ? "Verifying..." : "Verify" }}</span>
        </button>
      </form>
    </section>
  </div>

  <!-- 
  <section>
    <h2>Verify Email</h2>

    <p>Please enter the 6-digit code sent to your email.</p>

    <form @submit.prevent="verifyOtpCode">
      <input
        type="text"
        v-model="otp_code"
        placeholder="Enter OTP"
        maxlength="6"
        required
      />
 
      <button type="submit" :disabled="loading">
        {{ loading ? "Verifying..." : "Verify" }}
      </button>
    </form>
  </section>
  -->
</template>
<script>
import { otp } from "../services/api.js";
import { openOtp } from "../services/api.js";

export default {
  name: "OtpView",

  data() {
    return {
      otp_code: "",        // Ο κωδικός OTP που εισάγει ο χρήστης
      loading: false       // Flag για να μπλοκάρει πολλαπλά submits
    };
  },

  async mounted() {
  try {
    console.log("Attempting to trigger OTP email...");
    await openOtp(); // Περιμένουμε την απάντηση από το Flask
    console.log("OTP Request sent successfully to backend");
  } catch (error) {
    console.error("The backend failed to send the email:", error);
  }
},

  /*
  mounted() {
    openOtp();
    console.log("Done Get Method")
  },
  */

  methods: {

    async verifyOtpCode() {
      // Έλεγχος κενού
      if (!this.otp_code) {
        alert("Please enter the OTP code.");
        return;
      }

      // Έλεγχος μήκους (6 ψηφία)
      if (this.otp_code.length !== 6) {
        alert("OTP must be exactly 6 digits.");
        return;
      }

      // Έλεγχος ότι είναι μόνο αριθμοί
      if (!/^\d{6}$/.test(this.otp_code)) {
        alert("OTP must contain only numbers.");
        return;
      }

      // Ενεργοποίηση loading
      this.loading = true;
      console.log("Verifying OTP:", this.otp_code);

      try {

        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND μέσω verifyOtp()
        
        const data = await otp(this.otp_code);
        console.log(this.otp_code)
        if (data.success) {
          alert("OTP verified successfully.");

          // ΕΔΩ μελλοντικά:
          this.$router.push("/change_email")
        } else {
          alert(data.message || "Invalid or expired OTP.");
        }

      } catch (error) {
        console.error("OTP verification error:", error);
        alert("Error connecting to server.");
      } finally {
        // Απενεργοποίηση loading
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
@import "../assets/otp_style.css";
</style>