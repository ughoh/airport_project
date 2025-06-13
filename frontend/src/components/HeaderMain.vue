<template>
    <header class="	bg-indigo-600 flex justify-between border-b border-indigo-600 px-5 py-8">
      <div class="flex items-center gap-4">
        <img src="/airplane.ico" alt="Logo" class="w-16 h-16 object-contain rounded-full bg-white p-2 shadow-md">
          <div>
            <h1 class="text-4xl font-extrabold text-white drop-shadow-lg">SKY</h1>
            <h2 class="text-base lg:text-lg text-blue-100 ">Skylight International Airport</h2>
          </div>
      </div>

      <ul class="flex items-center gap-6 text-white text-lg font-medium tracking-wide">
        <li>
          <router-link to="/" class="hover:underline">Booking</router-link>
        </li>
        <li>
          <router-link to="/flights" class="hover:underline">Flights</router-link>
        </li>
        <li>
          <nav>
            <router-link to="/info" class="hover:underline">About airport</router-link>
          </nav>
        </li>
        <li>
          <router-link to="/profile" class="hover:underline">Profile</router-link>
        </li>

      </ul>

    </header>
</template>