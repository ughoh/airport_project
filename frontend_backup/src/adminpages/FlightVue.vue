<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminHeader from '@/adminpages/AdminHeader.vue'

const API_URL = 'http://localhost:8000/api/b1/flights'

const flights = ref([])
const selectedFlight = ref(null)
const flightForm = ref({
  airline_id: null,
  flight_number: '',
  aircraft_id: null,
  departure_airport_id: null,
  arrival_airport_id: null,
  departure_time: '',
  arrival_time: '',
  status: '',
  price: 0
})

const flightNumberQuery = ref('')
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

async function fetchFlights() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/table`)
    flights.value = res.data
  } catch {
    error.value = 'Failed to load flights.'
  } finally {
    loading.value = false
  }
}

async function fetchFlightById(id) {
  if (!id) {
    error.value = 'Invalid flight id'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/${id}`)
    selectedFlight.value = res.data
    flightForm.value = {
      airline_id: res.data.airline_id,
      flight_number: res.data.flight_number,
      aircraft_id: res.data.aircraft_id,
      departure_airport_id: res.data.departure_airport_id,
      arrival_airport_id: res.data.arrival_airport_id,
      departure_time: res.data.departure_time,
      arrival_time: res.data.arrival_time,
      status: res.data.status,
      price: res.data.price
    }
    isEditing.value = true
  } catch {
    error.value = 'Failed to load flight details.'
  } finally {
    loading.value = false
  }
}

async function updateFlight(id) {
  if (!id) {
    error.value = 'Invalid flight id'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const res = await axios.put(`${API_URL}/${id}`, flightForm.value)
    const index = flights.value.findIndex(f => f.id === id)
    if (index !== -1) flights.value[index] = res.data
    resetForm()
  } catch {
    error.value = 'Failed to update flight.'
  } finally {
    loading.value = false
  }
}

async function deleteFlight(id) {
  if (!id) {
    error.value = 'Invalid flight id'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`${API_URL}/${id}`)
    flights.value = flights.value.filter(f => f.id !== id)
    if (selectedFlight.value?.id === id) resetForm()
  } catch {
    error.value = 'Failed to delete flight.'
  } finally {
    loading.value = false
  }
}

async function createFlight() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post(`${API_URL}/`, flightForm.value)
    flights.value.push(res.data)
    resetForm()
  } catch {
    error.value = 'Failed to create flight.'
  } finally {
    loading.value = false
  }
}

async function searchByFlightNumber() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/search`, { params: { flight_number: flightNumberQuery.value } })
    flights.value = res.data
  } catch {
    error.value = 'Search failed.'
  } finally {
    loading.value = false
  }
}

function submitForm() {
  if (isEditing.value && selectedFlight.value) {
    updateFlight(selectedFlight.value.id)
  } else {
    createFlight()
  }
}

function resetForm() {
  flightForm.value = {
    airline_id: null,
    flight_number: '',
    aircraft_id: null,
    departure_airport_id: null,
    arrival_airport_id: null,
    departure_time: '',
    arrival_time: '',
    status: '',
    price: 0
  }
  selectedFlight.value = null
  isEditing.value = false
}

onMounted(fetchFlights)
</script>



<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <AdminHeader />

    <div class="max-w-5xl mx-auto mt-12 space-y-6">
      <h1 class="text-2xl font-bold text-center text-indigo-900 mb-6">✈️ Flight Management</h1>

      <div class="flex justify-center space-x-3">
        <input
          v-model="flightNumberQuery"
          placeholder="🔎 Search by flight number"
          class="flex-grow max-w-md border border-indigo-400 rounded px-3 py-1 text-indigo-900 placeholder-indigo-500"
        />
        <button
          @click="searchByFlightNumber"
          class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1 rounded font-semibold"
        >
          Search
        </button>
        <button
          @click="fetchFlights"
          class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-1 rounded font-semibold"
        >
          Reset
        </button>
      </div>

      <p v-if="loading" class="text-indigo-700 text-center font-semibold">Loading flights...</p>
      <p v-if="error" class="text-red-600 text-center font-semibold">{{ error }}</p>

      <ul v-if="flights.length" class="space-y-4">
        <li
          v-for="f in flights"
          :key="f.id"
          class="bg-white border border-indigo-400 rounded shadow text-indigo-900 font-medium tracking-wide p-4 flex justify-between items-center"
        >
          <div class="flex flex-wrap gap-6 text-sm md:text-base">
            <div>
              <div class="font-bold text-indigo-800">Flight Number</div>
              <div>{{ f.flight_number }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Airline ID</div>
              <div>{{ f.airline_id }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Aircraft ID</div>
              <div>{{ f.aircraft_id }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Departure Airport ID</div>
              <div>{{ f.departure_airport_id }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Arrival Airport ID</div>
              <div>{{ f.arrival_airport_id }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Departure Time</div>
              <div>{{ f.departure_time }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Arrival Time</div>
              <div>{{ f.arrival_time }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Status</div>
              <div>{{ f.status }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Price</div>
              <div>{{ f.price }}</div>
            </div>
          </div>
          <div class="space-x-4 text-sm">
            <button @click="fetchFlightById(f.id)" class="text-indigo-700 font-semibold hover:underline">
              Edit
            </button>
            <button @click="deleteFlight(f.id)" class="text-red-600 font-semibold hover:underline">
              Delete
            </button>
          </div>
        </li>
      </ul>

      <p v-else class="text-indigo-700 text-center font-semibold">No flights found.</p>

      <div class="bg-white border border-indigo-400 rounded shadow max-w-lg mx-auto p-5">
        <h3 class="text-lg font-semibold text-indigo-900 mb-4 text-center">
          {{ isEditing ? 'Edit Flight' : 'Add Flight' }}
        </h3>

        <form @submit.prevent="submitForm" class="flex flex-col space-y-4">
          <input
            v-model.number="flightForm.airline_id"
            type="number"
            placeholder="Airline ID"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="flightForm.flight_number"
            placeholder="Flight Number"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model.number="flightForm.aircraft_id"
            type="number"
            placeholder="Aircraft ID"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model.number="flightForm.departure_airport_id"
            type="number"
            placeholder="Departure Airport ID"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model.number="flightForm.arrival_airport_id"
            type="number"
            placeholder="Arrival Airport ID"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="flightForm.departure_time"
            type="datetime-local"
            placeholder="Departure Time"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="flightForm.arrival_time"
            type="datetime-local"
            placeholder="Arrival Time"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="flightForm.status"
            placeholder="Status"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model.number="flightForm.price"
            type="number"
            min="0"
            placeholder="Price"
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
