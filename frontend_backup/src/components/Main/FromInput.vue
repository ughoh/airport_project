<script setup>
import {onMounted, ref, watch} from 'vue'
import axios from "axios";
import { useFlightSearchStore } from '@/stores/FlightSearchStore'

const fromInput = ref('')
const suggestions = ref([])
const isSelecting = ref(false)
const list = ref([])

const store = useFlightSearchStore()

onMounted(async () => {
  const response = await axios.get('http://localhost:8000/api/b1/airport/')
  list.value = response.data
})

watch(fromInput, async (newVal) => {

  if (isSelecting.value) {
    isSelecting.value = false
    return
  }

  if (newVal.length >= 1) {
    suggestions.value = list.value.filter(airport =>
        airport.city.toLowerCase().includes(newVal.toLowerCase()) ||
        airport.iata_code.toLowerCase().includes(newVal.toLowerCase())
      ).map(airport => ({
      label: `${airport.city} (${airport.iata_code})`,
      id: airport.id
    }))
  } else {
    suggestions.value = []
  }
})

const selectOption = (option) => {
    isSelecting.value = true
    fromInput.value = option.label
    store.setFrom(option.label)
    suggestions.value = []
}

</script>

<template>
  <div class="relative w-full">
    <label class="text-indigo-500 text-sm font-bold mb-2 block">From</label>
    <input
      type="text"
      v-model="fromInput"
      placeholder="Enter city or airport"
      class="w-full px-4 py-2.5 rounded-xl border border-gray-300 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-500 transition duration-200"
    />

    <ul
      v-if="suggestions.length"
      class="absolute z-20 w-full mt-2 bg-white border border-gray-200 rounded-xl shadow-lg max-h-60 overflow-y-auto"
    >
      <li
        v-for="option in suggestions"
        :key="option.id"
        @click="selectOption(option)"
        class="px-4 py-2 hover:bg-indigo-50 cursor-pointer transition-colors duration-150"
      >
        {{ option.label }}
      </li>
    </ul>
  </div>
</template>
