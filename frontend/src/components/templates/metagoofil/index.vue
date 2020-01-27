<template>
  <v-flex class="text-xs-left">
    <v-divider></v-divider>
    <v-layout row wrap>
      <v-flex v-for="item in resource" :key="item" xs3>
        <v-card>
          <v-card-title class="justify-center" style="word-break: break-all">{{
            item.filename
          }}</v-card-title>
          <v-card-text>
            <div v-if="item.extension == 'pdf'" class="fi fi-swift fi-size-xl">
              <div class="fi-content">{{ item.extension }}</div>
            </div>
            <div v-if="item.extension == 'doc'" class="fi fi-doc fi-size-xl">
              <div class="fi-content">{{ item.extension }}</div>
            </div>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn flat color="green" :href="item.url" target="_blank"
              >Download</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "metagoofil",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };
      return plugin_result;
    }
  }
};
</script>
