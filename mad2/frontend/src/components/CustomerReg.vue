<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="registration-container">
          <h2 class="text-center mb-4">Customer Signup</h2>
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
            <button type="submit" class="btn btn-primary w-100">Register</button>
          </form>
          <div class="text-center mt-3">
            <p>Already have an account? <router-link to="/user/login" class="text-primary">Login here</router-link></p>
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
      message: null
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('/api/customer/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            address: this.address,
            postal_code: this.postalCode
          })
        });
        const data = await response.json();
        if (response.ok) {
          this.message = { text: data.message, category: 'success' };
          this.$router.push('/user/login');
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error registering customer:', error);
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
.registration-container {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.form-label {
  font-weight: bold;
}
</style>