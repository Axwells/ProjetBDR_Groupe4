<template>
    <div class="login-page">
        <h1>Se Connecter</h1>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="email">Email :</label>
                <input type="email" id="email" v-model="email" placeholder="Entrez votre email" required />
            </div>
            <div class="form-group">
                <label for="password">Mot de passe :</label>
                <input type="password" id="password" v-model="password" placeholder="Entrez votre mot de passe"
                    required />
            </div>
            <button type="submit" class="btn">Se connecter</button>
        </form>
        <p>Pas encore de compte ? <router-link to="/register">Créer un compte</router-link></p>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const handleLogin = () => {
    // Code pour gérer la connexion ici (ex: appel à une API)
    console.log('Email:', email.value)
    console.log('Mot de passe:', password.value)
    // Après la connexion réussie, rediriger vers la page d'accueil ou tableau de bord
}
</script>

<style scoped>
.login-page {
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