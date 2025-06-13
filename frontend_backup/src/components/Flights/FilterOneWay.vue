<template>
  <div class="max-w-6xl mx-auto my-6 flex gap-4 justify-center">
    <button
      @click="setFilter('cheapest')"
      class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
    >
      Cheapest
    </button>
    <button
      @click="setFilter('fastest')"
      class="bg-green-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
    >
      Fastest
    </button>
    <button
      @click="setFilter('best')"
      class="bg-purple-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
    >
      Best
    </button>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from "vue";

const props = defineProps({
  modelValue: String,
});

const emit = defineEmits(["update:modelValue", "filter-changed"]);

const selected = ref(props.modelValue || null);

watch(
  () => props.modelValue,
  (val) => {
    selected.value = val;
  }
);

function setFilter(type) {
  selected.value = type;
  emit("update:modelValue", type);
  emit("filter-changed", type);
}

</script>

