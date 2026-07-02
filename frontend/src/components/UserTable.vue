<script setup>
defineProps({
  users: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["update", "delete"]);
</script>

<template>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Username</th>
        <th>City</th>
        <th>Age</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="user in users" :key="user.id">
        <td>{{ user.id }}</td>
        <td><input v-model="user.username"></td>
        <td><input v-model="user.city"></td>
        <td><input v-model="user.age" type="number"></td>
        <td class="actions">
          <button type="button" @click="emit('update', user)">Update</button>
          <button type="button" class="danger" @click="emit('delete', user.id)">
            Delete
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
table {
  border-collapse: collapse;
  max-width: 1000px;
  width: 100%;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px 12px;
  text-align: left;
}

th {
  background:rgb(194, 205, 246);
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

.actions {
  display: flex;
  gap: 8px;
}

.danger {
  color: #b00020;
}
</style>
