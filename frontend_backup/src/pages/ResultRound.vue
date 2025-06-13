<script setup>
import HeaderMain from "@/components/HeaderMain.vue";
import FilterVue from "@/components/Flights/FilterVueRound.vue";
import { useFlightSearchStore } from "@/stores/FlightSearchStore";
import axios from "axios";
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";

const store = useFlightSearchStore();
const list = ref({ outbound: [], return: [] });
const filterType = ref(null);
const router = useRouter();

async function askedFlights() {
  const url = `http://localhost:8000/api/b1/flights/flights_sep_return?from_=${encodeURIComponent(
    store.from
  )}&to=${encodeURIComponent(store.to)}&dateGo=${encodeURIComponent(
    store.dateGo
  )}&dateReturn=${encodeURIComponent(store.dateReturn)}`;

  try {
    const response = await axios.get(url);
    list.value = {
      outbound: response.data.outbound || [],
      return: response.data.return || []
    };
  } catch (error) {
    console.error("Error fetching flights:", error.response?.data || error.message);
  }
}

onMounted(() => {
  if (store.from && store.to && store.dateGo && store.dateReturn) {
    askedFlights();
  }
});

function onFilterChanged(type) {
  filterType.value = type;
}

function durationToMinutes(dur) {
  const match = dur.match(/(\d+)h\s*(\d+)m/);
  if (!match) return 9999;
  return parseInt(match[1]) * 60 + parseInt(match[2]);
}

const isConnecting = (flight) => flight.is_connection === true;

const getFlightPrice = (flight) => {
  if (isConnecting(flight)) {
    return flight.first_leg.price + flight.second_leg.price;
  }
  return flight.price;
};

const getFlightDuration = (flight) => {
  if (isConnecting(flight)) {
    return durationToMinutes(flight.first_leg.flight_duration) + durationToMinutes(flight.second_leg.flight_duration);
  }
  return durationToMinutes(flight.flight_duration);
};

const combinedList = computed(() => {
  const combos = [];
  for (const out of list.value.outbound) {
    for (const ret of list.value.return) {
      combos.push({ outbound: out, return: ret });
    }
  }

  if (!filterType.value) return combos;

  if (filterType.value === "cheapest") {
    return combos.sort(
      (a, b) => (getFlightPrice(a.outbound) + getFlightPrice(a.return)) - (getFlightPrice(b.outbound) + getFlightPrice(b.return))
    );
  }

  if (filterType.value === "fastest") {
    return combos.sort(
      (a, b) => (getFlightDuration(a.outbound) + getFlightDuration(a.return)) - (getFlightDuration(b.outbound) + getFlightDuration(b.return))
    );
  }

  if (filterType.value === "best") {
    return combos.sort(
      (a, b) => {
        const aPrice = getFlightPrice(a.outbound) + getFlightPrice(a.return);
        const bPrice = getFlightPrice(b.outbound) + getFlightPrice(b.return);
        const aDur = getFlightDuration(a.outbound) + getFlightDuration(a.return);
        const bDur = getFlightDuration(b.outbound) + getFlightDuration(b.return);
        return aPrice / aDur - bPrice / bDur;
      }
    );
  }

  return combos;
});

function goToBookingDetails(pair) {
  const basePrice = getFlightPrice(pair.outbound) + getFlightPrice(pair.return);
  router.push({
  name: 'BookingDetails',
  query: {
    outboundId: isConnecting(pair.outbound) ? pair.outbound.first_leg.id : pair.outbound.id,
    sepId: isConnecting(pair.outbound) ? pair.outbound.second_leg.id : null,

    returnId: isConnecting(pair.return) ? pair.return.first_leg.id : pair.return.id,
    sepIdReturn: isConnecting(pair.return) ? pair.return.second_leg.id : null,

    basePrice: basePrice
  }
  });
}
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <HeaderMain />
    <FilterVue @filter-changed="onFilterChanged" />

    <div v-if="combinedList.length">
      <div
        v-for="(pair, index) in combinedList"
        :key="index"
        class="flex max-w-6xl mx-auto mt-6 bg-white shadow-xl rounded-2xl overflow-hidden"
      >
        <div class="flex flex-col flex-1 border-r border-gray-200">
          <template v-if="!pair.outbound.is_connection">
            <div class="flex items-center justify-between gap-4 px-6 py-4 border-b border-gray-200">
              <div class="text-gray-500 font-semibold text-right w-32">{{ pair.outbound.departure_date }}</div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.outbound.departure_hours }} {{ pair.outbound.from }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.outbound.departure_airport }}</div>
              </div>
              <div class="flex flex-col items-center text-sm text-gray-600">
                <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
                <span>{{ pair.outbound.flight_duration }}</span>
              </div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.outbound.arrival_hours }} {{ pair.outbound.to }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.outbound.arrival_airport }}</div>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="flex items-center justify-between gap-4 px-6 py-4 border-b border-gray-200">
              <div class="text-gray-500 font-semibold text-right w-32">{{ pair.outbound.first_leg.departure_date }}</div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.outbound.first_leg.departure_hours }} {{ pair.outbound.first_leg.from }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.outbound.first_leg.departure_airport }}</div>
              </div>
              <div class="flex flex-col items-center text-sm text-gray-600">
                <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
                <span>{{ pair.outbound.first_leg.flight_duration }}</span>
              </div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.outbound.first_leg.arrival_hours }} {{ pair.outbound.first_leg.to }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.outbound.first_leg.arrival_airport }}</div>
              </div>
            </div>
            <div class="flex items-center justify-between gap-4 px-6 py-4 border-b border-gray-200">
              <div class="text-gray-500 font-semibold text-right w-32">{{ pair.outbound.second_leg.departure_date }}</div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.outbound.second_leg.departure_hours }} {{ pair.outbound.second_leg.from }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.outbound.second_leg.departure_airport }}</div>
              </div>
              <div class="flex flex-col items-center text-sm text-gray-600">
                <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
                <span>{{ pair.outbound.second_leg.flight_duration }}</span>
              </div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.outbound.second_leg.arrival_hours }} {{ pair.outbound.second_leg.to }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.outbound.second_leg.arrival_airport }}</div>
              </div>
            </div>
          </template>

          <template v-if="!pair.return.is_connection">
            <div class="flex items-center justify-between gap-4 px-6 py-4">
              <div class="text-gray-500 font-semibold text-right w-32">{{ pair.return.departure_date }}</div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.return.departure_hours }} {{ pair.return.from }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.return.departure_airport }}</div>
              </div>
              <div class="flex flex-col items-center text-sm text-gray-600">
                <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
                <span>{{ pair.return.flight_duration }}</span>
              </div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.return.arrival_hours }} {{ pair.return.to }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.return.arrival_airport }}</div>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="flex items-center justify-between gap-4 px-6 py-4">
              <div class="text-gray-500 font-semibold text-right w-32">{{ pair.return.first_leg.departure_date }}</div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.return.first_leg.departure_hours }} {{ pair.return.first_leg.from }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.return.first_leg.departure_airport }}</div>
              </div>
              <div class="flex flex-col items-center text-sm text-gray-600">
                <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
                <span>{{ pair.return.first_leg.flight_duration }}</span>
              </div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.return.first_leg.arrival_hours }} {{ pair.return.first_leg.to }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.return.first_leg.arrival_airport }}</div>
              </div>
            </div>
            <div class="flex items-center justify-between gap-4 px-6 py-4">
              <div class="text-gray-500 font-semibold text-right w-32">{{ pair.return.second_leg.departure_date }}</div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.return.second_leg.departure_hours }} {{ pair.return.second_leg.from }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.return.second_leg.departure_airport }}</div>
              </div>
              <div class="flex flex-col items-center text-sm text-gray-600">
                <img src="/airplane-icon-vector.ico" alt="plane" class="w-6 h-6 mb-1" />
                <span>{{ pair.return.second_leg.flight_duration }}</span>
              </div>
              <div class="text-center flex-1">
                <div class="text-2xl font-bold text-gray-800">
                  {{ pair.return.second_leg.arrival_hours }} {{ pair.return.second_leg.to }}
                </div>
                <div class="text-gray-500 text-sm">{{ pair.return.second_leg.arrival_airport }}</div>
              </div>
            </div>
          </template>
        </div>

        <div class="flex flex-col justify-center items-center px-6 py-4 bg-yellow-50 w-48">
          <div class="text-red-500 font-semibold text-sm mb-2 text-center">
            Hurry up! <span class="text-gray-600">The price is about to change!</span>
          </div>
          <button
            @click="goToBookingDetails(pair)"
            class="bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-6 rounded-xl transition"
          >
            Continue
          </button>
          <div class="text-2xl font-bold text-gray-800 mt-4">
            {{ getFlightPrice(pair.outbound) + getFlightPrice(pair.return) }} ₴
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center mt-10 text-gray-600">
      No flight combinations available.
    </div>
  </div>
</template>
