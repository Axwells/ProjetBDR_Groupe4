<template>
  <div class="admin-users">
    <header class="main-header">
      <h1>Gestion des Utilisateurs</h1>
    </header>

    <main>
      <!-- Liste des utilisateurs -->
      <section>
        <h2>Liste des Utilisateurs</h2>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Nom d'utilisateur</th>
              <th>Super Admin</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.email">
              <td>{{ user.email }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.isSuperUser ? "Oui" : "Non" }}</td>
              <td>
                <button @click="editUser(user)">Modifier</button>
                <button @click="deleteUser(user.email)">Supprimer</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Formulaire d'ajout/modification -->
      <section>
        <h2>{{ isEditing ? "Modifier l'utilisateur" : "Ajouter un utilisateur" }}</h2>
        <form @submit.prevent="isEditing ? updateUser() : createUser()">
          <input v-model="form.email" type="email" placeholder="Email" :disabled="isEditing" required />
          <input v-model="form.username" type="text" placeholder="Nom d'utilisateur" required />
          <input v-model="form.password" type="password" placeholder="Mot de passe" :required="!isEditing" />
          <label>
            <input v-model="form.isSuperUser" type="checkbox" /> Super Admin
          </label>
          <button type="submit">{{ isEditing ? "Modifier" : "Ajouter" }}</button>
        </form>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const users = ref([]);
const form = ref({ email: "", username: "", password: "", isSuperUser: false });
const isEditing = ref(false);

// Charger les utilisateurs
const fetchUsers = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/app/users/");
    users.value = response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des utilisateurs :", error);
  }
};

// Créer un utilisateur
const createUser = async () => {
  try {
    await axios.post("http://127.0.0.1:8000/app/users/add/", { ...form.value });
    alert("Utilisateur ajouté avec succès !");
    resetForm();
    fetchUsers();
  } catch (error) {
    console.error("Erreur lors de l'ajout de l'utilisateur :", error);
  }
};

// Modifier un utilisateur
const updateUser = async () => {
  try {
    await axios.put(`http://127.0.0.1:8000/app/users/update/${form.value.email}/`, {
      username: form.value.username,
      isSuperUser: form.value.isSuperUser,
    });
    alert("Utilisateur modifié avec succès !");
    resetForm();
    fetchUsers();
  } catch (error) {
    console.error("Erreur lors de la modification de l'utilisateur :", error);
  }
};

// Supprimer un utilisateur
const deleteUser = async (email) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/app/users/delete/${email}/`);
    alert("Utilisateur supprimé avec succès !");
    fetchUsers();
  } catch (error) {
    console.error("Erreur lors de la suppression de l'utilisateur :", error);
  }
};

// Préparer le formulaire pour l'édition
const editUser = (user) => {
  form.value = { ...user, password: "" }; // Reset password field
  isEditing.value = true;
};

// Réinitialiser le formulaire
const resetForm = () => {
  form.value = { email: "", username: "", password: "", isSuperUser: false };
  isEditing.value = false;
};

// Charger les données au montage
onMounted(fetchUsers);
</script>

<style scoped>
/* Styles de base pour la page Admin */
.admin-users {
  padding: 20px;
}

.main-header {
  background-color: #42b983;
  color: white;
  text-align: center;
  padding: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 10px;
  text-align: left;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
