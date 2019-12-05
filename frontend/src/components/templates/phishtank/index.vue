<template>
  <v-flex class="text-xs-left">
    <v-flex v-if="resource.in_database" class="red--text title">Resource is in phishtank database</v-flex>
    <v-flex v-else class="green--text title">
      Resource is
      <span class="font-weight-bold">NOT</span> in phishtank database
    </v-flex>
    <v-divider v-if="resource.in_database"></v-divider>
    <v-flex v-if="resource.phish_detail_page">
      <v-layout>
        <v-flex lg2>
          <v-label>Link to Phishtank</v-label>
        </v-flex>
        <v-flex>
          <a
            target="_blank"
            rel="noopener noreferer"
            :href="resource.phish_detail_page"
          >{{ resource.phish_detail_page }}</a>
        </v-flex>
      </v-layout>
    </v-flex>
    <v-flex v-if="resource.verified">
      <v-layout align-center>
        <v-flex lg2>
          <v-label>Verified</v-label>
        </v-flex>
        <v-flex>
          <v-chip :color="what_color(resource.verified)">
            {{
            resource.verified
            }}
          </v-chip>
        </v-flex>
        <v-flex lg2>
          <v-label>Verified at</v-label>
        </v-flex>
        <v-flex>
          <v-chip>{{ formatted_time(resource.verified_at) }}</v-chip>
        </v-flex>
      </v-layout>
    </v-flex>
    <v-flex v-if="resource.valid">
      <v-layout align-center>
        <v-flex lg2>
          <v-label>Valid</v-label>
        </v-flex>
        <v-flex>
          <v-chip :color="what_color(resource.valid)">
            {{
            resource.valid
            }}
          </v-chip>
        </v-flex>
      </v-layout>
    </v-flex>
    <v-flex v-if="resource.screenshot_path" justify-center>
      <v-flex title>Screenshot</v-flex>
      <v-divider></v-divider>
      <v-layout align-center justify-center row fill-height py-3>
        <v-img :src="resource.screenshot_path" />
      </v-layout>
    </v-flex>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "phishtank",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results.results };
      return plugin_result;
    },
    screenshot: function() {
      if (this.resource.screenshot) {
        return new Buffer(this.resource.screenshot).toString("base64");
      }

      return null;
    }
  },
  methods: {
    what_color: function(item) {
      if (item) {
        return "green";
      }

      return "red";
    },

    formatted_time: function(ts) {
      let t = new Date(ts);
      return `${t.toLocaleDateString()} at ${t.toLocaleTimeString()}`;
    }
  }
};
</script>
