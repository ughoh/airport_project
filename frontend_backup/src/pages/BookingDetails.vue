<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import HeaderMain from "@/components/HeaderMain.vue";

const route = useRoute();
const router = useRouter();

const outboundId = route.query.outboundId;
const returnId = route.query.returnId || null;
const sepId = route.query.sepId || null;
const sepIdReturn = route.query.sepIdReturn || null;
const basePriceFromQuery = Number(route.query.basePrice);

const outboundFlight = ref(null);
const sepFlight = ref(null);
const returnFlight = ref(null);
const sepFlightReturn = ref(null);

const firstName = ref('');
const lastName = ref('');
const passengers = ref(1);
const ticketClass = ref('economy');
const error = ref('');
const loading = ref(false);
const userEmail = ref('');

const classPriceAdd = {
  economy: 0,
  business: 250,
  first: 500,
};

async function fetchFlight(id, direction = 'outbound') {
  if (!id) return null;

  const url = `http://localhost:8000/api/b1/flights/flights/${id}`;

  try {
    const res = await axios.get(url);
    return res.data;
  } catch (err) {
    console.error(`Failed to fetch ${direction} flight:`, err);
    return null;
  }
}

onMounted(async () => {
  userEmail.value = localStorage.getItem('userEmail') || '';
  if (!userEmail.value) {
    alert('Please log in to proceed with booking.');
    await router.push('/auth');
    return;
  }

  if (!outboundId) {
    alert('Outbound flight ID is missing.');
    await router.push('/');
    return;
  }

  outboundFlight.value = await fetchFlight(outboundId, 'outbound');

  if (sepId) {
    sepFlight.value = await fetchFlight(sepId, 'sep');
  }

  if (returnId) {
    returnFlight.value = await fetchFlight(returnId, 'return');
  }

  if (sepIdReturn) {
    sepFlightReturn.value = await fetchFlight(sepIdReturn, 'sepReturn');
  }
});

const totalPrice = computed(() => {
  const add = classPriceAdd[ticketClass.value] || 0;
  return (basePriceFromQuery + add) * passengers.value;
});

async function confirmBooking() {
  error.value = '';
  try {
    loading.value = true;

    if (!firstName.value || !lastName.value) {
      alert('Please fill in your first and last name.');
      loading.value = false;
      return;
    }

    if (passengers.value < 1 || passengers.value > 6) {
      alert('Number of passengers must be between 1 and 6.');
      loading.value = false;
      return;
    }

    const payload = {
      outbound_id: outboundId,
      sep_id: sepId,
      return_id: returnId,
      sep_id_return: sepIdReturn,
      first_name: firstName.value,
      last_name: lastName.value,
      passengers: passengers.value,
      ticket_class: ticketClass.value,
      total_price: totalPrice.value,
      user_email: userEmail.value
    };
    console.log('Payload to send:', payload);

    await axios.post('http://localhost:8000/api/b1/booking/bookings', payload);

    alert('Booking successful!');
    await router.push('/profile');
  } catch (err) {
    console.error(err);
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail;
      alert(error.value);
    } else {
      alert('Booking failed. Please try again.');
    }
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <HeaderMain />
    <div class="max-w-md mx-auto mt-12 p-8 bg-white rounded-xl shadow-lg">
      <h2 class="text-xl font-bold mb-6">Enter Booking Details</h2>

      <div class="mb-4">
        <label class="block mb-1 font-semibold">First Name</label>
        <input v-model="firstName" type="text" class="w-full px-3 py-2 border rounded" />
      </div>

      <div class="mb-4">
        <label class="block mb-1 font-semibold">Last Name</label>
        <input v-model="lastName" type="text" class="w-full px-3 py-2 border rounded" />
      </div>

      <div class="mb-4">
        <label class="block mb-1 font-semibold">Passengers (max 6)</label>
        <input
          v-model.number="passengers"
          type="number"
          min="1"
          max="6"
          class="w-full px-3 py-2 border rounded"
        />
      </div>

      <div class="mb-4">
        <label class="block mb-1 font-semibold">Ticket Class</label>
        <select v-model="ticketClass" class="w-full px-3 py-2 border rounded">
          <option value="economy">Economy</option>
          <option value="business">Business (+250)</option>
          <option value="first">First Class (+500)</option>
        </select>
      </div>

      <div class="mb-4 font-bold">Total Price: {{ totalPrice }} ₴</div>

      <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>

      <button
        @click="confirmBooking"
        :disabled="loading"
        class="w-full bg-indigo-600 text-white font-bold py-2 rounded hover:bg-indigo-700 transition disabled:opacity-50"
      >
        {{ loading ? 'Booking...' : 'Confirm Booking' }}
      </button>
    </div>
  </div>
</template>


