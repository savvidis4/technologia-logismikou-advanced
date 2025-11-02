<template>
  <section>
    <h2>Graphs</h2>
    <button @click="generateGraph">Generate Sample Graph</button>

    <div v-if="graphData.length">
      <ul>
        <li v-for="(point, i) in graphData" :key="i">
          Month {{ i + 1 }}: {{ point }} €
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
export default {
  name: "GraphsView",

  data() {
    return {
      graphData: []
    };
  },

  methods: {
    generateGraph() {
      /*
        Placeholder:
        - Δημιουργεί ψεύτικα δεδομένα για το γράφημα
        - Αργότερα θα αντικατασταθεί από Flask endpoint
      */
      this.graphData = [500, 600, 550, 700, 800, 750];
      console.log("Mock graph data generated");
    }
  }
};
</script>
