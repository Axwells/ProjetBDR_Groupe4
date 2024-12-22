<template>
    <div class="register-page">
        <h1>Créer un Compte</h1>
        <form @submit.prevent="handleRegister">
            <div class="form-group">
                <label for="username">Nom d'utilisateur :</label>
                <input type="text" id="username" v-model="username" placeholder="Entrez votre nom d'utilisateur"
                    required />
            </div>
            <div class="form-group">
                <label for="email">Email :</label>
                <input type="email" id="email" v-model="email" placeholder="Entrez votre adresse email" required />
            </div>
            <div class="form-group">
                <label for="password">Mot de passe :</label>
                <input type="password" id="password" v-model="password" placeholder="Entrez votre mot de passe"
                    required />
            </div>
            <button type="submit" class="btn">S'inscrire</button>
        </form>
        <p>Vous avez déjà un compte ? <router-link to="/login">Se connecter</router-link></p>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')

const handleRegister = () => {
    // Code pour gérer l'inscription ici (ex: appel à une API)
    console.log('Nom d\'utilisateur:', username.value)
    console.log('Email:', email.value)
    console.log('Mot de passe:', password.value)
    // Après l'inscription réussie, rediriger vers la page de login ou accueil
}
</script>

<style scoped>
.register-page {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
}

.form-group {
    margin-bottom: 10px;
}

input {
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    border-radius: 4px;
}

button {
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

p {
    text-align: center;
    margin-top: 10px;
}
</style>