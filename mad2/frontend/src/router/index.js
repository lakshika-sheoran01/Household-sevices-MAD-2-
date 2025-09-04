import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import AdminDashboard from '@/components/AdminDashboard.vue';
import AdminLogin from '@/components/AdminLogin.vue';
import AdminStats from '@/components/AdminStats.vue';
import CustomerDashboard from '@/components/CustomerDashboard.vue';
import CustomerReg from '@/components/CustomerReg.vue';
import ProfessionalDashboard from '@/components/ProfessionalDashboard.vue';
import ProfessionalReg from '@/components/ProfessionalReg.vue';
import UserLogin from '@/components/UserLogin.vue';
import ServiceRequest from '@/components/ServiceRequest.vue';

const routes= [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboard,
  },
  {
    path: '/admin/login',
    name: 'admin-login',
    component: AdminLogin,
  },
  {
    path: '/admin/stats',
    name: 'admin-stats',
    component: AdminStats,
  },
  {
    path: '/customer/dashboard',
    name: 'customer-dashboard',
    component: CustomerDashboard,
  },
  {
    path: '/customer/reg',
    name: 'customer-reg',
    component: CustomerReg,
  },
  {
    path: '/professional/dashboard',
    name: 'professional-dashboard',
    component: ProfessionalDashboard,
  },
  {
    path: '/professional/reg',
    name: 'professional-reg',
    component: ProfessionalReg,
  },
  {
    path: '/user/login',
    name: 'user-login',
    component: UserLogin,
  }
  ,
  {
    path: '/service-request/:id',
    name: 'service-request',
    component: ServiceRequest,
  }
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router;
