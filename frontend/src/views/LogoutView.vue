<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>Logout</h2>
    <p>You are being logged out...</p>
  </section>
</template>

<script>
// Εισάγουμε τη συνάρτηση logout από το api.js
import { logout } from "../services/api.js";

export default {
  name: "LogoutView",

  data() {
    return {
      loading: false // Flag για να μην πατηθεί ξανά το κουμπί όσο τρέχει
    };
  },

  async mounted() {
    this.logoutUser();
  },

  methods: {
    /*
      logoutUser()
      -----------------
      Η συνάρτηση αυτή είναι το αντίστοιχο του show_logout_screen() στο Python desktop app.

      Περιλαμβάνει:
       Παράθυρο επιβεβαίωσης
       Κλήση στο Flask backend μέσω του api.js
       Καθαρισμό των αποθηκευμένων δεδομένων
       Επιστροφή στη σελίδα σύνδεσης
    */
    async logoutUser() {
      // Ζητάμε επιβεβαίωση (όπως το messagebox.askyesno στο Python)
      const confirmed = confirm(
        "You are about to be logged out of your account.\nWould you like to proceed?"
      );

      if (!confirmed) {
        console.log("User canceled logout.");
        return; // Τερματισμός χωρίς αποσύνδεση
      }

      // Ενεργοποιούμε την ένδειξη φόρτωσης
      this.loading = true;
      console.log("User logging out...");

      try {
        //ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ BACKEND (Flask)
        /*
          Η συνάρτηση logout() που εισάγεται από το api.js κάνει:
            POST /api/logout
          και διαχειρίζεται το token στο header.

          Επιστρέφει JSON της μορφής:
            { "success": true, "message": "User logged out" }
        */
        const data = await logout(); // Κλήση Flask μέσω api.js

        // Έλεγχος επιτυχίας
        if (data.success) {
          // Αν όλα πήγαν καλά:
          // - καθαρίζουμε το token από το localStorage
          // - ενημερώνουμε τον χρήστη
          // - τον μεταφέρουμε στη σελίδα login
          localStorage.removeItem("token");
          console.log("User logged out successfully:", data);

          alert(data.message || "You have been logged out successfully.");
          this.$router.push("/login"); // Όπως το show_login_screen στο Python
        } else {
          // Αν ο server γύρισε αποτυχία
          console.warn("Logout failed:", data);
          alert(data.message || "Logout failed. Please try again.");
        }
      } catch (error) {
        // Αν προκύψει σφάλμα επικοινωνίας (π.χ. server down)
        console.error("Error during logout:", error);
        alert("Error connecting to server.");
      } finally {
        // Απενεργοποιούμε την ένδειξη φόρτωσης
        this.loading = false;
      }
    }
  }
};
</script>

