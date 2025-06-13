<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminHeader from '@/adminpages/AdminHeader.vue'

const API_URL = 'http://localhost:8000/api/b1/employees'

const employees = ref([])
const selectedEmployee = ref(null)
const employeeForm = ref({
  first_name: '',
  last_name: '',
  position: '',
  departament: '',
  contact_info: ''
})
const nameQuery = ref('')
const isEditing = ref(false)
const loading = ref(false)
const error = ref('')

const departments = [
  'Security',
  'Check-In',
  'Boarding',
  'Maintenance',
  'Air Traffic Control',
  'Baggage Handling',
  'Customs',
  'Cleaning',
  'Administration',
  'Catering'
]

async function fetchEmployees() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/`)
    employees.value = res.data
  } catch {
    error.value = 'Failed to load employees.'
  } finally {
    loading.value = false
  }
}

async function fetchEmployeeById(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/${id}/`)
    selectedEmployee.value = res.data
    employeeForm.value = {
      first_name: res.data.first_name,
      last_name: res.data.last_name,
      position: res.data.position,
      departament: res.data.departament,
      contact_info: res.data.contact_info
    }
    isEditing.value = true
  } catch {
    error.value = 'Failed to load employee details.'
  } finally {
    loading.value = false
  }
}

async function createEmployee() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post(`${API_URL}/`, employeeForm.value)
    employees.value.push(res.data)
    resetForm()
  } catch {
    error.value = 'Failed to create employee.'
  } finally {
    loading.value = false
  }
}

async function updateEmployee(id) {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.patch(`${API_URL}/update/${id}`, employeeForm.value)
    const index = employees.value.findIndex(e => e.id === id)
    if (index !== -1) employees.value[index] = res.data
    resetForm()
  } catch {
    error.value = 'Failed to update employee.'
  } finally {
    loading.value = false
  }
}

async function deleteEmployee(id) {
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`${API_URL}/delete/${id}`)
    employees.value = employees.value.filter(e => e.id !== id)
    if (selectedEmployee.value?.id === id) resetForm()
  } catch {
    error.value = 'Failed to delete employee.'
  } finally {
    loading.value = false
  }
}

async function searchByEmail() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/get/by_name`, { params: { name: nameQuery.value } })
    employees.value = res.data
  } catch {
    error.value = 'Search failed.'
  } finally {
    loading.value = false
  }
}

function submitForm() {
  if (isEditing.value && selectedEmployee.value) {
    updateEmployee(selectedEmployee.value.id)
  } else {
    createEmployee()
  }
}

function resetForm() {
  employeeForm.value = {
    first_name: '',
    last_name: '',
    position: '',
    departament: '',
    contact_info: ''
  }
  selectedEmployee.value = null
  isEditing.value = false
}

onMounted(fetchEmployees)
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <AdminHeader />

    <div class="max-w-4xl mx-auto mt-12 space-y-6">
      <h1 class="text-2xl font-bold text-center text-indigo-900 mb-6">👨‍💼 Employee Management</h1>

      <div class="flex justify-center space-x-3">
        <input
          v-model="nameQuery"
          placeholder="🔎 Search by email"
          class="flex-grow max-w-md border border-indigo-400 rounded px-3 py-1 text-indigo-900 placeholder-indigo-500"
        />
        <button
          @click="searchByEmail"
          class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1 rounded font-semibold"
        >
          Search
        </button>
        <button
          @click="fetchEmployees"
          class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-1 rounded font-semibold"
        >
          Reset
        </button>
      </div>

      <p v-if="loading" class="text-indigo-700 text-center font-semibold">Loading employees...</p>
      <p v-if="error" class="text-red-600 text-center font-semibold">{{ error }}</p>

      <ul v-if="employees.length" class="space-y-4">
        <li
          v-for="e in employees"
          :key="e.id"
          class="bg-white border border-indigo-400 rounded shadow text-indigo-900 font-medium tracking-wide p-4 flex justify-between items-center"
        >
          <div class="flex flex-wrap gap-6 text-sm md:text-base">
            <div>
              <div class="font-bold text-indigo-800">Name</div>
              <div>{{ e.first_name }} {{ e.last_name }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Position</div>
              <div>{{ e.position }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Departament</div>
              <div>{{ e.departament }}</div>
            </div>
            <div>
              <div class="font-bold text-indigo-800">Contact</div>
              <div>{{ e.contact_info }}</div>
            </div>
          </div>
          <div class="space-x-4 text-sm">
            <button @click="fetchEmployeeById(e.id)" class="text-indigo-700 font-semibold hover:underline">
              Edit
            </button>
            <button @click="deleteEmployee(e.id)" class="text-red-600 font-semibold hover:underline">
              Delete
            </button>
          </div>
        </li>
      </ul>

      <p v-else class="text-indigo-700 text-center font-semibold">No employees found.</p>

      <div class="bg-white border border-indigo-400 rounded shadow max-w-md mx-auto p-5">
        <h3 class="text-lg font-semibold text-indigo-900 mb-4 text-center">
          {{ isEditing ? 'Edit Employee' : 'Add Employee' }}
        </h3>

        <form @submit.prevent="submitForm" class="flex flex-col space-y-4">
          <input
            v-model="employeeForm.first_name"
            placeholder="First Name"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="employeeForm.last_name"
            placeholder="Last Name"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <input
            v-model="employeeForm.position"
            placeholder="Position"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900 placeholder-indigo-400"
          />
          <select
            v-model="employeeForm.departament"
            required
            class="border border-indigo-300 rounded px-3 py-1 text-indigo-900"
          >
            <option value="" disabled selected>Select Departament</option>
            <option v-for="d in departments" :key="d" :value="d">{{ d }}</option>
          </select>
          <input
            v-model="employeeForm.contact_info"
            placeholder="Contact Info"
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
