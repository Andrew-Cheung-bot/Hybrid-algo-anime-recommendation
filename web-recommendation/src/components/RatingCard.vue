<template>
    <v-card variant="text" class="text" width="185px" color="#0B1622">
        <img src="/anime_images/doggie.jpg" alt="Anime Image" style="width: 185px;height:265px">
        <small class="text" style="color: #8BA0B2;">
            Mushoku Tensei II: Isekai Ittara Honki Dasu Part 2
        </small>
    </v-card>
    <v-rating v-model="rating" size="x-small" half-increments hover></v-rating>
</template>

<script setup>


</script>

<style scoped>
.text {
    font-family: Overpass;
    color: #9FADBD
}
</style>