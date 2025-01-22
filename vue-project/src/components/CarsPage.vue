<template>
  <div class="cars-page">
    <header class="main-header">
      <h1>Résultats de la Recherche</h1>
    </header>

    <main v-if="cars.length > 0" class="main-content">
      <section class="cars-list">
        <div
          v-for="car in cars"
          :key="car.modelName"
          class="car-item"
          @click="goToSpecsPage(car.modelName)"
        >
          <h2>{{ car.modelName }}</h2>
          <p><strong>Marque :</strong> {{ car.brandName }}</p>
          <p><strong>Nombre de sièges :</strong> {{ car.numberOfSeats }}</p>
          <p><strong>Date de sortie :</strong> {{ car.releaseDate }}</p>
          <p><strong>Prix :</strong> {{ car.defaultPrice }} €</p>

          <div class="car-images">
            <h3>Images :</h3>
            <div v-if="car.images && car.images.length > 0" class="carousel">
              <div
                v-for="image in car.images"
                :key="image.id"
                class="carousel-item"
              >
                <img
                  :src="`/images/cars/${image.image}`"
                  :alt="`Image de ${car.modelName} - ${image.image}`"
                  style="max-height: 100px;"
                />
              </div>
            </div>
            <p v-else>Aucune image disponible pour ce modèle.</p>
          </div>
        </div>
      </section>
    </main>

    <p v-else class="no-cars-message">
      Aucun résultat trouvé pour vos critères de recherche.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const searchParams = route.query; // Récupère les critères de recherche passés dans l'URL
const cars = ref([]);

// Navigation vers SpecsPage
const goToSpecsPage = (modelName) => {
  router.push({ name: "SpecsPage", params: { modelName } });
};

// Récupération des résultats de la recherche
onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/app/search", {
      params: searchParams, // Transmet les paramètres de recherche à l'API
    });
    cars.value = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des résultats :", error);
    cars.value = [];
  }
});
</script>

<style src="../assets/main.css"></style>

<style scoped>
.cars-page {
  font-family: Arial, sans-serif;
  padding: 20px;
}

.main-header {
  text-align: center;
  background-color: #42b983;
  color: white;
  padding: 10px;
}

.cars-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.car-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.car-item:hover {
  transform: scale(1.02);
}

.car-item img {
  max-width: 100%;
  border-radius: 8px;
}

.carousel {
  display: flex;
  overflow-x: auto;
  gap: 10px;
}

.carousel-item {
  flex: 0 0 auto;
  width: 150px;
  height: 100px;
}

.no-cars-message {
  text-align: center;
  font-size: 18px;
  color: red;
  margin-top: 20px;
}
</style>
