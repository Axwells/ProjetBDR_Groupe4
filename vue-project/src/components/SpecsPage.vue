<template>
  <div class="specs-page">
    <header class="main-header" v-if="car">
      <h1>{{ car.brandName}} {{ modelName }}</h1>
    </header>

    <!-- Section des informations de base -->
    <section v-if="car" class="car-info">
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
    </section>

    <div class="main-content">
      <aside class="specs-list">
        <h2>Spécifications</h2>
        <ul>
          <li
            v-for="spec in specs"
            :key="spec.id"
            @click="selectSpec(spec)"
            :class="{ active: selectedSpec?.id === spec.id }"
          >
            Spécification {{ spec.id }}
          </li>
        </ul>
      </aside>

      <section v-if="selectedSpec" class="spec-details">
        <h2>Détails de la Spécification (A travailler dessus encore)</h2>
        <p><strong>Freins :</strong> {{ selectedSpec.brake.model }}</p>
        <p><strong>ABS :</strong> {{ selectedSpec.brake.abs ? "Oui" : "Non" }}</p>
        <p><strong>Transmission :</strong> {{ selectedSpec.transmission.type }}</p>
        <p><strong>Performance :</strong> {{ selectedSpec.performance.maxSpeed }} km/h</p>
        <h3>Moteurs :</h3>
        <ul>
          <li v-for="engine in selectedSpec.engines" :key="engine.modelName">
            {{ engine.modelName }} - {{ engine.horsePower }} ch
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const modelName = ref(route.params.modelName);
const car = ref(null); // Informations de la voiture
const specs = ref([]);
const selectedSpec = ref(null);

// Récupération des informations de la voiture
const fetchCarDetails = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/app/cars/details/${modelName.value}/`
    );
    car.value = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des détails de la voiture :", error);
    car.value = null;
  }
};

// Récupération des spécifications
const fetchSpecifications = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/app/specifications/${modelName.value}/`
    );
    specs.value = response.data;
    if (specs.value.length > 0) {
      selectedSpec.value = specs.value[0];
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des spécifications :", error);
    specs.value = [];
  }
};

// Charger les données lors du montage
onMounted(async () => {
  await fetchCarDetails();
  await fetchSpecifications();
});

const selectSpec = (spec) => {
  selectedSpec.value = spec;
};
</script>

<style src="../assets/main.css"></style>

<style scoped>
.specs-page {
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
}

.main-header {
  text-align: center;
  background-color: #42b983;
  color: white;
  padding: 10px;
}

.car-info {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.car-images {
  margin-top: 10px;
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

.main-content {
  display: flex;
}

.specs-list {
  width: 30%;
  border-right: 1px solid #ddd;
  padding: 10px;
}

.specs-list ul {
  list-style: none;
  padding: 0;
}

.specs-list li {
  padding: 10px;
  cursor: pointer;
  border: 1px solid #ddd;
  margin-bottom: 5px;
  border-radius: 5px;
}

.specs-list li.active {
  background-color: #42b983;
  color: white;
}

.spec-details {
  flex-grow: 1;
  padding: 20px;
}

.spec-details h2 {
  margin-bottom: 10px;
}
</style>
