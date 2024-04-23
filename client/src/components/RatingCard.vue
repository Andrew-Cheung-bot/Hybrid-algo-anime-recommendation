<template>
    <v-card variant="text" class="text" width="185px" color="#0B1622">
        <v-img style="width: 185px;height:265px" Default :src="props.Data.image_path"
            lazy-src="/anime_images/doggie.jpg">
            <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                    <v-progress-circular color="grey-lighten-4" indeterminate></v-progress-circular>
                </div>
            </template>
        </v-img>
        <small class="text" style="color: #8BA0B2;">
            {{ props.Data.anime_name }}
        </small>
    </v-card>
    <v-rating v-model="rating" size="x-small" half-increments hover @click="submitForm"></v-rating>
</template>

<script setup>
import { defineProps, ref, defineEmits } from 'vue'
const props = defineProps(['Data'])
const emits = defineEmits(["click"])

const rating = ref()

function submitForm() {
    emits('click', props.Data.anime_id.toString(), rating.value * 2)
}
</script>

<style scoped>
.text {
    font-family: Overpass;
    color: #9FADBD
}
</style>