<!-- filepath: /home/lakshika/mad2_project/frontend/src/components/AdminDashboard.vue -->
<template>
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
            <a class="nav-link active" href="#">Home</a>
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

  <div class="container mt-4 mb-5">
    <!-- Flash Messages -->
    <div v-if="message" :class="'alert alert-' + message.category" role="alert">
      {{ message.text }}
    </div>

        <!-- Modal for Adding Service -->
        <div v-show="showAddServiceModal" class="card p-3">
      <form @submit.prevent="createService">
        <h4>Create Service</h4>
        <label for="service_title" class="p-2">Service Title:</label>
        <input type="text" v-model="newService.service_title" required class="form-control"/>
        <label for="service_details" class="p-2">Service Details:</label>
        <input type="text" v-model="newService.service_details" required class="form-control"/>
        <label for="starting_price" class="p-2">Starting Price:</label>
        <input type="number" v-model="newService.starting_price" required class="form-control"/>
        <label for="duration_required" class="p-2">Duration Required:</label>
        <input type="text" v-model="newService.duration_required" required class="form-control"/>
        <button type="submit" class="btn btn-primary m-2">Create</button>
        <button type="button" class="btn btn-secondary " @click="closeAddServiceModal">Cancel</button>
      </form>
    </div>

    <!-- Modal for Editing Service -->
    <div v-show="showEditServiceModal" class="card p-3">
      <form @submit.prevent="editService">
        <h4>Edit Service</h4>
        <label for="service_title" class="p-2">Service Title:</label>
        <input type="text" v-model="selectedService.service_title" required class="form-control"/>
        <label for="service_details" class="p-2">Service Details:</label>
        <input type="text" v-model="selectedService.service_details" required class="form-control"/>
        <label for="starting_price" class="p-2">Starting Price:</label>
        <input type="number" v-model="selectedService.starting_price" required class="form-control"/>
        <label for="duration_required" class="p-2">Duration Required:</label>
        <input type="text" v-model="selectedService.duration_required" required class="form-control"/>
        <button type="submit" class="btn btn-primary m-2">Save</button>
        <button type="button" class="btn btn-secondary m-2" @click="closeEditServiceModal">Cancel</button>
      </form>
    </div>

    <!-- Modal for Deleting Service -->
    <div v-show="showDeleteServiceModal" class="card p-3">
      <h4>Are you sure you want to delete this service?</h4>
      <button class="btn btn-danger" @click="deleteService">Delete</button>
      <button class="btn btn-secondary" @click="closeDeleteServiceModal">Cancel</button>
    </div>

    <!-- Services Table -->
    <h3>Services</h3>
    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>Service Name</th>
          <th>Description</th>
          <th>Starting Price</th>
          <th>Duration Required</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td v-if="service">{{ service.service_title }}</td>
          <td v-if="service">{{ service.service_details }}</td>
          <td v-if="service">Rs.{{ service.starting_price }}</td>
          <td v-if="service">{{ service.duration_required }}</td>
          <td v-else>Loading...</td>
          <td>
            <button class="btn btn-primary btn-sm" @click="openEditServiceModal(service)">Edit</button>
            <button class="btn btn-danger btn-sm" @click="openDeleteServiceModal(service)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button class="btn btn-success mt-3" @click="openAddServiceModal">Add Service</button>

    <!-- Requests Table -->
    <h3 class="mt-5">Requests</h3>
    <table class="table table-bordered mt-3">
      <thead class="table-dark">
        <tr>
          <th>Customer Name</th>
          <th>Service Requested</th>
          <th>Professional Assigned</th>
          <th>Date Requested</th>
          <th>Date Closed</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.customer_name }}</td>
          <td>{{ request.service_title }}</td>
          <td>{{ request.professional_name }}</td>
          <td>{{ request.date_requested }}</td>
          <td>{{ request.date_closed }}</td>
          <td>{{ request.status }}</td>
        </tr>
      </tbody>
    </table>

    <h3 class="mt-5">Professionals</h3>
    <table class="table table-bordered mt-3">
      <thead class="table-dark">
        <tr>
          <th>Professional Name</th>
          <th>Experience Level</th>
          <th>Service</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in professionals" :key="professional.id">
          <td>{{ professional.username }}</td>
          <td>{{ professional.professional_experience_level }}</td>
          <td>{{ professional.service_title }}</td>
          <td>{{ professional.approval_status }}</td>
          <td>
            <!-- <button class="btn btn-info btn-sm m-1" @click="viewProfessionalDetails(professional)">View</button> -->
            <button class="btn btn-success btn-sm m-1" @click="approveProfessional(professional.id)" v-if="professional.approval_status === false">Approve</button>
            <button class="btn btn-danger btn-sm m-1" @click="rejectProfessional(professional.id)" v-if="professional.approval_status === false">Reject</button>
            <button class="btn btn-warning btn-sm m-1" @click="blockProfessional(professional.id)" v-if="professional.approval_status === true">Block</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  data() {
    return {
      adminName: '',
      services: [],
      requests: [],
      professionals: [],
      message: null,
      newService: {
        service_title: '',
        service_details: '',
        starting_price: '',
        duration_required: ''
      },
      selectedService: {},
      showAddServiceModal: false,
      showEditServiceModal: false,
      showDeleteServiceModal: false
    };
  },
  mounted() {
    this.fetchAdminData();
  },
  methods: {
    // Fetch admin data (services, requests, unapproved professionals)
    async fetchAdminData() {
      try {
        const response = await fetch('/api/admin/dashboard', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        // const data = await response.json();
        this.adminName = data.admin_name;
        this.services = data.services;
        this.requests = data.requests;
        this.professionals = data.professionals;
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to fetch data' };
      }
    },

    async fetchAdminData() {
      try {
        const response = await fetch('/api/admin/dashboard', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Ensure data is valid before assigning values
        this.adminName = data.admin_name || "Admin";
        this.services = Array.isArray(data.services) ? data.services : [];
        this.requests = Array.isArray(data.requests) ? data.requests : [];
        this.professionals = Array.isArray(data.professionals) ? data.professionals : [];

      } catch (error) {
        console.error("Failed to fetch data:", error);
        this.message = { category: 'danger', text: 'Failed to fetch data' };
        this.services = [];
        this.requests = [];
        this.professionals = [];
      }
    },


    // Approve a professional
    async approveProfessional(professionalId) {
      try {
        const response = await fetch(`/api/admin/approve_professional/${professionalId}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
        this.fetchAdminData();
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to approve professional' };
      }
    },

    // Reject a professional
    async rejectProfessional(professionalId) {
      try {
        const response = await fetch(`/api/admin/reject_professional/${professionalId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
        this.fetchAdminData();
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to reject professional' };
      }
    },

    // Block a professional
    async blockProfessional(professionalId) {
      try {
        const response = await fetch(`/api/admin/block_professional/${professionalId}`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
        this.fetchAdminData();
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to block professional' };
      }
    },


    // Create a new service
    async createService() {
      try {
        const response = await fetch('/api/admin/service', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newService)
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
        this.fetchAdminData();
        this.closeAddServiceModal();
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to create service' };
      }
    },

    // Edit an existing service
    async editService() {
      try {
        const response = await fetch(`/api/admin/service/${this.selectedService.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.selectedService)
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
        this.fetchAdminData();
        this.closeEditServiceModal();
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to edit service' };
      }
    },

    // Delete a service
    async deleteService() {
      try {
        const response = await fetch(`/api/admin/service/${this.selectedService.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.message = { category: 'success', text: data.message };
        this.fetchAdminData();
        this.closeDeleteServiceModal();
      } catch (error) {
        this.message = { category: 'danger', text: 'Failed to delete service' };
      }
    },

    // Modal control methods
    openAddServiceModal() {
      this.newService = {
        service_title: '',
        service_details: '',
        starting_price: '',
        duration_required: ''
      };
      this.showAddServiceModal = true;
      console.log(this.showAddServiceModal)
    },
    closeAddServiceModal() {
      this.showAddServiceModal = false;
      this.newService = { service_title: '', service_details: '', starting_price: '', duration_required: '' };
    },

    openEditServiceModal(service) {
      this.selectedService = { ...service };
      this.showEditServiceModal = true;
    },
    closeEditServiceModal() {
      this.showEditServiceModal = false;
      this.selectedService = "";
    },

    openDeleteServiceModal(service) {
      this.selectedService = service;
      this.showDeleteServiceModal = true;
    },
    closeDeleteServiceModal() {
      this.showDeleteServiceModal = false;
      this.selectedService = "";
    },

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
        this.message = { category: 'danger', text: 'Failed to export, please run mailhog and celery' };
      }
    },
  }
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>