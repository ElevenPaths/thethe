<template>
  <v-flex class="text-xs-left">
    <v-divider></v-divider>
    <v-card>
      <v-card-title>
        <v-flex subheading>Maltiverse results for this resource</v-flex>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-layout v-if="resource.classification" align-center>
          <v-flex lg2>
            <v-label>Classification</v-label>
          </v-flex>
          <v-flex lg2>
            <v-chip
              :color="classifier_color(resource.classification)"
              class="font-weight-bold"
              >{{ resource.classification }}</v-chip
            >
          </v-flex>

          <v-flex v-if="resource.entropy">
            <v-layout align-center>
              <v-flex lg2>
                <v-label>Domain entropy</v-label>
              </v-flex>
              <v-flex>
                <v-chip class="font-weight-bold">{{
                  resource.entropy.toFixed(2)
                }}</v-chip>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-flex v-for="(blacklist, index) in resource.blacklist" :key="index">
          <v-layout align-center>
            <v-flex lg1>
              <v-label>Description</v-label>
            </v-flex>
            <v-flex lg3>
              <v-chip class="font-weight-bold">{{
                blacklist.description
              }}</v-chip>
            </v-flex>
            <v-flex offset-xs-1 lg1>
              <v-label>Source</v-label>
            </v-flex>
            <v-flex lg3>
              <v-chip class="font-weight-bold">{{ blacklist.source }}</v-chip>
            </v-flex>
            <v-flex offset-xs-1 lg1>
              <v-label>First seen</v-label>
            </v-flex>
            <v-flex>
              <v-chip>{{ blacklist.first_seen }}</v-chip>
            </v-flex>
            <v-flex offset-xs-1 lg1>
              <v-label>Last seen</v-label>
            </v-flex>
            <v-flex>
              <v-chip>{{ blacklist.last_seen }}</v-chip>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-divider></v-divider>
        <v-layout v-if="resource.tag && resource.tag.length > 0">
          <v-flex subheading>Tags</v-flex>
          <v-flex v-for="tag in resource.tag" :key="tag">
            <v-chip>{{ tag }}</v-chip>
          </v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "maltiverse",
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
  },
  methods: {
    classifier_color: function(classification) {
      if (classification === "malicious") {
        return "red";
      }

      if (classification === "suspicious") {
        return "orange";
      }

      return "blue";
    }
  }
};
</script>
