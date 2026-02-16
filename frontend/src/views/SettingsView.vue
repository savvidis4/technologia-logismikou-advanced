<template>
  <!-- ΕΔΩ ΣΥΝΔΕΕΤΑΙ ΜΕ FRONTEND -->

  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>

      <button class="home" @click="goBack">
        <img src="/home_1.png" alt="home" class="home_icon">
        <span class="tooltip"> Home</span>
      </button>
        
      <button class="logout" @click="goToLogout()">
        <span>Log Out</span>
      </button>
    </header>

    <div class="body_top">
        <h2 class="title">User Settings</h2>
    </div>

    <main class="settings_main">
      <button class="settings_bar" type="button" @click="goToChangeEmail">
        <span class="bar_left">
          <span class="email_icon"><img src="/mail.png" alt="email"> </span>
          <span class="bar_text">Change E-mail</span>
        </span>
        <span class="bar_arrow"> > </span>
      </button>

      <button class="settings_bar" type="button" @click="goToChangePassword">
        <span class="bar_left">
          <span class="pswd_icon"><img src="/padlock.png" alt="password"> </span>
          <span class="bar_text">Change Password</span>
        </span>
        <span class="bar_arrow"> > </span>
      </button>

      <button class="settings_bar" type="button" @click="goToChangePin">
        <span class="bar_left">
          <span class="pin_icon"><img src="/pin.png" alt="card_pin"></span>
          <span class="bar_text">Change Card PIN</span>
        </span>
        <span class="bar_arrow"> > </span>
      </button>
    </main>
  </div>

  <!-- 
  <section>
    <h2>User Settings</h2>

     Κάθε κουμπί σε οδηγεί στο αντίστοιχο Vue component 
    <button @click="goToChangePassword">Change Password</button>
    <button @click="goToChangePin">Change PIN</button>
    <button @click="goToChangeEmail">Change Email</button>

     Κουμπί για επιστροφή στο home 
    <button @click="goBack">⬅ Back</button>
  </section>
  -->
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
      this.$router.push("/otp");
    },

    goBack() {
      // Επιστροφή στο home screen (ή όπου έχεις ορίσει)
      this.$router.push("/home");
    },

    goToLogout() {
      // Πηγαίνει στο component LogoutView.vue
      this.$router.push("/logout");
    }
  }
};
</script>


<style scoped>
@import "../assets/setting_style.css";
</style>