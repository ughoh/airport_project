<script setup>
import { ref, watch } from 'vue'
import { useFlightSearchStore } from '@/stores/FlightSearchStore'

const store = useFlightSearchStore()
const ticketClass = ref('')

watch(ticketClass, (newVal) => {
  store.setDateReturn(newVal)
})

</script>

<template>
      <div class="flex flex-col">
        <label class="text-gray-700 text-sm mb-1">Class</label>
        <select
            v-model="ticketClass"
          class="px-4 py-2 w-full border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-400"
        >
          <option>Economy</option>
          <option>Business</option>
          <option>First</option>
        </select>
      </div>

</template>