<template>
  <div class="admin-modifications">
    <header class="main-header">
        <div v-if="authStore.isLoggedIn" class="user-info">
        <p>Connecté en tant que : <strong>{{ authStore.username }}</strong></p>
      </div>
      <h1>Gestion des Modifications</h1>
    </header>

    <main v-if="modifications.length > 0" class="main-content">
      <section class="modifications-list">
        <h2>Liste des Modifications</h2>
        <ul>
          <li v-for="modification in modifications" :key="modification.id" class="modification-item">
            <p><strong>Voiture :</strong> {{ modification.modelNameCar }}</p>
            <p><strong>Proposition :</strong> {{ modification.text }}</p>
            <p><strong>Proposée par :</strong> {{ modification.emailUserSuggests }}</p>
            <p><strong>Statut :</strong> {{ modification.isAccepted === null ? 'En attente' : (modification.isAccepted ? 'Acceptée' : 'Rejetée') }}</p>
            <div class="actions">
              <button v-if="modification.isAccepted === null" @click="updateModification(modification.id, true)">
                Accepter
              </button>
              <button v-if="modification.isAccepted === null" @click="updateModification(modification.id, false)">
                Rejeter
              </button>
            </div>
          </li>
        </ul>
      </section>
    </main>

    <p v-else class="no-modifications-message">
      Aucune modification à afficher.
    </p>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { authStore } from "../store";

const modifications = ref([]);

// Fonction pour récupérer les modifications
const fetchModifications = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/app/modifications/", {
      headers: {
        "X-User-Email": authStore.email, // Ajoute l'email à l'en-tête
      },
    });
    modifications.value = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des modifications :", error);
  }
};

// Fonction pour mettre à jour une modification
const updateModification = async (id, isAccepted) => {
  try {
    await axios.put(
      `http://127.0.0.1:8000/app/modifications/${id}/`,
      {
        isAccepted,
        emailUserManages: authStore.email,
      },
      {
        headers: {
          "X-User-Email": authStore.email, // Ajoute l'email à l'en-tête
        },
      }
    );
    await fetchModifications(); // Rafraîchit la liste après modification
  } catch (error) {
    console.error("Erreur lors de la mise à jour de la modification :", error);
  }
};

// Charger les modifications au montage
onMounted(async () => {
  await fetchModifications();
});
</script>

<style scoped>
.admin-modifications {
  font-family: Arial, sans-serif;
  padding: 20px;
}

.main-header {
  text-align: center;
  background-color: #42b983;
  color: white;
  padding: 10px;
  margin-bottom: 20px;
}

.modifications-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modification-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.actions {
  margin-top: 10px;
}

button {
  margin-right: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #ddd;
}

/* Styles pour les logs */
.logs {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.logs h2 {
  margin-bottom: 10px;
}

.log-item {
  margin-bottom: 10px;
  font-size: 14px;
  color: #333;
}
</style>
