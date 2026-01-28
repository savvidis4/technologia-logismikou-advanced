<template>
  <section>
    <h2>Verify Email</h2>

    <p>Please enter the 6-digit code sent to your email.</p>

    <form @submit.prevent="verifyOtp">
      <input
        type="text"
        v-model="otp"
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
import { verifyOtp } from "../services/api.js";

export default {
  name: "VerifyOtpView",

  data() {
    return {
      otp_code: "",        // Ο κωδικός OTP που εισάγει ο χρήστης
      loading: false       // Flag για να μπλοκάρει πολλαπλά submits
    };
  },

  methods: {

    async verifyOtpCode() {
      // Έλεγχος κενού
      if (!this.otp) {
        alert("Please enter the OTP code.");
        return;
      }

      // Έλεγχος μήκους (6 ψηφία)
      if (this.otp.length !== 6) {
        alert("OTP must be exactly 6 digits.");
        return;
      }

      // Έλεγχος ότι είναι μόνο αριθμοί
      if (!/^\d{6}$/.test(this.otp)) {
        alert("OTP must contain only numbers.");
        return;
      }

      // Ενεργοποίηση loading
      this.loading = true;
      console.log("Verifying OTP:", this.otp);

      try {

        // ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND μέσω verifyOtp()
        
        const data = await verifyOtp(this.otp);

        if (data.success) {
          alert("OTP verified successfully.");

          // ΕΔΩ μελλοντικά:
          // this.$router.push("/settings")
          // ή ολοκλήρωση change-email flow
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