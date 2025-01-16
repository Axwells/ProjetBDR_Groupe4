<template>
    <div class="homepage">
        <header class="main-header">
            <div class="user-info">
                <p>Connecté en tant que : <strong>{{ username }}</strong></p>
            </div>
            <h1>Bienvenue sur le Dictionnaire de Voitures</h1>
        </header>

        <main class="main-content">
            <section id="brands">
                <h2>Marques disponibles</h2>
                <ul>
                    <li v-for="brand in brands" :key="brand.name">
                        <strong>{{ brand.name }}</strong>
                        <img v-if="brand.image" :src="brand.image" :alt="brand.name" style="max-height: 100px;" />
                        <span v-else>(Pas d'image disponible)</span>
                    </li>
                </ul>
            </section>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const username = "Jean Dupont"; // Remplacez par une donnée dynamique si nécessaire
const brands = ref([]);

// Appel à l'API lors du montage du composant
onMounted(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/app/api/brands/');
        brands.value = response.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des marques :", error);
    }
});
</script>

<style src="../assets/main.css"></style>
