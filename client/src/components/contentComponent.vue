<template>
    <h4 class="mb-3 text" :style="Color">{{ props.Title }}</h4>
    <v-row v-if="props.Title == 'RECOMMENDED FOR YOU'">
        <v-col>
            <ReItem :Data="props.Data[0]" />
        </v-col>
        <v-col>
            <ReItem :Data="props.Data[1]" />
        </v-col>
        <v-col>
            <ReItem :Data="props.Data[2]" />
        </v-col>
        <v-col>
            <ReItem :Data="props.Data[3]" />
        </v-col>
        <v-col>
            <ReItem :Data="props.Data[4]" />
        </v-col>
        <v-col>
            <ReItem :Data="props.Data[5]" />
        </v-col>
    </v-row>

    <v-row v-else>
        <v-col>
            <Item :Data="props.Data[0]" />
        </v-col>
        <v-col>
            <Item :Data="props.Data[1]" />
        </v-col>
        <v-col>
            <Item :Data="props.Data[2]" />
        </v-col>
        <v-col>
            <Item :Data="props.Data[3]" />
        </v-col>
        <v-col>
            <Item :Data="props.Data[4]" />
        </v-col>
        <v-col>
            <Item :Data="props.Data[5]" />
        </v-col>
    </v-row>

</template>

<script setup>
import { defineProps, ref } from 'vue'
import Item from '@/components/ItemCard.vue'
import ReItem from '@/components/ReItemCard.vue'

const props = defineProps(['Title', 'Color', 'Data'])
// console.log(props.Data)
</script>

<style scoped>
.text {
    font-family: Overpass;
    color: #9FADBD
}
</style>