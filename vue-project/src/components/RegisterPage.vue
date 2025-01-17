<template>
    <div class="register-page">
        <h1>Créer un Compte</h1>
        <form @submit.prevent="handleRegister">
            <div class="form-group">
                <label for="username">Nom d'utilisateur :</label>
                <input
                    type="text"
                    id="username"
                    v-model="username"
                    placeholder="Entrez votre nom d'utilisateur"
                    required
                />
            </div>
            <div class="form-group">
                <label for="email">Email :</label>
                <input
                    type="email"
                    id="email"
                    v-model="email"
                    placeholder="Entrez votre adresse email"
                    required
                />
            </div>
            <div class="form-group">
                <label for="password">Mot de passe :</label>
                <input
                    type="password"
                    id="password"
                    v-model="password"
                    placeholder="Entrez votre mot de passe"
                    required
                />
            </div>
            <button type="submit" class="btn">S'inscrire</button>
        </form>
        <p v-if="error" class="error-message">{{ error }}</p>
        <p>Vous avez déjà un compte ? <router-link to="/login">Se connecter</router-link></p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const username = ref('');
const email = ref('');
const password = ref('');
const error = ref('');

const handleRegister = async () => {
    error.value = ''; // Reset error message
    try {
        const response = await axios.post('http://127.0.0.1:8000/app/register/', {
            email: email.value,
            username: username.value,
            password: password.value,
        });

        if (response.status === 201) {
            // Registration successful, redirect to login or dashboard
            alert('Inscription réussie ! Vous pouvez vous connecter.');
            window.location.href = '/login'; // Adjust this path to your actual login route
        }
    } catch (err) {
        // Display error message
        if (err.response && err.response.data) {
            error.value = 'Une erreur est survenue lors de l\'inscription : ' + err.response.data.detail;
        } else {
            error.value = "Une erreur est survenue lors de l'inscription";
        }
        console.error(err);
    }
};
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

.error-message {
    color: red;
    margin-top: 10px;
    text-align: center;
}
</style>
