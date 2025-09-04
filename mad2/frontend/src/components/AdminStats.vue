<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Admin Dashboard</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link active" href="/admin/dashboard">Home</a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/stats">Statistics</router-link>
          </li>
          <li class="nav-item">
            <span class="nav-link" @click="exportData" style="cursor: pointer;">Export</span>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
    <div class="container mt-5">
      <h2>Admin Statistics</h2>
      <div class="row mt-4">
        <div class="col-md-4 stat-card">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Total Users</h5>
              <p class="card-text">{{ statsData.total_users }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4 stat-card">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Total Requests</h5>
              <p class="card-text">{{ statsData.total_requests }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4 stat-card">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Total Services Provided</h5>
              <p class="card-text">{{ statsData.total_services_provided }}</p>
            </div>
          </div>
        </div>
      </div>
      <h4 class="chart-container">Approved vs Flagged Users</h4>
      <img :src="'data:image/png;base64,' + statsData.user_status_chart" alt="Approved vs Flagged Users">
      <h4 class="chart-container">Service Statistics</h4>
      <img :src="'data:image/png;base64,' + statsData.bar_chart" alt="Service Stats">
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      statsData: {}
    };
  },
  created() {
    this.fetchStatsData();
  },
  methods: {
    
    async exportData() {
      try {
        const response = await fetch('/api/admin/export', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to create service' };
      }
    },
    async fetchStatsData() {
      try {
        const response = await fetch('/api/admin/stats', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.statsData = data;
      } catch (error) {
        console.error('Error fetching stats data:', error);
      }
    }
  }
};
</script>

<style scoped>
.stat-card {
  margin: 10px 0;
}
.chart-container {
  margin-top: 30px;
}
img {
  width: 100%;
  max-width: 600px;
  height: auto;
}
</style>