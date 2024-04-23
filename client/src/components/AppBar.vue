<template>
    <v-app-bar color="#152232">
        <template v-slot:prepend>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title class="text">Anime Recommendation System</v-app-bar-title>

        <v-app-bar-subtitle class="text">Hybrid recommendation system utilizing Item-based and SVD
            algorithms</v-app-bar-subtitle>

        <v-spacer></v-spacer>
        <Dialog />
    </v-app-bar>
</template>

<script setup>
import Dialog from '@/components/Dialogs.vue'
</script>

<style scoped>
.text {
    font-family: Overpass;
    color: #9FADBD
}
</style>