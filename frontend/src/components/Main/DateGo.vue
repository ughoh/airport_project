<script setup>
import { ref, watch } from 'vue'
import { useFlightSearchStore } from '@/stores/FlightSearchStore'

const store = useFlightSearchStore()
const dateGo = ref('')

watch(dateGo, (newVal) => {
  store.setDateGo(newVal)
})

</script>

<template>
  <div class="flex flex-col">
    <label class="text-indigo-500 text-sm font-bold mb-2">Departure</label>
    <input
      type="date"
      v-model="dateGo"
      class="px-4 py-2.5 w-full border border-gray-300 rounded-xl shadow-sm bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200"
    />
  </div>
</template>

