<template>
  <v-app>
    <AppBar />
    <v-main style="background-color: #0B1622; padding-left: 80px; padding-right: 80px;">
      <router-view />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script setup>
import AppFooter from '@/components/AppFooter.vue'
import AppBar from '@/components/AppBar.vue'
</script>
