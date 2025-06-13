<template>
  <div class="grid grid-cols-12 gap-y-1 gap-x-1">
    <div class="col-span-6"><span class="font-semibold">Carrier:</span> {{ flight.airline }}</div>
    <div class="col-span-3"><span class="font-semibold">Flight №:</span> {{ flight.flight_number }}</div>
    <div class="col-span-3"><span class="font-semibold">Class:</span> {{ ticketClass }}</div>

    <div class="col-span-6"><span class="font-semibold">From:</span> {{ flight.departure_city }}</div>
    <div class="col-span-6"><span class="font-semibold">To:</span> {{ flight.arrival_city }}</div>

    <div class="col-span-3"><span class="font-semibold">Date:</span> {{ flight.departure_time }}</div>
    <div class="col-span-3"></div>

    <div class="col-span-3">
      <div class="font-semibold">Gate</div>
      <div class="text-indigo-700 font-black text-xl">K18</div>
    </div>
    <div class="col-span-3">
      <div class="font-semibold">Boarding Time</div>
      <div class="text-indigo-700 font-black text-xl">{{ flight.departure_time }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  flight: Object,
  ticketClass: String,
});
</script>
