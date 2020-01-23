<template>
  <v-flex class="text-xs-left">
    <v-divider></v-divider>
    <v-card>
      <v-card-title>
        <v-flex title v-if="resource.threatlists.length > 0"
          >This IP is included in the following threat lists</v-flex
        >
        <v-flex v-else title>This IP is not included in any thread list</v-flex>
      </v-card-title>
      <v-card-text>
        <v-flex v-for="threatlist in resource.threatlists" :key="threatlist">{{
          threatlist
        }}</v-flex>
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "onyphe",
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
