<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="registration-card">
          <h2 class="text-center mb-4">Professional Signup</h2>
          <div v-if="message" :class="`alert alert-${message.category} alert-dismissible fade show`" role="alert">
            {{ message.text }}
            <button type="button" class="btn-close" @click="message = null" aria-label="Close"></button>
          </div>
          <form @submit.prevent="register">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" class="form-control" id="username" v-model="username" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <textarea class="form-control" id="address" v-model="address" rows="2" required></textarea>
            </div>
            <div class="mb-3">
              <label for="postal_code" class="form-label">Postal Code</label>
              <input type="text" class="form-control" id="postal_code" v-model="postalCode" required>
            </div>
            <div class="mb-3">
              <label for="professional_experience" class="form-label">Experience Level</label>
              <select class="form-select" id="professional_experience" v-model="professionalExperience" required>
                <option value="" disabled>Select experience level</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Expert">Expert</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="service" class="form-label">Service</label>
              <select class="form-select" id="service" v-model="service" required>
                <option value="" disabled>Select a service</option>
                <option v-for="service in services" :key="service.id" :value="service.service_title">{{ service.service_title }}</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary w-100">Register</button>
          </form>
          <div class="text-center mt-3">
            <p>Already have an account? <router-link to="/user/login" class="text-white">Login here</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      address: '',
      postalCode: '',
      professionalExperience: '',
      service: '',
      services: [],
      message: null
    };
  },
  created() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch('/api/professional/register', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.services = data.services;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    async register() {
      const requestBody = {
        username: this.username,
        password: this.password,
        address: this.address,
        postal_code: this.postalCode,
        professional_experience: this.professionalExperience,
        service: this.service
      };
      try {
        const response = await fetch('/api/professional/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(requestBody)
        });
        const data = await response.json();
        if (response.ok) {
          this.message = { text: data.message, category: 'success' };
          this.$router.push('/user/login');
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error registering professional:', error);
        this.message = { text: 'An error occurred. Please try again.', category: 'danger' };
      }
    }
  }
};
</script>

<style scoped>
body {
  background-color: #f8f9fa;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.registration-card {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.alert {
  margin-top: 15px;
}
</style>