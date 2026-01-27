<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->
  <section>
    <h2>User Settings</h2>

    <!-- Κάθε κουμπί σε οδηγεί στο αντίστοιχο Vue component -->
    <button @click="goToChangePassword">Change Password</button>
    <button @click="goToChangePin">Change PIN</button>
    <button @click="goToChangeEmail">Change Email</button>

    <!-- Κουμπί για επιστροφή στο home -->
    <button @click="goBack">⬅ Back</button>
  </section>
</template>

<script>
export default {
  name: "SettingsView",

  methods: {
    /*
      Τα methods αυτά απλά κάνουν routing.
      Δεν έχουν backend λογική.
      Δεν χρειάζονται API calls.
    */

    goToChangePassword() {
      // Πηγαίνει στο component ChangePasswordView.vue
      this.$router.push("/change_password");
    },

    goToChangePin() {
      // Πηγαίνει στο component ChangePinView.vue
      this.$router.push("/change_pin");
    },

    goToChangeEmail() {
      // Πηγαίνει στο component ChangeEmailView.vue
      this.$router.push("/change_email");
    },

    goBack() {
      // Επιστροφή στο home screen (ή όπου έχεις ορίσει)
      this.$router.push("/home");
    }
  }
};
</script>
