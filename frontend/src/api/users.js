const API_BASE_URL = "";


async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}


export function getUsers() {
  return request("/api/users");
}


export function createUser(user) {
  return request("/api/users", {
    method: "POST",
    body: JSON.stringify(user),
  });
}


export function updateUser(id, user) {
  return request(`/api/users/${id}`, {
    method: "PUT",
    body: JSON.stringify(user),
  });
}


export function deleteUser(id) {
  return request(`/api/users/${id}`, {
    method: "DELETE",
  });
}
