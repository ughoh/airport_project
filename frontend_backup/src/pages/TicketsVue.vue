<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import HeaderMain from "@/components/HeaderMain.vue";
import FlightInfo from "@/components/Flights/FlightInfo.vue";

const tickets = ref([]);
const loading = ref(false);
const error = ref('');
const router = useRouter();

const email = localStorage.getItem('userEmail');
if (!email) {
  router.push('/auth');
}

const isObjectNotEmpty = (obj) => {
  return obj && typeof obj === 'object' && Object.keys(obj).length > 0;
};

async function fetchTickets() {
  loading.value = true;
  error.value = '';

  try {
    const response = await axios.get(`http://localhost:8000/api/b1/booking/tickets?email=${encodeURIComponent(email)}`);
    tickets.value = Array.isArray(response.data) ? response.data : [];
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Unknown error occurred';
    tickets.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchTickets();
});
</script>

<template>
  <div class="w-full min-h-screen bg-indigo-100 pb-12">
    <HeaderMain />
    <div class="max-w-4xl mx-auto mt-12 space-y-6">
      <h1 class="text-3xl font-bold text-center text-indigo-900 mb-8">My Tickets</h1>

      <p v-if="loading" class="text-gray-600 text-center">Loading tickets...</p>
      <p v-if="error" class="text-red-600 mb-4 text-center">{{ error }}</p>

      <ul v-if="Array.isArray(tickets) && tickets.length > 0" class="space-y-10">
        <template v-for="ticket in tickets" :key="ticket.id">

          <li class="bg-white border-[3px] border-indigo-400 rounded-3xl shadow-xl overflow-hidden text-indigo-900 font-medium tracking-wide relative p-6">
            <FlightInfo :flight="ticket.outbound_flight" :ticketClass="ticket.ticket_class" :etkt="ticket.id" />
            <div class="mt-3 font-semibold text-indigo-800">
              Passenger: {{ ticket.first_name }} {{ ticket.last_name }}
            </div>
          </li>


          <li v-if="isObjectNotEmpty(ticket.sep_flight)" class="bg-white border-[3px] border-indigo-400 rounded-3xl shadow-xl overflow-hidden text-indigo-900 font-medium tracking-wide relative p-6">
            <FlightInfo :flight="ticket.sep_flight" :ticketClass="ticket.ticket_class" :etkt="ticket.id + '-sep'" />
            <div class="mt-3 font-semibold text-indigo-800">
              Passenger: {{ ticket.first_name }} {{ ticket.last_name }}
            </div>
          </li>

          <li v-if="isObjectNotEmpty(ticket.return_flight)" class="bg-white border-[3px] border-indigo-400 rounded-3xl shadow-xl overflow-hidden text-indigo-900 font-medium tracking-wide relative p-6">
            <FlightInfo :flight="ticket.return_flight" :ticketClass="ticket.ticket_class" :etkt="ticket.id + '-ret'" />
            <div class="mt-3 font-semibold text-indigo-800">
              Passenger: {{ ticket.first_name }} {{ ticket.last_name }}
            </div>
          </li>

          <li v-if="isObjectNotEmpty(ticket.sep_flight_return)" class="bg-white border-[3px] border-indigo-400 rounded-3xl shadow-xl overflow-hidden text-indigo-900 font-medium tracking-wide relative p-6">
            <FlightInfo :flight="ticket.sep_flight_return" :ticketClass="ticket.ticket_class" :etkt="ticket.id + '-sep-ret'" />
            <div class="mt-3 font-semibold text-indigo-800">
              Passenger: {{ ticket.first_name }} {{ ticket.last_name }}
            </div>
          </li>
        </template>
      </ul>

      <p v-else class="text-gray-700 text-center">You don’t have any purchased tickets yet.</p>
    </div>
  </div>
</template>



