<template>
  <section>
    <h2>Settings</h2>
    <form @submit.prevent="saveSettings">
      <label>
        Preferred Currency:
        <select v-model="currency">
          <option>EUR</option>
          <option>USD</option>
        </select>
      </label>
      <label>
        Notifications:
        <input type="checkbox" v-model="notifications" />
      </label>
      <button type="submit">Save</button>
    </form>
  </section>
</template>

<script>
export default {
  name: "SettingsView",

  data() {
    return {
      currency: "EUR",
      notifications: true
    };
  },

  methods: {
    saveSettings() {
      /*
        Placeholder:
        - Αποθηκεύει τοπικά τις ρυθμίσεις
        - Αργότερα θα γίνει axios.post('/api/settings')
      */
      console.log("Settings saved:", {
        currency: this.currency,
        notifications: this.notifications
      });
      alert("Settings saved (mock)");
    }
  }
};
</script>
