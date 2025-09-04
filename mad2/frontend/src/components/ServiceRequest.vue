<template>
  <div class="container mt-5">
    <div class="text-center mb-4">
      <h1 class="h3">Available Professionals</h1>
      <p class="text-muted">Service: {{ service.service_title }}</p>
    </div>

    <div v-if="message" :class="`alert alert-${message.category} alert-dismissible fade show`" role="alert">
      {{ message.text }}
      <button type="button" class="btn-close" @click="message = null" aria-label="Close"></button>
    </div>

    <input v-model="searchQuery" type="text" class="form-control mb-3 w-50" 
            placeholder="Search available professionals..." />

    <div class="mb-4">
      <label for="serviceData" class="form-label">Provide Service Details</label>
      <textarea id="serviceData" v-model="serviceData" class="form-control" rows="3" placeholder="Enter additional information about the service..."></textarea>
    </div>

    <div v-if="professionals.length">
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Name</th>
            <th>Experience Level</th>
            <th>Average Rating</th>
            <th>Starting Price</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in filteredProfessionals" :key="professional.username">
            <td>{{ professional.username }}</td>
            <td>{{ professional.professional_experience_level || "Not specified" }}</td>
            <td>{{ professional.average_rating || "No ratings yet" }}</td>
            <td>${{ service.starting_price }}</td>
            <td>
              <button @click="requestService(professional.username)" class="btn btn-primary btn-sm">Request Service</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="alert alert-warning text-center">No professionals are currently available for this service.</div>

    <div class="mt-4">
      <router-link to="/customer/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      service: {},
      professionals: [],
      serviceData: '',
      message: null,
      searchQuery: ""
        };
    },
    computed: {
        filteredProfessionals() {
            return this.professionals.filter(p => 
            p.username.toLowerCase().includes(this.searchQuery.toLowerCase()));
        },
    },
  created() {
    this.fetchServiceData();
  },
  methods: {
    async fetchServiceData() {
      const serviceId = this.$route.params.id;
      try {
        const response = await fetch(`/api/customer/service/${serviceId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.service = data.service;
        this.professionals = data.professionals;
      } catch (error) {
        console.error('Error fetching service data:', error);
      }
    },
    async requestService(professionalUsername) {
      const serviceId = this.$route.params.id;
      if (!this.serviceData.trim()) {
        this.message = { text: 'Please provide service details before requesting.', category: 'warning' };
        return;
      }
      try {
        const response = await fetch(`/api/customer/service/${serviceId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            professional: professionalUsername,
            details: this.serviceData
          })
        });
        const data = await response.json();
        if (response.ok) {
          this.message = { text: data.message, category: 'success' };
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error requesting service:', error);
        this.message = { text: 'An error occurred. Please try again.', category: 'danger' };
      }
    }
  }
};
</script>

<style scoped>
.alert {
  animation: fadeOut 5s ease forwards;
}

@keyframes fadeOut {
  0% { opacity: 1; }
  100% { opacity: 0; visibility: hidden; }
}
</style>
