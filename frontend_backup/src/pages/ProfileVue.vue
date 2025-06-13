<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import HeaderMain from "@/components/HeaderMain.vue";

const router = useRouter();

const email = ref('');
const role = ref('');
const error = ref('');

onMounted(() => {
  const storedEmail = localStorage.getItem('userEmail');
  const storedRole = localStorage.getItem('role');

  if (!storedEmail || !storedRole) {
    router.push('/auth');
    return;
  }

  email.value = storedEmail;
  role.value = storedRole;
});

function logout() {
  localStorage.removeItem('userEmail');
  localStorage.removeItem('role');
  router.push('/auth');
}
</script>


<template>
  <div class="w-full min-h-screen bg-indigo-100">
    <HeaderMain />
    <div class="max-w-md mx-auto mt-16 p-8 bg-white rounded-xl shadow-lg">
      <h1 class="text-2xl font-bold mb-4">Profile</h1>
      <p><strong>Email:</strong> {{ email }}</p>

      <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>

      <div class="mt-6">
        <router-link
          v-if="role === 'admin'"
          to="/admin"
          class="text-indigo-700 font-semibold hover:underline"
        >
          Admin Panel
        </router-link>
      </div>

      <div class="mt-4">
        <router-link
          v-if="role !== 'admin'"
          to="/tickets"
          class="text-indigo-700 font-semibold hover:underline"
        >
          My tickets
        </router-link>
      </div>

      <button
        @click="logout"
        class="mt-8 w-full bg-red-600 text-white py-2 rounded hover:bg-red-700 transition"
      >
        Logout
      </button>
    </div>
  </div>
</template>
