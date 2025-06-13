<script setup>
import { ref } from 'vue'
import FlightCheckIn from "@/components/Info/Passengers/FlightCheckIn.vue";
import LuggageBaggage from "@/components/Info/Passengers/LuggageBaggage.vue";
import SecurityRules from "@/components/Info/Passengers/SecurityRules.vue";
import SpecialNeeds from "@/components/Info/Passengers/SpecialNeeds.vue";
import TerminalAccess from "@/components/Info/Passengers/TerminalAccess.vue";
import AboutAirport from "@/components/Info/AboutAirport/AboutAirport.vue";
import ContactVue from "@/components/Info/AboutAirport/ContactVue.vue";
import CodeOfEthics from "@/components/Info/AboutAirport/CodeOfEthics.vue";
import AirportScheme from "@/components/Info/AboutAirport/AirportScheme.vue";
import PartnersVue from "@/components/Info/Partners/PartnersVue.vue";
import AirlineRelationship from "@/components/Info/Partners/AirlineRelationship.vue";
import HandlingCompanies from "@/components/Info/Partners/HandlingCompanies.vue";
import PlanningVue from "@/components/Info/Partners/PlanningVue.vue";
import VIP from "@/components/Info/VIP/VIP.vue";
import BusinessVue from "@/components/Info/VIP/BusinessVue.vue";
import ServicesVue from "@/components/Info/Additional/ServicesVue.vue";
import PolicyVue from "@/components/Info/Additional/PolicyVue.vue";

const menuItems = [
  {
    label: 'Passengers',
    sections: [
      {title: 'Flight check-in', component: FlightCheckIn },
      {title: 'Hand luggage & baggage', component: LuggageBaggage},
      {title: 'Security rules', component: SecurityRules},
      {title: 'Passengers with special needs', component: SpecialNeeds},
      {title: 'Terminal access', component: TerminalAccess}
    ]
  },
  {
    label: 'About Airport',
    sections: [
      {title: 'About Airport', component: AboutAirport},
      {title: 'Contact', component: ContactVue},
      {title: 'Code of Ethics and Business Conduct', component: CodeOfEthics},
      {title: 'Airport scheme', component: AirportScheme}
    ]
  },
  {
    label: 'Partners',
    sections: [
      {title: 'Partners Opportunities', component: PartnersVue},
      {title: 'Airline Relationship', component: AirlineRelationship},
      {title: 'Handling Companies', component: HandlingCompanies},
      {title: 'Planning and Operational Management', component: PlanningVue}
    ]
  },
  {
    label: 'VIP',
    sections: [
      {title: 'VIP-services', component: VIP},
      {title: 'Business-services', component: BusinessVue}
    ]
  },
  {
    label: 'Additional',
    sections: [
      {title: 'Services', component: ServicesVue},
      {title: 'Policy', component: PolicyVue}
    ]
  }
]

const expandedLabel = ref(null)
const selectedSection = ref(null)

function toggleItem(item) {
  if (expandedLabel.value === item.label) {
    expandedLabel.value = null
    selectedSection.value = null
  } else {
    expandedLabel.value = item.label
    selectedSection.value = null
  }
}

function selectSection(section) {
  selectedSection.value = section
}
</script>

<template>
  <div class="flex min-h-screen bg-gray-100">
    <div class="w-1/3 p-6 bg-white shadow-lg">
      <ul>
        <li v-for="item in menuItems" :key="item.label" class="mb-3 bg-indigo-100 border-gray-300 transition">
          <div
            @click="toggleItem(item)"
            class="flex justify-between items-center px-4 py-3 transition rounded cursor-pointer hover:bg-indigo-100"
            :class="{ 'bg-indigo-200 font-semibold transition': expandedLabel === item.label }"
          >
            {{ item.label }}
            <svg
              class="w-4 h-4 transform transition-transform"
              :class="{ 'rotate-90': expandedLabel === item.label }"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </div>

          <ul v-if="expandedLabel === item.label" class=" mt-2">
            <li
              v-for="section in item.sections"
              :key="section.title"
              @click.stop="selectSection(section)"
              class="px-3 py-2 text-sm rounded cursor-pointer transition hover:bg-indigo-50"
              :class="{ 'bg-indigo-300 text-white transition': selectedSection?.title === section.title }"
            >
              {{ section.title }}
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <div class="w-2/3 p-4 bg-indigo-200 border-l border-gray-300">
      <component v-if="selectedSection" :is="selectedSection.component" />
      <div v-else>
        <component v-bind:is="AboutAirport"></component>
      </div>
    </div>
  </div>
</template>