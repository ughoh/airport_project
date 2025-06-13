<template>
    <header class="	bg-indigo-600 flex justify-between border-b border-indigo-600 px-5 py-8">
      <div class="flex items-center gap-4">
        <img src="/airplane.ico" alt="Logo" class="w-16 h-16 object-contain rounded-full bg-white p-2 shadow-md">
          <div>
            <h1 class="text-4xl font-extrabold text-white drop-shadow-lg">SKY-ADMIN</h1>
            <h2 class="text-base lg:text-lg text-blue-100 ">Skylight International Airport</h2>
          </div>
      </div>

      <ul class="flex items-center gap-6 text-white text-lg font-medium tracking-wide">
        <li>
          <router-link to="/aircrafts" class="hover:underline">Aircrafts</router-link>
        </li>
        <li>
          <router-link to="/airlines" class="hover:underline">Airlines</router-link>
        </li>
        <li>
          <router-link to="/airports" class="hover:underline">Airports</router-link>
        </li>
        <li>
          <router-link to="/employees" class="hover:underline">Employees</router-link>
        </li>
        <li>
          <router-link to="/profile" class="hover:underline">Profile</router-link>
        </li>

      </ul>

    </header>
</template>
<script setup lang="ts">
</script>