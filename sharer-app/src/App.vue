<script setup lang="ts">
import {ref} from "vue";
import type {Ref} from "vue";

interface SearchResult {
  search_url: string,
  artist: string,
  title: string
}

const trackUrl: Ref<string> = ref("");
const searchResult: Ref<SearchResult | null> = ref(null);
const apiUrl = "https://apps.ionov.me/musicsharer/api/track/"

const updateLink = async () => {
  let trackId, res;

  try {
    trackId = new URL(trackUrl.value).pathname.split('/').pop();
  } catch (error) {
    console.log("Not a valid URL:", trackUrl.value);
    return
  }

  try {
    res = await fetch(apiUrl + trackId, { "mode": "cors" });
  }
  catch (error) {
    console.error("Failed to fetch: ", error);
  }

  if (res && res.ok)
    searchResult.value = await res.json();
};

</script>

<template>
  Paste Spotify share URL here
  <div>
    <input type="text" id="url" v-model="trackUrl" />
    <button @click="updateLink">Share</button>
  </div>
  Link: <a  v-if="searchResult" :href="searchResult.search_url" target="_blank">{{ searchResult.artist }} — {{ searchResult.title }}</a>
</template>

<style scoped>

</style>
