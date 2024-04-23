<template>
  <div class="content" style="margin-top: 10px;">
    <contentComponent v-if="re_flage" Title="RECOMMENDED FOR YOU" Color="color: #32A641" :Data="Recommendation_data" />
    <div v-else style="text-align: center;">
      <h3 class="text mt-4">Login to display recommendation list</h3>
    </div>
  </div>
  <v-divider style="margin-bottom: 20px;" :thickness="3" class="border-opacity-50" color="green"></v-divider>
  <div class="content">
    <contentComponent v-if="flag" Title="Master Recommended" Color="color: #D42E2E" :Data="Master_data" />
  </div>
  <v-divider style="margin-bottom: 20px;" :thickness="3" class="border-opacity-50" color="red"></v-divider>
  <div class="content">
    <contentComponent v-if="flag" Title="POPULAR THIS SEASON" Color="color: #ADC0D2" :Data="Popular_data" />
  </div>
  <div class="content">
    <contentComponent v-if="flag" Title="UPCOMING NEXT SEASON" Color="color: #ADC0D2" :Data="Upcoming_data" />
  </div>
  <div class="content">
    <contentComponent v-if="flag" Title="ALL TIME POPULAR" Color="color: #ADC0D2" :Data="All_popular_data" />
  </div>
</template>

<script setup>
import contentComponent from '@/components/contentComponent.vue'
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { recommendationStore } from '@/store/recommendation'

const Store = recommendationStore()

const Recommendation_data = ref()
const Master_data = ref()
const Popular_data = ref()
const Upcoming_data = ref()
const All_popular_data = ref()

const flag = ref(false)
const re_flage = ref(false)

onMounted(() => {
  const path_master = 'http://localhost:5001/listBooksForMaster'
  const path = 'http://localhost:5001/listBooks'
  axios.get(path_master)
    .then((res) => {
      Master_data.value = res.data
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    });
  axios.get(path)
    .then((res) => {
      Popular_data.value = res.data
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    });
  axios.get(path)
    .then((res) => {
      Upcoming_data.value = res.data
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    });
  axios.get(path)
    .then((res) => {
      All_popular_data.value = res.data
      flag.value = true
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    });
})

watch(() => Store.data, (newValue, oldValue) => {
  Recommendation_data.value = newValue
  // console.log(Recommendation_data.value)
  // console.log(Master_data.value)
  re_flage.value = true
})
</script>

<style scoped>
.content {
  margin-bottom: 20px;
  margin-left: 50px;
  margin-right: 50px;
}

.text {
  font-family: Overpass;
  color: #37b053
}
</style>