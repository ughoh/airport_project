import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/HomeVue.vue'
import AirportInfo from '@/pages/InfoVue.vue'
import FlightsVue from "@/pages/FlightsVue.vue";
import ResultVue from "@/pages/ResultVue.vue";
import ResultRound from "@/pages/ResultRound.vue";
import AuthVue from "@/pages/AuthVue.vue";
import ProfileVue from "@/pages/ProfileVue.vue";
import BookingDetails from "@/pages/BookingDetails.vue";
import TicketsVue from "@/pages/TicketsVue.vue";
import AdminPanel from "@/adminpages/AdminPanel.vue";
import AircraftVue from "@/adminpages/AircraftVue.vue";
import AirlineVue from "@/adminpages/AirlineVue.vue";
import AirportVue from "@/adminpages/AirportVue.vue";
import EmployeeVue from "@/adminpages/EmployeeVue.vue";

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/info', name: 'AirportInfo', component: AirportInfo },
  { path: '/flights', name: 'Flights', component: FlightsVue },
  { path: '/results', name: 'results', component: ResultVue },
  { path: '/results_round', name: 'results_round', component: ResultRound },
  { path: '/auth', name: 'auth', component: AuthVue },
  { path: '/profile', name: 'profile', component: ProfileVue},
  { path: '/booking-details', name: 'BookingDetails', component: BookingDetails},
  { path: '/tickets', name: 'tickets', component: TicketsVue},
  { path: '/admin', name: 'admin', component: AdminPanel},
  { path: '/aircrafts', name: 'aircrafts', component: AircraftVue},
  { path: '/airlines', name: 'airlines', component: AirlineVue},
  { path: '/airports', name: 'airports', component: AirportVue},
  { path: '/employees', name: 'employees', component: EmployeeVue}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router;
