<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Customer Dashboard: {{ customer.username }}</a>
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
              <a class="nav-link" href="/">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <input v-model="searchQuery" type="text" class="form-control mb-3 w-50" 
            placeholder="Search available services, requested services..." />

      <div v-if="customer" class="profile-section">
        <h4>Profile Information</h4>
        <p><strong>Address:</strong> {{ customer.user_address }}</p>
        <p><strong>Postal Code:</strong> {{ customer.postal_code }}</p>
      </div>
      <button class="btn btn-primary" @click="openProfileModal" data-bs-toggle="modal"
        data-bs-target="#editProfileModal">Edit Profile</button>
    </div>

    <h4 class="m-3">Available Services</h4>
    <div class="d-flex flex-wrap justify-content-start gap-3" style="margin-left: 20px;  margin-right: 20px;">
      <div v-for="service in filteredServices" :key="service.id" class="card service-card" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">{{ service.service_title }}</h5>
          <p class="card-text">{{ service.description }}</p>
          <router-link :to="'/service-request/' + service.id" class="btn btn-primary">Request Service</router-link>
        </div>
      </div>
    </div>

    <h4 class="m-3">Service History</h4>
    <div class="service-history-table card p-4">
      <table class="table table-striped m-3">
        <thead>
          <tr>
            <th scope="col">Service</th>
            <th scope="col">Professional</th>
            <th scope="col">Date</th>
            <th scope="col">Status</th>
            <th scope="col">Rating</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="history in filteredServicesHistory" :key="history.id">
            <td>{{ history.service_title }}</td>
            <td>{{ history.professional_username || "Not assigned" }}</td>
            <td>{{ history.created_at }}</td>
            <td>{{ history.request_status }}</td>
            <td>{{ history.customer_rating || "Not rated" }}</td>
            <td>
              <div v-if="history.request_status === 'Accepted'">
                <button class="btn btn-success btn-sm" @click="markRequestAsClosed(history.id)">Mark as Done</button>
              </div>
              <div v-if="history.request_status === 'Closed' && !history.customer_rating">
                <button class="btn btn-primary btn-sm" @click="openRatingModal(history.id)" data-bs-toggle="modal"
                  data-bs-target="#rateModal">Rate</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editProfileModalLabel">Edit Profile</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="updateProfile">
            <div class="modal-body">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" v-model="form.username" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" v-model="form.password" class="form-control" />
              </div>
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" v-model="form.user_address" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="postal_code" class="form-label">Postal Code</label>
                <input type="text" v-model="form.postal_code" class="form-control" required />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary" >Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="modal fade" id="rateModal" tabindex="-1" aria-labelledby="rateModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="rateModalLabel">Rate Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="rateService">
            <div class="modal-body">
              <div class="mb-3">
                <label for="rating" class="form-label">Rating (1-5)</label>
                <input type="number" v-model="ratingForm.rating" class="form-control" min="1" max="5" required />
              </div>
              <div class="mb-3">
                <label for="review" class="form-label">Your Review</label>
                <textarea v-model="ratingForm.review" class="form-control" rows="4" required></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customer: {},
      services: [],
      serviceHistory: [],
      form: {
        username: "",
        password: "",
        user_address: "",
        postal_code: "",
      },
      ratingForm: {
        rating: 1,
        review: "",
      },
      searchQuery: ""
        };
    },
    computed: {
        filteredServices() {
            return this.services.filter(service => 
            service.service_title.toLowerCase().includes(this.searchQuery.toLowerCase()));
        },
        filteredServicesHistory() {
            return this.serviceHistory.filter(service => 
            service.service_title.toLowerCase().includes(this.searchQuery.toLowerCase()));
        },
    },
  mounted() {
    this.getCustomerDashboard();
  },
  methods: {
    async getCustomerDashboard() {
      try {
        const response = await fetch("/api/customer/dashboard", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const data = await response.json();
        this.customer = data.customer;
        this.services = data.services;
        this.serviceHistory = data.service_history;
      } catch (error) {
        console.error("Error fetching customer data:", error);
      }
    },
    async updateProfile() {
      try {
        const response = await fetch("/api/customer/profile", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(this.form),
        });
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
          this.getCustomerDashboard();
        }
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    },
    async markRequestAsClosed(requestId) {
      try {
        const response = await fetch(`/api/customer/request/${requestId}/close`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
          this.getCustomerDashboard();
        }
      } catch (error) {
        console.error("Error closing request:", error);
      }
    },
    async rateService() {
      try {
        const response = await fetch(`/api/customer/request/${this.ratingForm.request_id}/rate`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(this.ratingForm),
        });
        const result = await response.json();
        alert(result.message);
        if (response.ok) {
          this.getCustomerDashboard();
        }
      } catch (error) {
        console.error("Error rating service:", error);
      }
    },
    openProfileModal() {
      this.form.username = this.customer.username;
      this.form.user_address = this.customer.user_address;
      this.form.postal_code = this.customer.postal_code;
    },
    openRatingModal(requestId) {
      this.ratingForm.request_id = requestId;
    },
  },
};
</script>

<style scoped>
body {
  background-color: #f4f6f9;
}

.navbar {
  margin-bottom: 20px;
}

.profile-section {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.profile-section p {
  margin-bottom: 5px;
}

.table thead {
  background-color: #007bff;
  color: white;
}

.table tbody tr:hover {
  background-color: #f1f1f1;
}

.modal-header {
  background-color: #007bff;
  color: white;
}
</style>
