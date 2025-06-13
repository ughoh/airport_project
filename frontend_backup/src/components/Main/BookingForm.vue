<script setup>
import OneWay from "@/components/Main/RadioVue.vue";
import FromInput from "@/components/Main/FromInput.vue";
import DateGo from "@/components/Main/DateGo.vue";
import ToInput from "@/components/Main/ToInput.vue";
import DateReturn from "@/components/Main/DateReturn.vue";
import SearchButton from "@/components/Main/SearchButton.vue";

import { computed } from 'vue'
import { useFlightSearchStore } from '@/stores/FlightSearchStore'

const store = useFlightSearchStore()

const ticketType = computed({
  get: () => store.ticketType,
  set: (value) => store.setTicketType(value)
})
</script>


<template>
  <div class="max-w-7xl mx-auto mt-14 p-12 bg-white rounded-3xl shadow-lg">
      <OneWay v-model="ticketType" class="mb-6" />

      <form class="grid grid-cols-12 gap-5 items-end">

        <div class="col-span-3">
          <FromInput />
        </div>

        <div class="col-span-3">
          <ToInput />
        </div>

        <div :class="ticketType === 'roundtrip' ? 'col-span-2' : 'col-span-4'">
          <DateGo />
        </div>

        <div v-if="ticketType === 'roundtrip'" class="col-span-2">
          <DateReturn />
        </div>

        <div class="col-span-2">
          <SearchButton />
        </div>

      </form>
    </div>
</template>