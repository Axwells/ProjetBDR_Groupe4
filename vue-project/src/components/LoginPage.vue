<template>
    <div class="login-page">
        <h1>Se Connecter</h1>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="email">Email :</label>
                <input
                    type="email"
                    id="email"
                    v-model="email"
                    placeholder="Entrez votre email"
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
            <button type="submit" class="btn">Se connecter</button>
        </form>
        <p v-if="error" class="error">{{ error }}</p>
        <p>Pas encore de compte ? <router-link to="/register">Créer un compte</router-link></p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const email = ref('');
const password = ref('');
const error = ref(null);

const handleLogin = async () => {
  error.value = null;
  try {
    const response = await axios.post('http://127.0.0.1:8000/app/login/', {
      email: email.value,
      password: password.value,
    });

    console.log('Login success:', response.data);

    // Store tokens in localStorage
    localStorage.setItem('accessToken', response.data.access);
    localStorage.setItem('refreshToken', response.data.refresh);
    localStorage.setItem('username', response.data.username);

    // Update login state
    window.location.href = '/'; // Redirect to homepage
  } catch (err) {
    console.error('Login failed:', err.response.data);
    error.value = err.response.data.message || 'Email ou mot de passe incorrect';
  }
};
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
    border: 1px solid #ccc;
}

button {
    padding: 10px 15px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

.error {
    color: red;
    margin-top: 10px;
    text-align: center;
}
</style>
