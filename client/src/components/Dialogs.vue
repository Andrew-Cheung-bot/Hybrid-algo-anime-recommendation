<template>
    <v-dialog width="auto">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn color="brown" prepend-icon="mdi-login" text="Login" variant="outlined"
                v-bind="activatorProps"></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card prepend-icon="mdi-earth" title="Please rate the following animes.">

                <v-row style="margin: 10px 20px;">
                    <v-col>
                        <div class="text-center">
                            <RatingItem />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem />
                        </div>
                    </v-col>
                </v-row>

                <v-card-actions style="margin-left: 20px;margin-right: 20px;margin-bottom: 10px;">
                    <v-btn block color="surface-variant" text="Save" variant="flat" @click="isActive.value = false"></v-btn>
                </v-card-actions>

            </v-card>
        </template>
    </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import RatingItem from '@/components/RatingCard.vue'

const dialog = ref('')
</script>