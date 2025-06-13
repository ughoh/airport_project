<script setup>
import { defineEmits } from 'vue'

const emit = defineEmits(['update:modelValue'])

const updateValue = (value) => {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="mb-6 flex gap-4">
    <label
      class="flex items-center gap-2 px-4 py-2 font-bold rounded-full border border-indigo-300 cursor-pointer transition-all duration-200"
      :class="modelValue === 'oneway' ? 'bg-indigo-100 text-indigo-800 border-indigo-500' : 'bg-white text-indigo-500 hover:bg-indigo-50'"
    >
      <input
        type="radio"
        name="ticket"
        value="oneway"
        class="hidden"
        :checked="modelValue === 'oneway'"
        @change="updateValue('oneway')"
      />
      One way
    </label>

    <label
      class="flex items-center gap-2 px-4 font-bold py-2 rounded-full border border-indigo-300 cursor-pointer transition-all duration-200"
      :class="modelValue === 'roundtrip' ? 'bg-indigo-100 text-indigo-800 border-indigo-500' : 'bg-white text-indigo-500 hover:bg-indigo-50'"
    >
      <input
        type="radio"
        name="ticket"
        value="roundtrip"
        class="hidden"
        :checked="modelValue === 'roundtrip'"
        @change="updateValue('roundtrip')"
      />
      Round trip
    </label>

<!--    <label-->
<!--      class="flex items-center gap-2 px-4 font-bold py-2 rounded-full border border-indigo-300 cursor-pointer transition-all duration-200"-->
<!--      :class="modelValue === 'separate' ? 'bg-indigo-100 text-indigo-800 border-indigo-500' : 'bg-white text-indigo-500 hover:bg-indigo-50'"-->
<!--    >-->
<!--      <input-->
<!--        type="radio"-->
<!--        name="ticket"-->
<!--        value="separate"-->
<!--        class="hidden"-->
<!--        :checked="modelValue === 'separate'"-->
<!--        @change="updateValue('separate')"-->
<!--      />-->
<!--      Separate-->
<!--    </label>-->
  </div>
</template>