<script setup>
const username = "Jean Dupont"; // Remplacez ceci par la variable dynamique correspondant au nom de l'utilisateur connecté.
</script>

<template>
  <div class="homepage">
    <header class="main-header">
      <div class="user-info">
        <p>Connecté en tant que : <strong>{{ username }}</strong></p>
      </div>
      <h1>Bienvenue sur le Dictionnaire de Voitures</h1>
    </header>

    <main class="main-content">
      <!-- Search Section -->
      <section id="search" class="section">
        <h2>Rechercher une Voiture</h2>
        <p>Recherchez des informations sur vos voitures préférées par nom, marque, moteur, ou puissance.</p>
        <p>Affinez votre recherche grâce à nos filtres avancés : marque, type de moteur, puissance, et bien plus.</p>
        <button class="btn">Commencez votre recherche</button>
      </section>

      <!-- Register Section -->
      <section id="register" class="section">
        <h2>Register</h2>
        <p>
          Rejoignez notre communauté en créant un compte. En tant qu'utilisateur, vous pourrez :
        </p>
        <ul>
          <li>Donner votre avis sur les voitures et partager vos expériences.</li>
          <li>Proposer de nouvelles informations ou modèles à ajouter.</li>
        </ul>
        <p>Les administrateurs vérifieront vos propositions et les intégreront si elles sont pertinentes.</p>
        <button class="btn">Créer un compte</button>
      </section>

      <!-- Login Section -->
      <section id="login" class="section">
        <h2>Login</h2>
        <p>Déjà un compte ?</p>
        <p>
          Cliquez ci-dessous pour vous connecter à votre compte et profiter de toutes nos fonctionnalités :
        </p>

        <button class="btn">Se connecter</button>
      </section>
    </main>
  </div>
</template>



<style src="./assets/main.css"></style>
