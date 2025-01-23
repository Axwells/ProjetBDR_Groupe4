<template>
  <div id="app">
    <!-- Navbar Section -->
    <nav class="navbar">
      <ul class="navbar-links">
        <li><router-link to="/" class="navbar-item">Accueil</router-link></li>
        <li v-if="!authStore.isLoggedIn"><router-link to="/register" class="navbar-item">Inscription</router-link></li>
        <li v-if="!authStore.isLoggedIn"><router-link to="/login" class="navbar-item">Connexion</router-link></li>
        <li v-if="authStore.isLoggedIn"><router-link to="/" @click.prevent="handleLogout" class="navbar-item">Déconnexion</router-link></li>
        <li><router-link to="/brands" class="navbar-item">Marques</router-link></li>
        <li><router-link to="/search" class="navbar-item">Voitures</router-link></li>

        <!-- Admin Dropdown -->
        <li v-if="authStore.isSuperUser" class="dropdown">
          <div class="dropdown-container">
            <button @click="toggleDropdown" class="navbar-item dropdown-btn">
              Admin
            </button>
            <ul v-show="showDropdown" class="dropdown-menu">
              <li><router-link to="/admin/modifications" class="dropdown-item">Gestion des Modifications</router-link></li>
              <li><router-link to="/admin/users" class="dropdown-item">Gestion des Utilisateurs</router-link></li>
            </ul>
          </div>
        </li>
      </ul>
    </nav>

    <!-- The page content will be rendered here -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { authStore } from "./store";

const showDropdown = ref(false); // État pour afficher ou masquer le menu déroulant

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value; // Alterne entre afficher et masquer
};

const handleLogout = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("username");
  localStorage.removeItem("email");
  localStorage.removeItem("isSuperUser");

  authStore.setLoginStatus(false); // Met à jour l'état global
  alert("Vous êtes déconnecté");
};

onMounted(() => {
  const token = localStorage.getItem("accessToken");
  const username = localStorage.getItem("username");
  const email = localStorage.getItem("email");
  const isSuperUser = localStorage.getItem("isSuperUser") === "true";
  if (token && username && email) {
    authStore.setLoginStatus(true, username, email, isSuperUser);
  }
});
</script>

<style scoped>
/* Basic Navbar Styles */
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

/* Dropdown Styles */
.dropdown-container {
  position: relative;
  display: inline-block;
}

.dropdown-btn {
  background: none;
  border: none;
  color: white;
  padding: 15px 25px;
  font-size: 18px;
  cursor: pointer;
}

.dropdown-btn:hover {
  background-color: #575757;
  border-radius: 5px;
}

.dropdown-menu {
  position: absolute;
  top: 50px;
  left: 0;
  background-color: #333;
  list-style: none;
  padding: 10px 0;
  margin: 0;
  border-radius: 5px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  z-index: 100;
  min-width: 200px;
}

.dropdown-item {
  display: block;
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #575757;
}

/* Align Dropdown with Navbar */
.navbar-item,
.dropdown-btn {
  display: inline-block;
  vertical-align: middle;
}

.dropdown {
  position: relative;
}
</style>
