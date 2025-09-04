<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="login-container">
          <h2 class="text-center mb-4">Login</h2>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" class="form-control" id="username" v-model="username" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </form>
          <div v-if="message" :class="`alert alert-${message.category} alert-dismissible fade show mt-3`" role="alert">
            {{ message.text }}
            <button type="button" class="btn-close" @click="message = null" aria-label="Close"></button>
          </div>
        </div>
      </div>
      <div class="text-center mt-3">
      <router-link to="/" class="btn btn-secondary">Home</router-link>
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
      message: null
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('/api/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });
        const data = await response.json();
        if (response.ok) {
          localStorage.setItem('token', data.access_token);
          this.message = { text: data.message, category: 'success' };
          if (data.user_role === 'admin') {
            this.$router.push('/admin/dashboard');
          } else if (data.user_role === 'professional') {
            this.$router.push('/professional/dashboard');
          } else {
            this.$router.push('/customer/dashboard');
          }
        } else {
          this.message = { text: data.message, category: 'danger' };
        }
      } catch (error) {
        console.error('Error logging in:', error);
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
.login-container {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.form-label {
  font-weight: bold;
}
</style>