<template>
  <!-- Λογικά εδώ θα μπει ο κώδικας του Λάμπρου -->
  <section>
    <h2>Create Account</h2>

    <form @submit.prevent="registerUser">
      <input
        type="text"
        v-model="name"
        placeholder="Full Name"
        required
      />
      <input
        type="email"
        v-model="email"
        placeholder="Email"
        required
      />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <button type="submit" :disabled="loading">
        {{ loading ? "Creating Account..." : "Create Account" }}
      </button>
    </form>

    <p>
      Already registered?
      <router-link to="/login">Login</router-link>
    </p>
  </section>
</template>

<script>
import { register } from "../services/api.js";

export default {
  name: "RegisterView",

  data() {
    return {
      name: "",
      email: "",
      password: "",
      loading: false
    };
  },

  methods: {
    async registerUser() {
      if (!this.name || !this.email || !this.password) {
        alert("Please fill in all fields.");
        return;
      }

      this.loading = true;

      try {
        // Κλήση στο Flask backend μέσω api.js
        const data = await register(this.name, this.email, this.password);

        // Έλεγχος μόνο για success (χωρίς message)
        if (data.success) {
          alert("Account created successfully!");
          // Μετάβαση στη sign-in
          this.$router.push("/login");
        } else {
          alert("Registration failed. Try again.");
        }
      } catch (error) {
        console.error("Error during registration:", error);
        alert("Error connecting to server.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

