<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['filter-changed']);

function selectFilter(type) {
  emit('filter-changed', type);
}
</script>

<template>
  <div class="flex gap-4 justify-center my-4">
    <button
      @click="selectFilter('cheapest')"
      class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
    >
      Cheapest
    </button>
    <button
      @click="selectFilter('fastest')"
      class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
    >
      Fastest
    </button>
    <button
      @click="selectFilter('best')"
      class="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition"
    >
      Best
    </button>
  </div>
</template>
