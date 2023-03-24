<template>
    <input type = "text" class = "rounded border-2 border-gray-200 w-full m-3" placeholder="Search for Meals"/>

    <div class = "flex gap-2 justify-center mt-3 ">
        <!-- <router-link v-for="letter of letters.split('')" -->
        <router-link :to = "{name: 'byLetter', params: {letter}}"  v-for = "letter of letters" :key = "letter">
            {{ letter }}
        </router-link>
    </div>
</template>

<script setup>

import { computed, onMounted } from 'vue'
import store from '../store';
import axiosClient from '../axiosClient.js'

const meals = computed(() => store.state.meals)
const letters = 'ABCDEFGHIJKLMNOPQESTUVWXYZ'.split("")

onMounted(async () => {
    const response = await axiosClient.get('/list.php?i=list');
    console.log(response.data);
})

</script>
