<template>
    <div class="search-page">
        <header>
            <h1>Recherche de Voitures</h1>
            <p>Entrez les critères de recherche pour trouver votre voiture préférée.</p>
        </header>

        <section class="search-form">
            <label for="car-name">Nom de la voiture:</label>
            <input type="text" id="car-name" v-model="carName" placeholder="Entrez le nom de la voiture" />

            <label for="car-brand">Marque:</label>
            <input type="text" id="car-brand" v-model="carBrand" placeholder="Entrez la marque" />

            <label for="car-engine">Type de moteur :</label>
            <select id="car-engine" v-model="carEngine">
                <option value="">-- Choisissez un type --</option>
                <option value="essence">Essence</option>
                <option value="electrique">Électrique</option>
            </select>

            <label for="car-power">Puissance minimale :</label>
            <input type="number" id="car-power" v-model="carPower" placeholder="Puissance en chevaux" />

            <button class="btn" @click="searchCars">Rechercher</button>
        </section>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const carName = ref("");
const carBrand = ref("");
const carEngine = ref("");
const carPower = ref(null);

const router = useRouter();

const searchCars = () => {
  const query = {
    carName: carName.value,
    carBrand: carBrand.value,
    carEngine: carEngine.value,
    carPower: carPower.value,
  };

  // Redirige vers la page des résultats avec les critères de recherche
  router.push({ name: "CarsPage", query });
};
</script>


<style scoped>
.search-page {
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 20px;
}

.search-form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
    margin: 0 auto;
}

.search-form label {
    margin-bottom: 5px;
}

.search-form input {
    margin-bottom: 15px;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
}

.search-form button {
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.search-form button:hover {
    background-color: #45a049;
}

.search-results {
    margin-top: 20px;
}

.search-results ul {
    list-style-type: none;
    padding: 0;
}

.search-results li {
    padding: 10px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    margin-bottom: 10px;
}
</style>