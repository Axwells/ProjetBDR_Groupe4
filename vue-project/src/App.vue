<template>
  <div id="app">
    <!-- Navbar Section -->
    <nav class="navbar">
      <ul class="navbar-links">
        <li><router-link to="/" class="navbar-item">Accueil</router-link></li>
        <li v-if="!authStore.isLoggedIn"><router-link to="/register" class="navbar-item">Inscription</router-link></li>
        <li v-if="!authStore.isLoggedIn"><router-link to="/login" class="navbar-item">Connexion</router-link></li>
        <li v-if="authStore.isLoggedIn"><router-link to="/" @click.prevent="handleLogout" class="navbar-item">Déconnexion</router-link></li>
        <li><router-link to="/search" class="navbar-item">Voitures</router-link></li>
      </ul>
    </nav>

    <!-- The page content will be rendered here -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { authStore } from './store';

const handleLogout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('username');
  
  authStore.setLoginStatus(false); // Met à jour l'état global
  alert('Vous êtes déconnecté');
};
  
onMounted(() => {
  const token = localStorage.getItem('accessToken');
  const username = localStorage.getItem('username');
  if (token && username) {
    authStore.setLoginStatus(true, username);
  }
});
</script>

<style scoped>
/* Basic Styles for Navbar */
.navbar {
  background-color: #333;
  padding: 10px 0;
  text-align: center;
}

.navbar-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
}

.navbar-item {
  text-decoration: none;
  color: white;
  padding: 15px 25px;
  font-size: 18px;
  cursor: pointer;
}

.navbar-item:hover {
  background-color: #575757;
  border-radius: 5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-links {
    flex-direction: column;
  }

  .navbar-item {
    padding: 12px 20px;
    font-size: 16px;
  }
}
</style>
