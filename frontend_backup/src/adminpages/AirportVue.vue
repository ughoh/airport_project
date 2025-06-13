<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminHeader from '@/adminpages/AdminHeader.vue'

const API_URL = 'http://localhost:8000/api/b1/airport'

const airports = ref([])
const selectedAirport = ref(null)
const airportForm = ref({
  name: '',
  city: '',
  country: '',
  iata_code: '',
  icao_code: ''
})
const iataQuery = ref('')
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

async function fetchAirports() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/`)
    airports.value = res.data
  } catch {
    error.value = 'Failed to load airports.'
  } finally {
    loading.value = false
  }
}

async function fetchAirportById(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/${id}/`)
    selectedAirport.value = res.data
    airportForm.value = {
      name: res.data.name,
      city: res.data.city,
      country: res.data.country,
      iata_code: res.data.iata_code,
      icao_code: res.data.icao_code
    }
    isEditing.value = true
  } catch {
    error.value = 'Failed to load airport details.'
  } finally {
    loading.value = false
  }
}

async function createAirport() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post(`${API_URL}/`, airportForm.value)
    airports.value.push(res.data)
    resetForm()
  } catch {
    error.value = 'Failed to create airport.'
  } finally {
    loading.value = false
  }
}

async function updateAirport(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.patch(`${API_URL}/update/${id}`, airportForm.value)
    const index = airports.value.findIndex(a => a.id === id)
    if (index !== -1) airports.value[index] = res.data
    resetForm()
  } catch {
    error.value = 'Failed to update airport.'
  } finally {
    loading.value = false
  }
}

async function deleteAirport(id) {
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`${API_URL}/delete/${id}`)
    airports.value = airports.value.filter(a => a.id !== id)
    if (selectedAirport.value?.id === id) resetForm()
  } catch {
    error.value = 'Failed to delete airport.'
  } finally {
    loading.value = false
  }
}

async function searchByIATA() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/get/by_iata`, { params: { iata_code: iataQuery.value } })
    airports.value = res.data
  } catch {
    error.value = 'Search failed.'
  } finally {
    loading.value = false
  }
}

function submitForm() {
  if (isEditing.value && selectedAirport.value) {
    updateAirport(selectedAirport.value.id)
  } else {
    createAirport()
  }
}

function resetForm() {
  airportForm.value = {
    name: '',
    city: '',
    country: '',
    iata_code: '',
    icao_code: ''
  }
  selectedAirport.value = null
  isEditing.value = false
}

onMounted(fetchAirports)
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <AdminHeader />

    <div class="max-w-4xl mx-auto mt-12 space-y-6">
      <h1 class="text-2xl font-bold text-center text-indigo-900 mb-6">🌍 Airport Management</h1>

      <div class="flex justify-center space-x-3">
        <input
          v-model="iataQuery"
          placeholder="🔎 Search by IATA code"
          class="flex-grow max-w-md border border-indigo-400 rounded px-3 py-1 text-indigo-900 placeholder-indigo-500"
        />
        <button
          @click="searchByIATA"
          class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1 rounded font-semibold"
        >
          Search
        </button>
        <button
          @click="fetchAirports"
          class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-1 rounded font-semibold"
        >
          Reset
        </button>
      </div>

      <p v-if="loading" class="text-indigo-700 text-center font-semibold">Loading airports...</p>
      <p v-if="error" class="text-red-600 text-center font-semibold">{{ error }}</p>

      <ul v-if="airports.length" class="space-y-4">
        <li
          v-for="a in airports"
          :key="a.id"
          class="bg-white border border-indigo-400 rounded shadow text-indigo-900 font-medium tracking-wide p-4 flex justify-between items-center"
        >
          <div class="flex flex-wrap gap-6 text-sm md:text-base">
            <div>
              <div class="font-bold text-indigo-800">Name</div>
              <div>{{ a.name }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">City</div>
              <div>{{ a.city }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Country</div>
              <div>{{ a.country }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">IATA</div>
              <div class="uppercase">{{ a.iata_code }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">ICAO</div>
              <div class="uppercase">{{ a.icao_code }}</div>
            </div>
          </div>
          <div class="space-x-4 text-sm">
            <button @click="fetchAirportById(a.id)" class="text-indigo-700 font-semibold hover:underline">
              Edit
            </button>
            <button @click="deleteAirport(a.id)" class="text-red-600 font-semibold hover:underline">
              Delete
            </button>
          </div>
        </li>
      </ul>

      <p v-else class="text-indigo-700 text-center font-semibold">No airports found.</p>

      <div class="bg-white border border-indigo-400 rounded shadow max-w-md mx-auto p-5">
        <h3 class="text-lg font-semibold text-indigo-900 mb-4 text-center">
          {{ isEditing ? 'Edit Airport' : 'Add Airport' }}
        </h3>

        <form @submit.prevent="submitForm" class="flex flex-col space-y-4">
          <input
            v-model="airportForm.name"
            placeholder="Name"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="airportForm.city"
            placeholder="City"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="airportForm.country"
            placeholder="Country"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="airportForm.iata_code"
            placeholder="IATA Code"
            maxlength="3"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400 uppercase"
          />
          <input
            v-model="airportForm.icao_code"
            placeholder="ICAO Code"
            maxlength="4"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400 uppercase"
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

