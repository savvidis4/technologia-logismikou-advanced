<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Change Email</h2>

    <!-- STEP 1: Old Email, New Email, Confirm New Email -->
    <div v-if="step === 1">
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

      <button @click="submitEmailChangeStep1" :disabled="loading">
        {{ loading ? "Processing..." : "Send OTP" }}
      </button>
    </div>

    <!-- STEP 2: OTP Verification -->
    <div v-if="step === 2">
      <p>Please enter the One-Time Password sent to your new email:</p>

      <input
        type="text"
        v-model="otp"
        placeholder="Enter OTP"
      />

      <button @click="submitEmailChangeStep2" :disabled="loading">
        {{ loading ? "Checking..." : "Verify OTP" }}
      </button>

      <button @click="goBackToSettings">
        Cancel
      </button>
    </div>

    <!-- STEP 3: Success -->
    <div v-if="step === 3">
      <h3>Success!</h3>
      <p>Your email was successfully changed to: {{ newEmail }}</p>

      <button @click="goBackToSettings">Back</button>
    </div>
  </section>
</template>

<script>
import { requestEmailChange, verifyEmailOTP } from "../api/api.js";

export default {
  name: "ChangeEmailView",

  data() {
    return {
      step: 1,

      oldEmail: "",
      newEmail: "",
      confirmNewEmail: "",

      otp: "",
      
      loading: false
    };
  },

  methods: {
    /*
      STEP 1:
      -----------------------
      Validation όπως στο desktop app.
      Καλούμε backend για OTP.
    */
    async submitEmailChangeStep1() {
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
        const data = await requestEmailChange(this.oldEmail, this.newEmail);

        if (data.success) {
          // Πάμε στο βήμα OTP
          this.step = 2;
        } else {
          alert(data.message || "Email change request failed.");
        }
      } catch (error) {
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    },

    /*
      STEP 2:
      -----------------------
      Ο χρήστης δίνει το OTP.
      Το backend ελέγχει:
      - αν το OTP ταιριάζει
      - αν ναι → αλλάζει email → success
    */
    async submitEmailChangeStep2() {
      if (!this.otp) {
        alert("Please enter the OTP.");
        return;
      }

      this.loading = true;

      try {
        const data = await verifyEmailOTP(this.otp);

        if (data.success) {
          // OTP correct → backend already changed email
          this.step = 3;
        } else {
          alert("Wrong OTP. Please try again.");
        }

      } catch (error) {
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
