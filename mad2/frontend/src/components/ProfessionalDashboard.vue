<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Professional Dashboard: {{ professional.username }}</a>
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
      <div v-if="message" :class="`alert alert-${message.category} alert-dismissible fade show`" role="alert">
        {{ message.text }}
        <button type="button" class="btn-close" @click="message = null" aria-label="Close"></button>
      </div>
      <div class="profile-section">
        <h3>Profile Information</h3>
        <p><strong>Service:</strong> {{ professional.service }}</p>
        <p><strong>Address:</strong> {{ professional.address }}</p>
        <p><strong>Postal Code:</strong> {{ professional.postal_code }}</p>
        <p><strong>Rating:</strong> {{ professional.rating }}</p>
        <p><strong>Experience Level:</strong> {{ professional.experience }}</p>
        <button class="btn btn-primary" @click="openEditProfileModal">Edit Profile</button>
      </div>
      <h4>Service Requests</h4>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Service</th>
            <th>Customer</th>
            <th>Request Date</th>
            <th>Details</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in pendingRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.service_title }}</td>
            <td>{{ request.customer_name }}</td>
            <td>{{ request.details }}</td>
            <td>{{ new Date(request.created_at).toLocaleDateString() }}</td>
            <td>{{ request.request_status }}</td>
            <td>
              <button class="btn btn-success btn-sm" @click="acceptRequest(request.id)">Accept</button>
              <button class="btn btn-danger btn-sm" @click="rejectRequest(request.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
      <h4>Accepted Requests</h4>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Service</th>
            <th>Customer</th>
            <th>Details</th>
            <th>Completion Date</th>
          </tr>
        </thead>
        <tbody>
          <!-- {{ acceptedRequests }} -->
          <tr v-for="accepted in acceptedRequests" :key="accepted.id">
            <td>{{ accepted.id }}</td>
            <td>{{ accepted.service_title }}</td>
            <td>{{ accepted.customer_name }}</td>
            <td>{{ accepted.details }}</td>
            <td>{{ new Date(accepted.closed_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
      <h4>Closed Requests</h4>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Service</th>
            <th>Customer</th>
            <th>Details</th>
            <th>Completion Date</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="closed in closedRequests" :key="closed.id">
            <td>{{ closed.id }}</td>
            <td>{{ closed.service_title }}</td>
            <td>{{ closed.customer_name }}</td>
            <td>{{ closed.details }}</td>
            <td>{{ new Date(closed.closed_at).toLocaleDateString() }}</td>
            <td>{{ closed.customer_rating > 0 ? `${closed.customer_rating}/5` : 'Not rated' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editProfileModalLabel">Edit Profile</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="editProfile">
            <div class="modal-body">
              <div class="mb-3">
                <label for="user_address" class="form-label">Address</label>
                <input type="text" class="form-control" id="user_address" v-model="professional.address" required>
              </div>
              <div class="mb-3">
                <label for="postal_code" class="form-label">Postal Code</label>
                <input type="text" class="form-control" id="postal_code" v-model="professional.postal_code" required>
              </div>
              <div class="mb-3">
                <label for="experience_level" class="form-label">Experience Level</label>
                <select id="experience_level" v-model="professional.experience" class="form-select" required>
                  <option value="" disabled>-- Choose Experience Level --</option>
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Expert">Expert</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  <!-- </div> -->
</template>

<script>
export default {
  data() {
    return {
      professional: {},
      pendingRequests: [],
      closedRequests: [],
      acceptedRequests: [],
      message: null
    };
  },
  created() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await fetch('/api/professional/dashboard', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        console.log(data);
        this.professional = data.professional;
        this.pendingRequests = data.pending_requests;
        this.acceptedRequests = data.accepted_requests;
        this.closedRequests = data.closed_requests;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    },
    openEditProfileModal() {
      new bootstrap.Modal(document.getElementById('editProfileModal')).show();
    },
    async editProfile() {
      try {
        const response = await fetch('/api/professional/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.professional)
        });
        const data = await response.json();
        if (response.ok) {
          this.message = { text: data.message, category: 'success' };
          this.fetchDashboardData();
          new bootstrap.Modal(document.getElementById('editProfileModal')).hide();
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error editing profile:', error);
        this.message = { text: 'An error occurred. Please try again.', category: 'danger' };
      }
    },
    async acceptRequest(requestId) {
      try {
        const response = await fetch(`/api/professional/request/${requestId}/accept`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.message = { text: data.message, category: 'success' };
          this.fetchDashboardData();
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error accepting request:', error);
        this.message = { text: 'An error occurred. Please try again.', category: 'danger' };
      }
    },
    async rejectRequest(requestId) {
      try {
        const response = await fetch(`/api/professional/request/${requestId}/reject`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.message = { text: data.message, category: 'success' };
          this.fetchDashboardData();
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error rejecting request:', error);
        this.message = { text: 'An error occurred. Please try again.', category: 'danger' };
      }
    }
  }
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

h4
{
  margin-left: 20px;
}
.table {
  margin-left: 20px;
  margin-right: 20px;
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