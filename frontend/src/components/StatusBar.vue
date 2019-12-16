<template>
  <v-footer absolute class="grey darken-3">
    <v-spacer></v-spacer>
    <v-layout align-center justify-end>
      <v-flex lg1 class="text-md-center white--text">&copy;&nbsp;{{ new Date().getFullYear() }}</v-flex>
      <v-flex lg1 pr-1>
        <v-img :src="require('../../public/static/images/11p_logo.png')" contain></v-img>
      </v-flex>
    </v-layout>
  </v-footer>
</template>
<script></script>
