<template>
  <v-layout row wrap class="subheading">{{ resource }}</v-layout>
</template>

<script>
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "urlscan",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data };
      return plugin_result;
    }
  },
  methods: {
    formatted_time: function(ts) {
      let t = new Date(ts);
      return `${t.toLocaleDateString()} at ${t.toLocaleTimeString()}`;
    },
    copy_content: async function(data) {
      await navigator.clipboard.writeText(data);
    }
  }
};
</script>
