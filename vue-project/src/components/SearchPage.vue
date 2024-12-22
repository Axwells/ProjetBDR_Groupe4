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

            <label for="car-engine">Type de moteur:</label>
            <input type="text" id="car-engine" v-model="carEngine" placeholder="Type de moteur" />

            <label for="car-power">Puissance:</label>
            <input type="number" id="car-power" v-model="carPower" placeholder="Puissance en chevaux" />

            <button class="btn" @click="searchCars">Rechercher</button>
        </section>

        <section v-if="results.length > 0" class="search-results">
            <h2>Résultats de la recherche:</h2>
            <ul>
                <li v-for="(car, index) in results" :key="index">
                    <strong>{{ car.name }}</strong> - {{ car.brand }} - {{ car.engine }} - {{ car.power }} ch
                </li>
            </ul>
        </section>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const carName = ref('');
const carBrand = ref('');
const carEngine = ref('');
const carPower = ref('');
const results = ref([]);

const searchCars = () => {
    // For now, mock search results, you can replace this with an actual search query to your backend or API
    results.value = [
        { name: 'Audi RS3', brand: 'Audi', engine: '5-cylinder', power: 400 },
        { name: 'BMW M3', brand: 'BMW', engine: 'Inline-6', power: 500 },
        { name: 'Mercedes-AMG C63', brand: 'Mercedes', engine: 'V8', power: 470 },
    ];

    // Add basic filtering logic if necessary
    if (carName.value) {
        results.value = results.value.filter(car => car.name.toLowerCase().includes(carName.value.toLowerCase()));
    }
    if (carBrand.value) {
        results.value = results.value.filter(car => car.brand.toLowerCase().includes(carBrand.value.toLowerCase()));
    }
    if (carEngine.value) {
        results.value = results.value.filter(car => car.engine.toLowerCase().includes(carEngine.value.toLowerCase()));
    }
    if (carPower.value) {
        results.value = results.value.filter(car => car.power >= carPower.value);
    }
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