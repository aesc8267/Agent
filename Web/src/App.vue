<template>
  <div id="app">
    <p>{{ text }}</p>
  </div>
</template>
<script lang="ts" setup name="App">
import {hello_world} from './api/agent'
import { ref } from 'vue'
let text=ref('hello')
hello_world().then((res) => {
  text.value = res.data
  console.log(res.data)
})
</script>