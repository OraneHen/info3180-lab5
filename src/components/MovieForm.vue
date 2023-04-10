<template>
    <div v-if="status == 200" class="alert alert-success" role="alert">
        {{ resp.message }}
    </div>
    <div v-if="status == 400" class="alert alert-danger" role="alert">
        <li v-for="({ error }, index) in resp.errors">
            {{ resp.errors[index] }}
        </li>
    </div>
    <form enctype="multipart/form-data" @submit.prevent="saveMovie" id="movieForm" class="form">
        <h2>Upload Form</h2>
        <div class="field mb-3">
            <label for="title" class="field-label">Title</label>
            <input type="text" name="title" class="formcontrol" />
        </div>
        <div class="field mb-3">
            <label for="description" class="field-label">Description</label>
            <textarea name="description" id="description" cols="30" rows="3" class="formcontrol"></textarea>
        </div>
        <div class="field mb-3">
            <label for="poster" class="field-label">Photo Upload</label>
            <input type="file" id="poster" name="poster" class="formcontrol">
        </div>
        <input type="submit" class="btn btn-primary"> 
    </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
let csrf_token = ref("");
let status = ref("") ;
let resp = ref("");

onMounted(() => {
    getCsrfToken();
});

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        })
}

function saveMovie() {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    }).then(function (response) {
        status.value = response.status;
        return response.json();
    }).then(function (data) {
        resp.value = data;
        console.log(data.errors[0]);
    }).catch(function (error) {
        console.log(error)
    });
}
</script>

<style>
.form{
    display: flex;
    flex-direction: column;
    width: 1280px;
    margin: auto;
}
.field{
    display: flex;
    flex-direction: column;
}
.field-label{
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 5px;
}
</style>