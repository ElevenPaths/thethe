<template>
  <v-footer absolute class="grey darken-3">
    <span lg1 class="text-md-center white--text px-2 font-weight-bold">v{{ version }}</span>
    <v-spacer></v-spacer>
    <v-btn flat href="https://elevenpaths.com" target="_blank">
      <v-img :src="require('@/assets/11p_logo.png')" contain max-width="64"></v-img>
    </v-btn>
    <span lg1 class="text-md-center white--text px-2">&copy;&nbsp;{{ new Date().getFullYear() }}</span>
  </v-footer>
</template>

<script>
const APP_VERSION = require("../../package.json").version;

export default {
  name: "StatusBar",
  data() {
    return {
      version: APP_VERSION
    };
  }
};
</script>
