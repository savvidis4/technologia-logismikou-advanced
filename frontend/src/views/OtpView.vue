<template>
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

  mounted() {
    openOtp();
    console.log("Done Get Method")
  },

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
          this.$router.push("/settings")
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