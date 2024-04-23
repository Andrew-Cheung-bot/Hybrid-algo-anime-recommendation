<template>
  <div class="content" style="margin-top: 10px;">
    <contentComponent Title="RECOMMENDED FOR YOU" Color="color: #32A641" Data="This is Recommendation" />
  </div>
  <v-divider style="margin-bottom: 20px;"></v-divider>
  <div class="content">
    <contentComponent v-if="flag" Title="TRENDING NOW" Color="color: #ADC0D2" :Data="Trending_data" />
  </div>
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
import { onMounted, ref, onBeforeMount } from 'vue'
import axios from 'axios';

// const Recommendation_data = ref()
const Trending_data = ref()
const Popular_data = ref()
const Upcoming_data = ref()
const All_popular_data = ref()

const flag = ref(false)

onMounted(() => {
    const path = 'http://localhost:5001/listBooks';
    axios.get(path)
      .then((res) => {
        Trending_data.value = res.data
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
</script>

<style scoped>
.content {
  margin-bottom: 30px;
  margin-left: 50px;
  margin-right: 50px;
}
</style>