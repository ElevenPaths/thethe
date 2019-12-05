<template>
  <v-flex lg6 class="text-xs-left">
    <v-divider></v-divider>
    <v-layout row pt-2 wrap class="subheading">
      <v-flex>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.email" lg3>
            <v-label>Email:</v-label>
          </v-flex>
          <v-flex>{{ resource.email }}</v-flex>
        </v-layout>
      </v-flex>
    </v-layout>

    <v-layout row pt-2 wrap class="subheading">
      <v-flex>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.status_description" lg3>
            <v-label>Status:</v-label>
          </v-flex>
          <v-flex>{{ resource.status_description }}</v-flex>
        </v-layout>
      </v-flex>
    </v-layout>

    <v-layout row pt-2 wrap class="subheading">
      <v-flex>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.smtp_code" lg3>
            <v-label>SMTP Code:</v-label>
          </v-flex>
          <v-flex>{{ resource.smtp_code }}</v-flex>
        </v-layout>
      </v-flex>
    </v-layout>

    <v-layout row pt-2 wrap class="subheading">
      <v-flex>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.smtp_log" lg3>
            <v-label>SMTP Log:</v-label>
          </v-flex>
          <v-flex>{{ resource.smtp_log }}</v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "verifymail",
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
