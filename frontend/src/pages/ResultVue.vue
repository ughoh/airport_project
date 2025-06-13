<script setup>
import HeaderMain from "@/components/HeaderMain.vue";
import FilterOneWay from "@/components/Flights/FilterOneWay.vue";
import { useFlightSearchStore } from "@/stores/FlightSearchStore";
import axios from "axios";
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const store = useFlightSearchStore();
const list = ref([]);
const filterType = ref(null);
const router = useRouter();

async function askedFlights() {
  const urlDirect = `http://localhost:8000/api/b1/flights/chosen?from_=${encodeURIComponent(store.from)}&to=${encodeURIComponent(store.to)}&dateGo=${encodeURIComponent(store.dateGo)}`;

  try {
    const directResponse = await axios.get(urlDirect);

    if (directResponse.data.length > 0) {
      list.value = directResponse.data.map(item => ({
        type: 'direct',
        price: item.price,
        outbound: item,
        sep: null
      }));
    } else {
      const urlWithConnection = `http://localhost:8000/api/b1/flights/flights_sep?from_=${encodeURIComponent(store.from)}&to=${encodeURIComponent(store.to)}&dateGo=${encodeURIComponent(store.dateGo)}`;
      const connectionResponse = await axios.get(urlWithConnection);
      console.log('Connection flights data:', connectionResponse.data);

      list.value = connectionResponse.data.map(item => ({
        type: 'connection',
        price: item.first_leg.price + item.second_leg.price,
        outbound: item.first_leg,
        sep: item.second_leg
      }));
    }
  } catch (error) {
    console.error("Error fetching flights:", error.response?.data || error.message);
  }
}

onMounted(() => {
  if (store.from && store.to && store.dateGo) {
    askedFlights();
  }
});

function durationToMinutes(dur) {
  const match = dur.match(/(\d+)h\s*(\d+)m/);
  if (!match) return 9999;
  return parseInt(match[1]) * 60 + parseInt(match[2]);
}

const filteredList = computed(() => {
  if (!filterType.value) return list.value;

  const sorted = [...list.value];
  if (filterType.value === "cheapest") {
    return sorted.sort((a, b) => a.price - b.price);
  }

  if (filterType.value === "fastest" || filterType.value === "best") {
    return sorted.sort((a, b) => {
      const aDur = a.sep
        ? durationToMinutes(a.outbound.flight_duration) + durationToMinutes(a.sep.flight_duration)
        : durationToMinutes(a.outbound.flight_duration);
      const bDur = b.sep
        ? durationToMinutes(b.outbound.flight_duration) + durationToMinutes(b.sep.flight_duration)
        : durationToMinutes(b.outbound.flight_duration);

      if (filterType.value === "fastest") return aDur - bDur;
      return (a.price / aDur) - (b.price / bDur);
    });
  }

  return list.value;
});

function goToBookingDetails(ticket) {
  router.push({
    name: "BookingDetails",
    query: {
      outboundId: ticket.outbound.id,
      sepId: ticket.sep ? ticket.sep.id : "",
      basePrice: ticket.price
    }
  });
}

function onFilterChanged() {
}
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <HeaderMain />
    <FilterOneWay v-model="filterType" @filter-changed="onFilterChanged" />

    <div
      v-for="ticket in filteredList"
      :key="ticket.outbound.id || ticket.id"
      class="flex max-w-6xl mx-auto mt-6 bg-white shadow-xl rounded-2xl overflow-hidden"
    >
      <div
        class="flex flex-1 flex-col border-r border-gray-200"
        :class="ticket.type !== 'connection' ? 'justify-center' : ''"
      >
        <div
          v-if="ticket.type !== 'connection'"
          class="flex items-center justify-between gap-4 px-8 py-5"
          style="min-height: 150px;"
        >
          <div class="text-gray-500 font-semibold text-right w-32">
            {{ ticket.outbound.departure_date }}
          </div>

          <div class="text-center flex-1">
            <div class="text-2xl font-bold text-gray-800">
              {{ ticket.outbound.departure_hours }} {{ ticket.outbound.from }}
            </div>
            <div class="text-gray-500 text-sm">
              {{ ticket.outbound.departure_airport }}
            </div>
          </div>

          <div class="flex flex-col items-center text-sm text-gray-600">
            <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
            <span>{{ ticket.outbound.flight_duration }}</span>
          </div>

          <div class="text-center flex-1">
            <div class="text-2xl font-bold text-gray-800">
              {{ ticket.outbound.arrival_hours }} {{ ticket.outbound.to }}
            </div>
            <div class="text-gray-500 text-sm">
              {{ ticket.outbound.arrival_airport }}
            </div>
          </div>
        </div>

        <div v-if="ticket.type === 'connection'" class="flex flex-col gap-2 border-t border-gray-200 px-8 py-5">
          <div
            v-for="(leg, i) in [ticket.outbound, ticket.sep]"
            :key="leg.id || i"
            class="flex items-center justify-between gap-4"
          >
            <div class="text-gray-500 font-semibold text-right w-32">
              {{ leg.departure_date }}
            </div>
            <div class="text-center flex-1">
              <div class="text-2xl font-bold text-gray-800">
                {{ leg.departure_hours }} {{ leg.from }}
              </div>
              <div class="text-gray-500 text-sm">
                {{ leg.departure_airport }}
              </div>
            </div>
            <div class="flex flex-col items-center text-sm text-gray-600">
              <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
              <span>{{ leg.flight_duration }}</span>
            </div>
            <div class="text-center flex-1">
              <div class="text-2xl font-bold text-gray-800">
                {{ leg.arrival_hours }} {{ leg.to }}
              </div>
              <div class="text-gray-500 text-sm">
                {{ leg.arrival_airport }}
              </div>
            </div>
          </div>
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

    <div v-if="filteredList.length === 0" class="text-center mt-10 text-gray-600">
      No flights available.
    </div>
  </div>
</template>
