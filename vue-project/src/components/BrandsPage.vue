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
                    <li
                v-for="brand in brands"
                :key="brand.name"
                @click="goToBrandCars(brand.name)"
                class="brand-item"
            >
                <strong>{{ brand.name }}</strong>
                <img
                    v-if="brand.image"
                    :src="`/images/brands/${brand.image}`"
                    :alt="brand.name"
                    style="max-height: 100px;"
                />
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
import { useRouter } from 'vue-router';

const username = "Jean Dupont"; // Remplacez par une donnée dynamique si nécessaire
const brands = ref([]);
const router = useRouter();

// Appel à l'API lors du montage du composant
onMounted(async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/app/brands/');
        brands.value = response.data;
    } catch (error) {
        console.error("Erreur lors de la récupération des marques :", error);
    }
});

const goToBrandCars = (brandName) => {
    const query = {
    carName: "",
    carBrand: brandName,
    carEngine: "",
    carPower: null,
  };

  // Redirige vers la page des résultats avec les critères de recherche
  router.push({ name: "CarsPage", query });
};
</script>

<style src="../assets/main.css"></style>
