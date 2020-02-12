<template>
  <v-layout row>
    <v-flex xs12 sm6 md3>
      <v-select v-model="plugin" :items="plugins" label="Service"></v-select>
    </v-flex>
    <v-flex>
      <v-text-field
        v-model="apikey"
        label="API KEY"
        @keyup.enter="
          $emit('add', plugin, apikey);
          clean();
        "
      ></v-text-field>
    </v-flex>
    <v-flex xs1>
      <v-btn
        icon
        :disabled="empty"
        @click="
          $emit('add', plugin, apikey);
          clean();
        "
      >
        <v-icon>done</v-icon>
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import api_call from "../utils/api";

export default {
  props: ["reset"],
  data() {
    return {
      plugins: [],
      plugin: "",
      apikey: ""
    };
  },
  computed: {
    empty: function() {
      var result = true;
      if (this.plugin != "" && this.apikey != "") {
        result = false;
      }
      return result;
    }
  },
  mounted: function() {
    if (this.$store.getters["is_authenticated"]) {
      let params = {
        url: "/api/get_all_plugins"
      };

      api_call(params).then(resp => {
        this.plugins = resp.data.sort();
      });
    }
  },
  watch: {
    reset: function(oldValue, newValue) {
      if (newValue) {
        this.clean();
      }
    }
  },
  methods: {
    clean() {
      this.plugin = "";
      this.apikey = "";
    }
  }
};
</script>
