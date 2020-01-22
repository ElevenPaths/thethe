<template>
  <v-layout row>
    <v-flex xs12 sm6 md3>
      <v-select v-model="plugin" :items="plugins" label="Service"></v-select>
    </v-flex>
    <v-flex>
      <v-text-field v-model="apikey" label="API KEY" @keyup.enter="$emit('add', plugin, apikey)"></v-text-field>
    </v-flex>
    <v-flex xs1>
      <v-btn icon @click="$emit('add', plugin, apikey)">
        <v-icon>done</v-icon>
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import api_call from "../utils/api";

export default {
  data() {
    return {
      plugins: [],
      plugin: "",
      apikey: ""
    };
  },
  mounted: function() {
    let params = {
      url: "/api/get_all_plugins"
    };

    api_call(params).then(resp => {
      resp.data.sort((a, b) => {
        if (a.name > b.name) return 1;
        if (b.name > a.name) return -1;
        return 0;
      });
      this.plugins = resp.data;
    });
  }
};
</script>