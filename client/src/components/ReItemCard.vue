<template>
    <v-card variant="text" class="text" width="185px" color="#0B1622" hover elevation="16" @click="showInfo">
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

        <v-expand-transition>
            <v-card v-if="reveal" class="position-absolute w-100" height="100%" style="bottom: 0;">
                <v-card-text class="pb-0">
                    <p class="text-h7 text mb-2">Why recommended</p>
                    <p class="text">Hybrid Score: </p>
                    <v-chip class="mb-3 mr-3" color="green" size=" small" label>
                        <v-icon icon="mdi-label" start></v-icon>
                        {{ props.Data.hybrid_score }}
                    </v-chip>
                    <p class="text">Predicted Rating: </p>
                    <v-chip class="mb-3 mr-3" color="green" size=" small" label>
                        <v-icon icon="mdi-label" start></v-icon>
                        {{ props.Data.predicted_rating }}
                    </v-chip>
                    <p class="text">Content Similarity: </p>
                    <v-chip class="mb-3 mr-3" color="green" size=" small" label>
                        <v-icon icon="mdi-label" start></v-icon>
                        {{ props.Data.content_similarity }}
                    </v-chip>
                </v-card-text>
            </v-card>
        </v-expand-transition>
    </v-card>
</template>

<script setup>
import { defineProps, ref } from 'vue'
const props = defineProps(['Data'])

const reveal = ref(false)

function showInfo() {
    reveal.value = !reveal.value
}
</script>

<style scoped>
.text {
    font-family: Overpass;
    color: #9FADBD
}
</style>