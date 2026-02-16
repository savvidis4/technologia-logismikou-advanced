<template>
  <!-- Λογικά εδώ θα μπει ο κώδικας του Λάμπρου -->

  <div>
    <header class="header">
        <img src="/logo.png" alt="bank logo" class="img"/>
        <h2 class="logo">Bank of University of West Attica e-Banking</h2>
    </header>

    <div class="register_container">
       <h2>Create New Account</h2>

       <form @submit.prevent="registerUser">
          <div class="input_row">
            <p class="input_label1">Enter New Email</p>
            <input type="email" v-model="email" placeholder="E-mail" required>
          </div>

          <div class="input_row password_row">
            <p class="input_label2">Enter New Password</p>
            <input :type="showPassword1 ? 'text' : 'password'" v-model="password" placeholder="Password" required />
            
            <span class="trigger" @click="showPassword1 = !showPassword1">
              <img :src="showPassword1 ? '/show (1).png' : '/hide (1).png'" :alt="showPassword1 ? 'show' : 'hide'" class="show_pswd"/>
            </span>
          </div>

          <div class="input_row password_row">
            <p class="input_label2">Verify New Password</p>
            <input :type="showPassword2 ? 'text' : 'password'" v-model="ver_password" placeholder="Password" required />
              
            <span class="trigger" @click="showPassword2 = !showPassword2">
              <img :src="showPassword2 ? '/show (1).png' : '/hide (1).png'" :alt="showPassword2 ? 'show' : 'hide'" class="show_pswd"/>
            </span>
          </div>


          <button type="submit" class="register" :disabled="loading">
            {{ loading ? "Creating Account..." : "Register" }}
          </button>
        
          <p class="login_link">
            Already have an account?
            <router-link to="/login">Log in </router-link>
          </p>
        </form>
    </div>

    <img src="/pada1.webp" alt="background" class="pada_img"/>
  </div>




  <!--
  <section>
    <h2>Create Account</h2>

    <form @submit.prevent="registerUser">
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
      <input
        type="password"
        v-model="ver_password"
        placeholder="Verify Password"
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
  -->
</template>

<script>
import { register } from "../services/api.js";

export default {
  name: "RegisterView",

  data() {
    return {
      email: "",
      password: "",
      ver_password: "",
      loading: false,
      // ΛΑΜΠΡΟΣ: Δική μου προσθήκη για να μπορούν να φαίνονται οι κωδικοί αν θέλει ο χρήστης
      showPassword1: false,
      showPassword2: false
    };
  },

  methods: {
    async registerUser() {
      if (!this.ver_password || !this.email || !this.password) {
        alert("Please fill in all fields.");
        return;
      }

      this.loading = true;

      try {
        // Κλήση στο Flask backend μέσω api.js
        const data = await register(this.email, this.password, this.ver_password);

        console.log("Registration response:", data);

        if (!data.success) {
          alert(data.message);
          return;
        }

        // Έλεγχος μόνο για success (χωρίς message)
        if (data.success) {
          alert("Account created successfully!");
          // Μετάβαση στη sign-in
          this.$router.push("/login");
        } else {
          alert(data.message || "Registration failed. Try again.");
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

<style scoped>
@import "../assets/register_style.css";
</style>
