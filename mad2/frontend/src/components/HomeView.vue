<template>
  <div class="home-container">
    <h1>Welcome to Household Services App</h1>
    <div class="button-group">
      <router-link to="/admin/login" class="btn btn-primary">Admin Login</router-link>
      <router-link to="/user/login" class="btn btn-primary">Customer Login</router-link>
      <router-link to="/customer/reg" class="btn btn-primary">Customer Registration</router-link>
      <router-link to="/user/login" class="btn btn-primary">Professional Login</router-link>
      <router-link to="/professional/reg" class="btn btn-primary">Professional Registration</router-link>

    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
};
</script>

<style scoped>
.home-container {
  text-align: center;
  margin-top: 50px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.btn-primary {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #217dbb;
}
</style>

