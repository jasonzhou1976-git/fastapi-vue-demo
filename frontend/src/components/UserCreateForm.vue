<script setup>
import { reactive } from "vue";

const emit = defineEmits(["create"]);

const newUser = reactive({
  username: "",
  city: "",
  age: "",
});

function submitForm() {
  emit("create", {
    username: newUser.username,
    city: newUser.city,
    age: Number(newUser.age),
  });

  newUser.username = "";
  newUser.city = "";
  newUser.age = "";
}
</script>

<template>
  <form class="create-form" @submit.prevent="submitForm">
    <input v-model="newUser.username" placeholder="username" required>
    <input v-model="newUser.city" placeholder="city" required>
    <input v-model="newUser.age" type="number" placeholder="age" required>
    <button type="submit">Insert UUU</button>
  </form>
</template>

<style scoped>
.create-form {
  display: grid;
  grid-template-columns: 1fr 1fr 120px 120px;
  gap: 8px;
  margin-bottom: 24px;
  max-width: 1000px;
  width: 100%;
}

input {
  padding: 6px;
  width: 100%;
  box-sizing: border-box;
}

button {
  cursor: pointer;
  padding: 6px 10px;
}
</style>
