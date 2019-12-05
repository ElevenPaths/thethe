<template>
  <v-flex class="text-xs-left">
    <v-divider></v-divider>
    <v-layout row wrap class="subheading">
      <v-flex>
        <v-layout align-center>
          <v-flex lg1 title>Abuse Confidence Score</v-flex>
          <v-flex offset-lg1 lg2>
            <v-progress-circular
              :rotate="360"
              :size="100"
              :width="15"
              :value="resource.abuseConfidenceScore"
              :color="abuse_confidence_score_color"
              >{{ resource.abuseConfidenceScore }}%</v-progress-circular
            >
          </v-flex>
          <v-flex offset-lg1>
            <v-layout column>
              <v-layout>
                <v-flex lg2>Total reports</v-flex>
                <v-flex>{{ resource.totalReports }}</v-flex>
              </v-layout>
              <v-layout>
                <v-flex lg2>Distinc users</v-flex>
                <v-flex>{{ resource.numDistinctUsers }}</v-flex>
              </v-layout>
              <v-layout>
                <v-flex lg2>Domain</v-flex>
                <v-flex>{{ resource.domain }}</v-flex>
              </v-layout>
              <v-layout align-center>
                <v-flex lg2>Reported at</v-flex>
                <v-flex v-if="resource.lastReportedAt">
                  {{ new Date(resource.lastReportedAt).toLocaleDateString() }}
                  <v-chip>{{ days_ago }}</v-chip>
                  <span>days ago</span>
                </v-flex>
                <v-flex v-else>
                  <span>N/D</span>
                </v-flex>
              </v-layout>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "abuseipdb",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };
      return plugin_result.data;
    },
    abuse_confidence_score_color: function() {
      let score = this.resource.abuseConfidenceScore;

      if (score < 33) {
        return "yellow";
      } else if (score >= 33 && score <= 66) {
        return "orange";
      } else if (score > 66) {
        return "red";
      }

      return "blue";
    },

    days_ago: function() {
      let past = new Date(this.resource.lastReportedAt).getTime();
      let today = new Date().getTime();
      return Math.floor((today - past) / (24 * 60 * 60 * 60));
    }
  }
};
</script>
