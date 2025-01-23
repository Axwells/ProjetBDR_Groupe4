<template>
  <div class="specs-page">
    <header class="main-header" v-if="car">
      <div v-if="authStore.isLoggedIn" class="user-info">
        <p>Connecté en tant que : <strong>{{ authStore.username }}</strong></p>
      </div>
      <h1>{{ car.brandName }} {{ modelName }}</h1>
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
      <button v-if="authStore.isLoggedIn" @click="showModifForm = true" class="btn-add-review">Proposer une modification</button>
          <p v-else>Connectez-vous pour proposer une modification.</p>
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
        <h2>Détails de la Spécification</h2>
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

        <!-- Section des reviews -->
        <h3>Reviews</h3>
        <div class="reviews-section">
          <ul>
            <li v-for="review in reviews" :key="review.id">
              <strong>{{ review.title }}</strong> - Note : {{ review.grade }}/5
              <p>{{ review.content || "Pas de contenu fourni." }}</p>
              <small>Posté par : {{ review.username }}</small>
            </li>
          </ul>
          <button v-if="authStore.isLoggedIn" @click="showReviewForm = true" class="btn-add-review">Écrire une review</button>
          <p v-else>Connectez-vous pour écrire une review.</p>
        </div>
      </section>
    </div>


    <div v-if="showReviewForm" class="modal-overlay">
      <div class="modal-content">
        <h2>Ajouter une Review</h2>
        <form @submit.prevent="addReview">
          <label for="title">Titre :</label>
          <input type="text" id="title" v-model="newReview.title" required />

          <label for="content">Contenu :</label>
          <textarea id="content" v-model="newReview.content"></textarea>

          <label for="grade">Note :</label>
          <input type="number" id="grade" v-model="newReview.grade" min="1" max="5" required />

          <button type="submit">Envoyer</button>
          <button type="button" @click="showReviewForm = false">Annuler</button>
        </form>
      </div>
    </div>

    <div v-if="showModifForm" class="modal-overlay">
      <div class="modal-content">
        <h2>Proposer une modification</h2>
        <form @submit.prevent="addModif">
          <label for="title">Texte :</label>
          <input type="text" id="title" v-model="newModif.text" required />

          <button type="submit">Envoyer</button>
          <button type="button" @click="showModifForm = false">Annuler</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { authStore } from "../store";

const route = useRoute();
const modelName = ref(route.params.modelName);
const car = ref(null); // Informations de la voiture
const specs = ref([]);
const selectedSpec = ref(null);
const reviews = ref([]);
const modifications = ref([]);
const showReviewForm = ref(false);
const showModifForm = ref(false);

// New review form data
const newReview = ref({
  title: "",
  content: "",
  grade: 1,
});

const newModif = ref({
  text: "",
});

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
      selectSpec(specs.value[0]); // Sélectionne la première spec
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des spécifications :", error);
    specs.value = [];
  }
};

// Récupération des reviews pour une spécification sélectionnée
const fetchReviews = async (specId) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/app/reviews/${specId}/`
    );
    reviews.value = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des reviews :", error);
    reviews.value = [];
  }
};

// Sélectionner une spécification et récupérer ses reviews
const selectSpec = (spec) => {
  selectedSpec.value = spec;
  fetchReviews(spec.id);
};

// Charger les données lors du montage
onMounted(async () => {
  await fetchCarDetails();
  await fetchSpecifications();
});

const addReview = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/app/reviews/add/", {
      title: newReview.value.title,
      content: newReview.value.content,
      grade: newReview.value.grade,
      idSpecification: selectedSpec.value.id,
      emailUser: authStore.email,
    });

    reviews.value.push(response.data);

    newReview.value = { title: "", content: "", grade: 1 };
    showReviewForm.value = false;
  } catch (error) {
    console.error("Erreur lors de l'ajout de la review :", error);
  }
};


const addModif = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/app/modifications/add/", {
      text: newModif.value.text,
      modelNameCar: modelName.value,
      emailUserSuggests: authStore.email,
    });

    modifications.value.push(response.data);
    newModif.value = { text: "" };
    showModifForm.value = false;
  } catch (error) {
    console.error("Erreur lors de l'ajout de la proposition de modifications :", error);
  }
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

.reviews-section {
  margin-top: 20px;
}

.reviews-section ul {
  list-style: none;
  padding: 0;
}

.reviews-section li {
  margin-bottom: 10px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  margin-bottom: 15px;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin-bottom: 5px;
}

.modal-content input,
.modal-content textarea {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-content button {
  margin-top: 10px;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-content button:first-of-type {
  background-color: #42b983;
  color: white;
}

.modal-content button:last-of-type {
  background-color: #f44336;
  color: white;
}
</style>
