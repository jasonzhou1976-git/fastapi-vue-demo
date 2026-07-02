<script setup>
import { onMounted, ref } from "vue";
import UserCreateForm from "./components/UserCreateForm.vue";
import UserTable from "./components/UserTable.vue";
import {
  createUser,
  deleteUser,
  getUsers,
  updateUser,
} from "./api/users";

const users = ref([]);
const error = ref("");

async function loadUsers() {
  error.value = "";
  try {
    users.value = await getUsers();
  } catch (err) {
    error.value = err.message;
  }
}

async function handleCreate(user) {
  error.value = "";
  try {
    await createUser(user);
    await loadUsers();
  } catch (err) {
    error.value = err.message;
  }
}

async function handleUpdate(user) {
  error.value = "";
  try {
    await updateUser(user.id, {
      username: user.username,
      city: user.city,
      age: Number(user.age),
    });
    await loadUsers();
  } catch (err) {
    error.value = err.message;
  }
}

async function handleDelete(userId) {
  error.value = "";
  try {
    await deleteUser(userId);
    await loadUsers();
  } catch (err) {
    error.value = err.message;
  }
}

onMounted(loadUsers);
</script>

<template>
  <main>
    <h1>User Management</h1>

    <UserCreateForm @create="handleCreate" />

    <p v-if="error" class="error">{{ error }}</p>

    <UserTable
      :users="users"
      @update="handleUpdate"
      @delete="handleDelete"
    />
  </main>
</template>

<style scoped>
main {
  font-family: Arial, sans-serif;
  margin: 40px;
}

.error {
  color: #b00020;
}
</style>
