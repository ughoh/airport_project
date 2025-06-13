<script setup>
import { useRouter } from 'vue-router'
import { useFlightSearchStore } from '@/stores/FlightSearchStore'

const router = useRouter()
const store = useFlightSearchStore()

const search = async () => {
  if (!store.from || !store.to) {
    alert('"From" or "To" are not defined')
    return
  }

  if (!store.dateGo) {
    alert('Departure date not defined')
    return
  }

  if (store.ticketType === 'roundtrip' && !store.dateReturn) {
    alert('Return date not defined')
    return
  }

  if (store.ticketType === 'roundtrip') {
    await router.push('/results_round')
  }
  else await router.push('/results')

}
</script>

<template>
      <div class="flex flex-col">
        <button
          type="button"
          @click="search"
          class="w-full bg-indigo-600 text-white text-2xl font-semibold px-6 py-2 rounded-lg shadow-md transition"
        >
          Search
        </button>
      </div>
</template>