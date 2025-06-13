<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminHeader from '@/adminpages/AdminHeader.vue'

const API_URL = 'http://localhost:8000/api/b1/aircrafts'

const aircrafts = ref([])
const selectedAircraft = ref(null)
const aircraftForm = ref({ model: '', capacity: 0, registration_number: '' })
const modelQuery = ref('')
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

async function fetchAircrafts() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/`)
    aircrafts.value = res.data
  } catch {
    error.value = 'Failed to load aircrafts.'
  } finally {
    loading.value = false
  }
}

async function fetchAircraftById(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/${id}/`)
    selectedAircraft.value = res.data
    aircraftForm.value = {
      model: res.data.model,
      capacity: res.data.capacity,
      registration_number: res.data.registration_number,
    }
    isEditing.value = true
  } catch {
    error.value = 'Failed to load aircraft details.'
  } finally {
    loading.value = false
  }
}

async function createAircraft() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post(`${API_URL}/`, aircraftForm.value)
    aircrafts.value.push(res.data)
    resetForm()
  } catch {
    error.value = 'Failed to create aircraft.'
  } finally {
    loading.value = false
  }
}

async function updateAircraft(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.patch(`${API_URL}/update/${id}`, aircraftForm.value)
    const index = aircrafts.value.findIndex(a => a.id === id)
    if (index !== -1) aircrafts.value[index] = res.data
    resetForm()
  } catch {
    error.value = 'Failed to update aircraft.'
  } finally {
    loading.value = false
  }
}

async function deleteAircraft(id) {
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`${API_URL}/delete/${id}`)
    aircrafts.value = aircrafts.value.filter(a => a.id !== id)
    if (selectedAircraft.value?.id === id) resetForm()
  } catch {
    error.value = 'Failed to delete aircraft.'
  } finally {
    loading.value = false
  }
}

async function searchByModel() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/get/param`, { params: { model: modelQuery.value } })
    aircrafts.value = res.data
  } catch {
    error.value = 'Search failed.'
  } finally {
    loading.value = false
  }
}

function submitForm() {
  if (isEditing.value && selectedAircraft.value) {
    updateAircraft(selectedAircraft.value.id)
  } else {
    createAircraft()
  }
}

function resetForm() {
  aircraftForm.value = { model: '', capacity: 0, registration_number: '' }
  selectedAircraft.value = null
  isEditing.value = false
}

onMounted(fetchAircrafts)
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <AdminHeader />

    <div class="max-w-4xl mx-auto mt-12 space-y-6">
  <h1 class="text-2xl font-bold text-center text-indigo-900 mb-6">✈️ Aircraft Management</h1>

  <div class="flex justify-center space-x-3">
    <input
      v-model="modelQuery"
      placeholder="🔎 Search by model"
      class="flex-grow max-w-md border border-indigo-400 rounded px-3 py-1 text-indigo-900 placeholder-indigo-500"
    />
    <button
      @click="searchByModel"
      class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1 rounded font-semibold"
    >
      Search
    </button>
    <button
      @click="fetchAircrafts"
      class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-1 rounded font-semibold"
    >
      Reset
    </button>
  </div>

  <p v-if="loading" class="text-indigo-700 text-center font-semibold">Loading aircrafts...</p>
  <p v-if="error" class="text-red-600 text-center font-semibold">{{ error }}</p>

  <ul v-if="aircrafts.length" class="space-y-4">
    <li
      v-for="a in aircrafts"
      :key="a.id"
      class="bg-white border border-indigo-400 rounded shadow text-indigo-900 font-medium tracking-wide p-4 flex justify-between items-center"
    >
      <div class="flex space-x-6 text-sm md:text-base">
        <div>
          <div class="font-bold text-indigo-800">Model</div>
          <div class="uppercase">{{ a.model }}</div>
        </div>
        <div>
          <div class="font-bold text-indigo-800">Capacity</div>
          <div>{{ a.capacity }} seats</div>
        </div>
        <div>
          <div class="font-bold text-indigo-800">Registration #</div>
          <div class="uppercase">{{ a.registration_number }}</div>
        </div>
      </div>
      <div class="space-x-4 text-sm">
        <button
          @click="fetchAircraftById(a.id)"
          class="text-indigo-700 font-semibold hover:underline"
        >
          Edit
        </button>
        <button
          @click="deleteAircraft(a.id)"
          class="text-red-600 font-semibold hover:underline"
        >
          Delete
        </button>
      </div>
    </li>
  </ul>

  <p v-else class="text-indigo-700 text-center font-semibold">No aircrafts found.</p>

  <div class="bg-white border border-indigo-400 rounded shadow max-w-md mx-auto p-5">
    <h3 class="text-lg font-semibold text-indigo-900 mb-4 text-center">
      {{ isEditing ? 'Edit Aircraft' : 'Add Aircraft' }}
    </h3>

    <form @submit.prevent="submitForm" class="flex flex-col space-y-4">
      <input
        v-model="aircraftForm.model"
        placeholder="Model"
        required
        class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
      />
      <input
        v-model.number="aircraftForm.capacity"
        placeholder="Capacity"
        type="number"
        min="1"
        required
        class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
      />
      <input
        v-model="aircraftForm.registration_number"
        placeholder="Registration Number"
        required
        class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
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