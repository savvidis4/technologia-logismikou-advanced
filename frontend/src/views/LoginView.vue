<template>
  <!-- Λογικά εδώ θα μπει ο κώδικας του Λάμπρου -->
  <div>
    
    <!-- HEADER -->
    <header class="header">
        <img src="/logo.png" alt="bank logo" class="img"/>
        <h2 class="logo">Bank of University of West Attica e-Banking</h2>

        <router-link to="/register" class="register_btn">

          <img src="/register.png" alt="register_icon" class="register_icon"/>
          <span>Create Account</span>
        </router-link>
    </header>

    <!-- ΚΟΥΤΙ LOGIN -->
     <div class="login_container">
        <h2>Welcome</h2>

        <!-- EIMAIL FIELD -->
        <form @submit.prevent="loginUser">
            <div class="input_row">
                <p class="input_label1">Enter Email</p>
                <input type="text" v-model="email" placeholder="E-mail" required />
            </div>

        <!-- PASSWORD FIELD -->
         <div class="input_row">
           <p class="input_label2">Enter Password</p>
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="password" 
              placeholder="Password" 
              required 
            />

            <!-- Show / Hide password -->
             <span class="trigger" @click="togglePassword">
                <img 
                :src="showPassword ? 'show (1).png' : 'hide (1).png'" 
                :alt="showPassword ? 'show' : 'hide'" 
                class="show_pswd"
                />
              </span>
          </div>

          <p class="forgot">
            <router-link to="/forgot_password">Forgot Password?</router-link>
          </p>

           <button type="submit" class="login" :disabled="loading">
              {{ loading ? "Logging in..." : "Log In" }}
           </button>
        </form>
      </div>

      <img src="/pada1.webp" alt="background" class="pada_img" />
  </div>
  <!-- ΕΔΩ ΤΕΛEΙΩΝΕΙ Ο ΚΩΔΙΚΑΣ ΛΑΜΠΡΟΥΚΟΥ -->

<!-- 
  <section>
    <h2>Sign In PANEEEE</h2>

    
    <form @submit.prevent="loginUser">
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
        {{ loading ? "Logging in..." : "Log In" }}
      </button>
    </form>

    <p>
      Don’t have an account?
      <router-link to="/register">Sign Up</router-link>
    </p>
  </section> -->
</template>

<script>
// Εισάγωγή της συνάρτησης login() από το api.js
import router from "@/router/index.js";
import { login } from "../services/api.js";

//Το export default { ... } 
// είναι η “περιγραφή” του Vue component — πώς λέγεται, τι δεδομένα κρατάει και τι κάνει.
//Π.χ να δηλωσω στο router κατι απο αυτο το component
export default {
  name: "LoginView",

  data() {
    return {
      email: "",      // Τιμή από το πεδίο email (μέσω v-model)
      password: "",   // Τιμή από το πεδίο password
      loading: false  // Flag που αποτρέπει πολλαπλά clicks
    };
  },

  methods: {
    /*
      loginUser()
      -----------------
      Η βασική συνάρτηση που εκτελείται όταν ο χρήστης πατήσει "Log In".

      Περιλαμβάνει:
      Έλεγχο input (όλα τα πεδία πρέπει να είναι συμπληρωμένα)
      Κλήση στο Flask backend μέσω της συνάρτησης login() του api.js
      Ανάλυση της απάντησης (token / μήνυμα)
      Αποθήκευση token στο localStorage
      Μετάβαση στο κύριο dashboard (π.χ. Transfers)
    */

    async loginUser() {
      
      // Έλεγχος δεδομένων
      if (!this.email || !this.password) {
        alert("Please fill in both fields.");
        return;
      }

      // Ενεργοποιούμε ένδειξη φόρτωσης
      this.loading = true;
      console.log("Attempting login with:", this.email, this.password);

      try {

        // Κληση μεθοδους login απο το api.js
        // Εδώ γίνεται το actual request προς το backend
        const data = await login(this.email, this.password);
        console.log("Received login response:", data);
        // Έλεγχος της απάντησης
        if (data.success) {
          console.log("Login successful:", data);

          // Αποθήκευση του token στο localStorage
          localStorage.setItem("token", data.token);

          // Μήνυμα επιβεβαίωσης
          alert(data.message || "Login successful!");

          // Μετάβαση στο Transfers (ή Home screen)
          this.$router.push("/home");
        } else {
          // Αν ο server επέστρεψε αποτυχία (λάθος email/κωδικός)
          console.warn("Login failed:", data.message);
          alert(data.message || "Invalid credentials.");
        }
      } catch (error) {
        // Αν προκύψει σφάλμα επικοινωνίας (server down, timeout, κ.λπ.)
        console.error("Error during login:", error);
        alert("Error connecting to server.");
      } finally {
        // Επαναφορά του κουμπιού φόρτωσης
        this.loading = false;
      }
    }
  }
};
</script>
