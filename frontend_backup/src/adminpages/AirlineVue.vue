<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminHeader from '@/adminpages/AdminHeader.vue'

const API_URL = 'http://localhost:8000/api/b1/airlines'

const airlines = ref([])
const selectedAirline = ref(null)
const airlineForm = ref({ name: '', code: '', country: '' })
const nameQuery = ref('')
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

async function fetchAirlines() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/`)
    airlines.value = res.data
  } catch {
    error.value = 'Failed to load airlines.'
  } finally {
    loading.value = false
  }
}

async function fetchAirlineById(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/${id}/`)
    selectedAirline.value = res.data
    airlineForm.value = {
      name: res.data.name,
      code: res.data.code,
      country: res.data.country,
    }
    isEditing.value = true
  } catch {
    error.value = 'Failed to load airline details.'
  } finally {
    loading.value = false
  }
}

async function createAirline() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post(`${API_URL}/`, airlineForm.value)
    airlines.value.push(res.data)
    resetForm()
  } catch {
    error.value = 'Failed to create airline.'
  } finally {
    loading.value = false
  }
}

async function updateAirline(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.patch(`${API_URL}/update/${id}`, airlineForm.value)
    const index = airlines.value.findIndex(a => a.id === id)
    if (index !== -1) airlines.value[index] = res.data
    resetForm()
  } catch {
    error.value = 'Failed to update airline.'
  } finally {
    loading.value = false
  }
}

async function deleteAirline(id) {
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`${API_URL}/delete/${id}`)
    airlines.value = airlines.value.filter(a => a.id !== id)
    if (selectedAirline.value?.id === id) resetForm()
  } catch {
    error.value = 'Failed to delete airline.'
  } finally {
    loading.value = false
  }
}

async function searchByName() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/get/by_name`, { params: { name: nameQuery.value } })
    airlines.value = res.data
  } catch {
    error.value = 'Search failed.'
  } finally {
    loading.value = false
  }
}

function submitForm() {
  if (isEditing.value && selectedAirline.value) {
    updateAirline(selectedAirline.value.id)
  } else {
    createAirline()
  }
}

function resetForm() {
  airlineForm.value = { name: '', code: '', country: '' }
  selectedAirline.value = null
  isEditing.value = false
}

onMounted(fetchAirlines)
</script>

<template>
  <div class="w-full min-h-screen bg-blue-100 pb-12">
    <AdminHeader />

    <div class="max-w-4xl mx-auto mt-12 space-y-6">
      <h1 class="text-2xl font-bold text-center text-blue-900 mb-6">🛫 Airline Management</h1>

      <div class="flex justify-center space-x-3">
        <input
          v-model="nameQuery"
          placeholder="🔎 Search by name"
          class="flex-grow max-w-md border border-blue-400 rounded px-3 py-1 text-blue-900 placeholder-blue-500"
        />
        <button
          @click="searchByName"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded font-semibold"
        >
          Search
        </button>
        <button
          @click="fetchAirlines"
          class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-1 rounded font-semibold"
        >
          Reset
        </button>
      </div>

      <p v-if="loading" class="text-blue-700 text-center font-semibold">Loading airlines...</p>
      <p v-if="error" class="text-red-600 text-center font-semibold">{{ error }}</p>

      <ul v-if="airlines.length" class="space-y-4">
        <li
          v-for="a in airlines"
          :key="a.id"
          class="bg-white border border-blue-400 rounded shadow text-blue-900 font-medium tracking-wide p-4 flex justify-between items-center"
        >
          <div class="flex space-x-6 text-sm md:text-base">
            <div>
              <div class="font-bold text-blue-800">Name</div>
              <div>{{ a.name }}</div>
            </div>
            <div>
              <div class="font-bold text-blue-800">Code</div>
              <div>{{ a.code }}</div>
            </div>
            <div>
              <div class="font-bold text-blue-800">Country</div>
              <div>{{ a.country }}</div>
            </div>
          </div>
          <div class="space-x-4 text-sm">
            <button
              @click="fetchAirlineById(a.id)"
              class="text-blue-700 font-semibold hover:underline"
            >
              Edit
            </button>
            <button
              @click="deleteAirline(a.id)"
              class="text-red-600 font-semibold hover:underline"
            >
              Delete
            </button>
          </div>
        </li>
      </ul>

      <p v-else class="text-blue-700 text-center font-semibold">No airlines found.</p>

      <div class="bg-white border border-blue-400 rounded shadow max-w-md mx-auto p-5">
        <h3 class="text-lg font-semibold text-blue-900 mb-4 text-center">
          {{ isEditing ? 'Edit Airline' : 'Add Airline' }}
        </h3>

        <form @submit.prevent="submitForm" class="flex flex-col space-y-4">
          <input
            v-model="airlineForm.name"
            placeholder="Name"
            required
            class="border border-blue-300 rounded px-3 py-1 text-blue-900 placeholder-blue-400"
          />
          <input
            v-model="airlineForm.code"
            placeholder="Code"
            required
            class="border border-blue-300 rounded px-3 py-1 text-blue-900 placeholder-blue-400"
          />
          <input
            v-model="airlineForm.country"
            placeholder="Country"
            required
            class="border border-blue-300 rounded px-3 py-1 text-blue-900 placeholder-blue-400"
          />

          <div class="flex justify-center space-x-4">
            <button
              type="submit"
              class="bg-green-600 hover:bg-green-700 text-white rounded px-6 py-1 font-semibold"
            >
              {{ isEditing ? 'Update' : 'Create' }}
            </button>
            <button
              type="button"
              @click="resetForm"
              class="bg-gray-300 hover:bg-gray-400 text-gray-800 rounded px-6 py-1 font-semibold"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
