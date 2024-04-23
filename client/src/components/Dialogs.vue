<template>
    <v-dialog width="auto">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn color="brown" prepend-icon="mdi-login" text="Login" variant="outlined" v-bind="activatorProps"
                @click="listBooks"></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card prepend-icon="mdi-earth" title="Please rate the following animes.">

                <v-row style="margin: 10px 20px;">
                    <v-col>
                        <div class="text-center">
                            <RatingItem v-if="flag" :Data="Books_data[0]" @click="handleSubmit" />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem v-if="flag" :Data="Books_data[1]" @click="handleSubmit" />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem v-if="flag" :Data="Books_data[2]" @click="handleSubmit" />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem v-if="flag" :Data="Books_data[3]" @click="handleSubmit" />
                        </div>
                    </v-col>
                    <v-col>
                        <div class="text-center">
                            <RatingItem v-if="flag" :Data="Books_data[4]" @click="handleSubmit" />
                        </div>
                    </v-col>
                </v-row>

                <v-card-actions style="margin-left: 20px;margin-right: 20px;margin-bottom: 10px;">
                    <v-btn block color="surface-variant" text="Save (Result will display in 30 seconds)" variant="flat"
                        @click="saveRating"></v-btn>
                </v-card-actions>

            </v-card>
        </template>
    </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import RatingItem from '@/components/RatingCard.vue'
import axios from 'axios';
import { storeToRefs } from 'pinia'
import { recommendationStore } from '@/store/recommendation'

const Store = recommendationStore()
let dictionary = {}
const isActive = ref()

function saveRating() {
    isActive.value = false
    const path = 'http://localhost:5001/rate';
    axios.post(path, {
        "ratings": JSON.stringify(dictionary)
    })
        .then((res) => {
            // console.log(res.data)
            Store.updateData(res.data)
            const data = storeToRefs(Store)
            console.log(data)
        })
        .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
        });
}

const Books_data = ref()
const flag = ref(false)
function listBooks() {
    const path = 'http://localhost:5001/listBooks';
    axios.get(path)
        .then((res) => {
            Books_data.value = res.data
            flag.value = true
        })
        .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
        });
}

function handleSubmit(id, rating) {
    dictionary[id] = rating
    // console.log(dictionary)
}
</script>