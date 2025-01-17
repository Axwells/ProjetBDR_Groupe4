<template>
  <div class="homepage">
    <header class="main-header">
      <div v-if="authStore.isLoggedIn" class="user-info">
        <p>Connecté en tant que : <strong>{{ authStore.username }}</strong></p>
      </div>
      <h1>Bienvenue sur le Dictionnaire de Voitures</h1>
    </header>

    <main class="main-content">
      <!-- Search Section -->
      <section id="search" class="section">
        <h2>Rechercher une Voiture</h2>
        <p>Recherchez des informations sur vos voitures préférées par nom, marque, moteur, ou puissance.</p>
        <router-link to="/search">
          <button class="btn">Commencez votre recherche</button>
        </router-link>
      </section>

      <!-- Register Section -->
      <section v-if="!authStore.isLoggedIn" id="register" class="section">
        <h2>Register</h2>
        <p>
          Rejoignez notre communauté en créant un compte. En tant qu'utilisateur, vous pourrez :
        </p>
        <ul>
          <li>Donner votre avis sur les voitures et partager vos expériences.</li>
          <li>Proposer de nouvelles informations ou modèles à ajouter.</li>
        </ul>
        <router-link to="/register">
          <button class="btn">Créer un compte</button>
        </router-link>
      </section>

      <!-- Login Section -->
      <section v-if="!authStore.isLoggedIn" id="login" class="section">
        <h2>Login</h2>
        <p>Déjà un compte ?</p>
        <router-link to="/login">
          <button class="btn">Se connecter</button>
        </router-link>
      </section>
    </main>
  </div>
</template>


<script setup>
import { authStore } from '../store'; // Importer le store

// Pas besoin de propriétés locales, le store est directement réactif
</script>


<style src="../assets/main.css"></style>