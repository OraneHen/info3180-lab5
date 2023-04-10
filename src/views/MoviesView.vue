<template>
    <h2 class="header">Movies</h2>
    <div class="movies">
        <div v-for="movie  in (resp.movies ? resp.movies : [])" class="mov_container">
            <div class="crop">
                <img :src="movie.poster" class="img"/>
            </div>
            <div class="mov_body">
                <div class="title">
                    {{ movie.title }}
                </div>
                <div class="description">
                    {{ movie.description }}
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.header{
    margin: 0px 50px;
}
.movies {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    margin: 0px 50px;
}

.mov_container {
    display: flex;
    flex-direction: row;
    max-width: 600px;
    max-height: 300px;
    border: 1px solid #afafaf;
    border-radius: 4px;
    width:100%;
    margin-top: 20px;
    margin-right: 50px
} 

.crop {
    display: flex;
    width: 200px;
    height: 300px;
    min-width: 200px;
    position: relative;
    overflow: hidden;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

.img {
    width: 200px;
    height: 300px;
    object-fit: cover;
    object-position: center center; 
}

.mov_body{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.title {
    margin-top: 15px;
    font-size: 22px;
    font-weight: 500;
    min-height: 20%;
}

.description{
    margin-top: 5px;
}
</style>

<script setup>
import { ref, onMounted } from "vue";
let resp = ref("");

onMounted(() => {
    fetchMovies();
});

function fetchMovies() {
    fetch('/api/v1/movies')
        .then((response) => response.json())
        .then((data) => {
            resp.value = data;
        })
}

</script>
