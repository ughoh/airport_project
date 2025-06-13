<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import axios from "axios";
import HeaderMain from "@/components/HeaderMain.vue";

const list = ref([]);

async function fetchFlights() {
    const response = await axios.get('http://localhost:8000/api/b1/flights/table');
    list.value = response.data;
}

onMounted(() => {
  fetchFlights();

  const interval = setInterval(() => {
    fetchFlights();
  }, 300000);

  onUnmounted(() => {
    clearInterval(interval);
  });
});
</script>

<template>
  <HeaderMain />
  <div class="w-full min-h-screen bg-indigo-100 p-4" style="background-image: url('/bgimage.ico')">
    <div class="max-w-7xl mx-auto mt-2 bg-white shadow-lg rounded-3xl">
    <h2 class="text-2xl font-bold text-indigo-500 rounded-t-3xl bg-indigo-200 text-center p-4">Today's Flight Schedule</h2>
      <div class="overflow-x-auto p-2">
    <table class="min-w-full text-sm text-left text-gray-700 rounded-lg border border-white">
      <thead class="font-bold uppercase bg-white text-indigo-500">
        <tr>
          <th scope="col" class="px-6 py-3">Flight</th>
          <th scope="col" class="px-6 py-3">Route</th>
          <th scope="col" class="px-6 py-3">Departure Time</th>
          <th scope="col" class="px-6 py-3">Arrival Time</th>
          <th scope="col" class="px-6 py-3">Status</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-indigo-100">
        <tr v-for="flight in list" :key="flight.flight_id" class="hover:bg-indigo-50">
          <td class="px-6 py-4 font-bold text-gray-900">{{ flight.flight_number }}</td>
          <td class="px-6 py-4 font-medium text-gray-900">{{ flight.departure_airport_name }} → {{ flight.arrival_airport_name }}</td>
          <td class="px-6 py-4 font-medium text-gray-900">{{ flight.departure_time }}</td>
          <td class="px-6 py-4 font-medium text-gray-900">{{ flight.arrival_time }}</td>
          <td class="px-6 py-4 font-medium"
          :class="{
            'text-green-500': flight.flight_status === 'Planned',
            'text-yellow-500': flight.flight_status === 'Delayed',
            'text-red-600': flight.flight_status === 'Canceled'
          }">{{ flight.flight_status }}
          </td>
        </tr>
      </tbody>
    </table>
      </div>
    </div>
  </div>
</template>
