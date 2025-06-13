<template>
  <div>
    <div
      v-for="ticket in flights"
      :key="ticket.outbound.id + '-' + (ticket.sep ? ticket.sep.id : 'null')"
      class="flex max-w-6xl mx-auto mt-6 bg-white shadow-xl rounded-2xl overflow-hidden"
    >
      <div class="flex flex-col flex-1 border-r border-gray-200">
        <div class="flex items-center justify-between gap-4 px-6 py-4 border-b border-gray-200">
          <FlightCardDetails :ticket="ticket.outbound" />
        </div>
        <div v-if="ticket.sep" class="flex items-center justify-between gap-4 px-6 py-4">
          <FlightCardDetails :ticket="ticket.sep" />
        </div>
      </div>

      <div class="flex flex-col justify-center items-center px-6 py-4 bg-yellow-50 w-48">
        <div class="text-red-500 font-semibold text-sm mb-2 text-center">
          Hurry up! <span class="text-gray-600">The price is about to change!</span>
        </div>
        <button
          @click="goToBookingDetails(ticket)"
          class="bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-6 rounded-xl transition"
        >
          Continue
        </button>
        <div class="text-2xl font-bold text-gray-800 mt-4">
          {{ ticket.price }} ₴
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  flights: {
    type: Array,
    required: true
  }
});

function goToBookingDetails(ticket) {
  // Твоя логіка переходу
}
</script>

<!-- Ось повний код FlightCardDetails, який показує інформацію про рейс -->
<template #FlightCardDetails="{ ticket }">
  <div class="flex flex-col w-full">
    <div class="font-semibold text-lg">{{ ticket.airline }} - Flight №{{ ticket.flight_number }}</div>
    <div class="flex justify-between mt-1">
      <div>
        <div class="text-sm font-medium">From:</div>
        <div>{{ ticket.departure_city }} — {{ ticket.departure_airport }}</div>
        <div class="text-xs text-gray-500">{{ ticket.departure_time }}</div>
      </div>
      <div class="text-center self-center">
        <div class="font-bold">→</div>
        <div class="text-xs text-gray-500">{{ ticket.flight_duration }}</div>
      </div>
      <div>
        <div class="text-sm font-medium">To:</div>
        <div>{{ ticket.arrival_city }} — {{ ticket.arrival_airport }}</div>
        <div class="text-xs text-gray-500">{{ ticket.arrival_time }}</div>
      </div>
    </div>
  </div>
</template>
