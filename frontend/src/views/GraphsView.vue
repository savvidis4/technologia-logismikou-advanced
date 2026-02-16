<template>

  <div>
    <header class="header">
      <img src="/logo.png" alt="bank logo" class="img">
      <h2 class="logo">Bank of University of West Attica e-Banking</h2>
      <router-link to="/settings" class="settings" style="text-decoration: none;">
        <img src="/settings.png" alt="settings" class="settings_icon">
        <span class="tooltip">User Settings</span>
      </router-link>
      
      <button class="logout" @click="handleLogout()"><span>Log Out</span></button>
    </header>

    <div class="body_top">
      <h2 class="title">Graphs</h2>
      <router-link to="/home" class="exit">
        <img src="/exit.png" alt="exit">
      </router-link>
    </div>

    <section class="container">
        <div class="layout">
            <button class="arrow ar_prev" @click="prevSlide"> < </button>   

            <div class="slider_wrapper">
                <div v-if="loading" class="loading_box">Loading charts...</div>

                <div v-else class="slider_content">
                    
                    <div v-if="currentSlide === 0" class="chart_slide">
                        <h3>Transactions per Month</h3>
                        <div class="canvas_container">
                            <Bar v-if="countChartData" :data="countChartData" :options="chartOptions" />
                        </div>
                    </div>

                    <div v-if="currentSlide === 1" class="chart_slide">
                        <h3>Spending Distribution</h3>
                        <div class="canvas_container">
                            <Pie v-if="pieChartData" :data="pieChartData" :options="pieOptions" />
                        </div>
                    </div>

                    <div v-if="currentSlide === 2" class="chart_slide">
                        <h3>Cash Flow (In vs Out)</h3>
                        <div class="canvas_container">
                            <Bar v-if="inOutChartData" :data="inOutChartData" :options="chartOptions" />
                        </div>
                    </div>

                </div>
            </div>

            <button class="arrow ar_next" @click="nextSlide"> > </button>
        </div>

        <div class="slider_nav">
            <div class="dot" :class="{ active: currentSlide === 0 }" @click="currentSlide = 0"></div>
            <div class="dot" :class="{ active: currentSlide === 1 }" @click="currentSlide = 1"></div>
            <div class="dot" :class="{ active: currentSlide === 2 }" @click="currentSlide = 2"></div>
        </div>
    </section>

  </div>

  <!-- 
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
  -->
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getGraphsData } from '@/services/api';
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';
import { useRouter } from 'vue-router';




// Εγγραφή των components του Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

// ΛΑΜΠΡΟΣ: ΠΡΟΣΘΗΚΗ ΓΙΑ Logout
const router = useRouter();
const loading = ref(true);
const countChartData = ref(null);
const pieChartData = ref(null);
const inOutChartData = ref(null);
// ΛΑΜΠΡΟΣ: ΠΡΟΣΘΗΚΗ ΓΙΑ slider ΣΤΑ ΓΡΑΦΗΜΑΤΑ
const currentSlide = ref(0);
const totalSlides = 3;

const chartOptions = { 
  responsive: true, 
  maintainAspectRatio: false // <--- ΑΥΤΟ ΕΙΝΑΙ ΤΟ ΚΛΕΙΔΙ
};
const pieOptions = { responsive: true, maintainAspectRatio: false };

// ΛΑΜΠΡΟΣ: Logic για το Slider
const nextSlide = () => {
    currentSlide.value = (currentSlide.value + 1) % totalSlides;
};

const prevSlide = () => {
    currentSlide.value = (currentSlide.value - 1 + totalSlides) % totalSlides;
};

// ΛΑΜΠΡΟΣ: ΛΕΙΤΟΥΡΓΙΑ Logout
const handleLogout = () => {
    router.push("/login");
};

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

@import "../assets/graph_style.css";

.layout {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.slider_wrapper {
    width: 60%;
    background: rgb(255, 255, 255);
    padding: 10px;
    border-radius: 15px;
    min-height: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.canvas_container {
    width: 100%;
    height: 380px;
    background-color: rgba(255, 255, 255, 0);
    border-radius: 18px;
}

.slider_nav {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 20px;
}

.dot {
    width: 12px;
    height: 12px;
    background: #ccc;
    border-radius: 50%;
    cursor: pointer;
}

.dot.active { 
  background: white; 
}

/* Styles για τα βέλη (από το δικό σου CSS) */
.arrow {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: white;
}

h3 {
  text-align: center;
  margin-bottom: 10px;
  color: black;
}

.chart-box {
  background: rgb(134, 134, 134);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  min-height: 300px;
}


/*
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
  /*width: 100%;
}
*/

</style>