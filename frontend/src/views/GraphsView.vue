<template>
  <div class="graphs-container">
    <h1>Account Graphs (Euro €)</h1>
    
    <div v-if="loading">Loading charts...</div>

    <div v-else class="charts-grid">
      
      <div class="chart-box">
        <h3>Transactions per Month</h3>
        <div class="canvas-container">
            <Bar v-if="countChartData" :data="countChartData" :options="chartOptions" />
        </div>
      </div>

      <div class="chart-box">
        <h3>Transaction Type Distribution</h3>
        <div class="canvas-container">
            <Pie v-if="pieChartData" :data="pieChartData" :options="pieOptions" />
        </div>
      </div>

      <div class="chart-box full-width">
        <h3>Money In/Out per Month</h3>
        <div class="canvas-container">
            <Bar v-if="inOutChartData" :data="inOutChartData" :options="chartOptions" />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getGraphsData } from '@/services/api';
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';




// Εγγραφή των components του Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

const loading = ref(true);
const countChartData = ref(null);
const pieChartData = ref(null);
const inOutChartData = ref(null);

const chartOptions = { 
  responsive: true, 
  maintainAspectRatio: false // <--- ΑΥΤΟ ΕΙΝΑΙ ΤΟ ΚΛΕΙΔΙ
};
const pieOptions = { responsive: true, maintainAspectRatio: false };

onMounted(async () => {
  try {
    const data = await getGraphsData();

    // 1. Transactions Count Data
    countChartData.value = {
      labels: data.count_chart.labels,
      datasets: [{
        label: 'Count',
        data: data.count_chart.data,
        backgroundColor: '#1976d2'
      }]
    };

    // 2. Pie Chart Data
    pieChartData.value = {
      labels: data.pie_chart.labels,
      datasets: [{
        data: data.pie_chart.data,
        backgroundColor: ['#1976d2', '#2e7d32', '#fbc02d'] // Χρώματα
      }]
    };

    // 3. In/Out Data
    inOutChartData.value = {
      labels: data.bar_in_out.labels,
      datasets: data.bar_in_out.datasets // Έρχεται έτοιμο με χρώματα από το backend
    };

  } catch (error) {
    console.error("Error loading graphs:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
h3 {
  text-align: center;
  margin-bottom: 10px;
  color: black;
}
.graphs-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.full-width {
  grid-column: span 2;
}
.chart-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  min-height: 300px;
}
.canvas-container {
  position: relative;
  height: 300px; /* Ή όσο ύψος θέλεις να έχει το γράφημα */
  width: 100%;
}
</style>