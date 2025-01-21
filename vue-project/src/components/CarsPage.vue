<template>
    <div class="homepage">
        <header class="main-header">
            <div class="user-info">
                <p>Connecté en tant que : <strong>{{ username }}</strong></p>
            </div>
            <h1>Bienvenue sur le Dictionnaire de Voitures</h1>
        </header>

        <main class="main-content">
            <section id="cars">
                <h2>Voitures de la marque {{ brandName }}</h2>
                <ul>
                    <li v-for="car in cars" :key="car.modelName" class="car-item">
                        <strong>{{ car.modelName }}</strong> - {{ car.numberOfSeats }} sièges,
                        sortie le {{ car.releaseDate }}, prix : {{ car.defaultPrice }} €
                    </li>
                </ul>
            </section>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const username = "Jean Dupont"; // Remplacez par une donnée dynamique si nécessaire
const cars = ref([]);
const route = useRoute();
const brandName = route.params.brandName; // Récupère le nom de la marque depuis l'URL

// Appel à l'API pour récupérer les voitures de la marque
onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/app/brands/${brandName}/cars/`);
        cars.value = response.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des voitures :", error);
    }
});
</script>

<style src="../assets/main.css"></style>
