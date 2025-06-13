<script setup>
import { ref } from 'vue';
import axios from 'axios';
import HeaderMain from "@/components/HeaderMain.vue";

const mode = ref('login');

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');

function switchMode(newMode) {
  error.value = '';
  mode.value = newMode;
}

function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

async function onSubmit() {
  error.value = '';

  if (!validateEmail(email.value)) {
    error.value = 'Please enter a valid email.';
    return;
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters.';
    return;
  }

  if (mode.value === 'register' && password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.';
    return;
  }

  try {
    if (mode.value === 'login') {
      const params = new URLSearchParams();
      params.append('username', email.value);
      params.append('password', password.value);

      const response = await axios.post(
        'http://127.0.0.1:8000/api/b1/users/login',
        params,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );

      const { role } = response.data;

      localStorage.setItem('userEmail', email.value);
      localStorage.setItem('role', role);
      window.location.href = '/profile';

    } else {
      await axios.post('http://127.0.0.1:8000/api/b1/users/register', {
        email: email.value,
        password: password.value,
      });

      alert('Registered successfully! Please login.');
      switchMode('login');
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Network or server error';
  }
}

const userRole = ref(localStorage.getItem('role'));
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <HeaderMain :role="userRole" />
    <div class="max-w-md mx-auto mt-16 p-8 bg-white rounded-xl shadow-lg">
      <div class="flex justify-center space-x-8 mb-6">
        <button
          :class="mode === 'login' ? 'font-bold border-b-2 border-blue-600' : 'text-gray-500'"
          @click="switchMode('login')"
        >
          Login
        </button>
        <button
          :class="mode === 'register' ? 'font-bold border-b-2 border-blue-600' : 'text-gray-500'"
          @click="switchMode('register')"
        >
          Register
        </button>
      </div>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-gray-700">Email</label>
          <input
            type="email"
            v-model="email"
            placeholder="example@mail.com"
            class="w-full px-3 py-2 border rounded"
            required
          />
        </div>

        <div>
          <label class="block text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            placeholder="minimum 6 characters"
            class="w-full px-3 py-2 border rounded"
            required
          />
        </div>

        <div v-if="mode === 'register'">
          <label class="block text-gray-700">Confirm Password</label>
          <input
            type="password"
            v-model="confirmPassword"
            placeholder="Repeat password"
            class="w-full px-3 py-2 border rounded"
            required
          />
        </div>

        <div v-if="Boolean(error)" class="text-red-500 text-sm">{{ error }}</div>

        <button
          type="submit"
          class="w-full bg-indigo-600 text-white py-2 font-bold rounded hover:bg-blue-700 transition"
        >
          {{ mode === 'login' ? 'Login' : 'Register' }}
        </button>
      </form>
    </div>
  </div>
</template>

