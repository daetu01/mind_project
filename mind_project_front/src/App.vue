<script setup>
import FloatingNav from './components/FloatingNav.vue';
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-apple-gray font-sans text-apple-black selection:bg-wow-purple selection:text-white">
    <FloatingNav />
    <main class="pt-14 relative z-10">
      <RouterView />
    </main>
  </div>
</template>
