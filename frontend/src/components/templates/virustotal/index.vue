<template>
  <v-flex
    v-if="resource.response_code === 0"
    class="font-weight-medium"
    subheading
  >
    <v-card>
      <v-card-title>Resource is not in VirusTotal</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <span class="red--text">{{ resource.verbose_msg }}</span>
      </v-card-text>
    </v-card>
  </v-flex>
  <v-flex v-else class="text-xs-left">
    <v-card>
      <v-card-title class="title">VirusTotal information</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-layout v-if="resource.scan_date">
          <v-flex lg1>
            <v-label>Scan date</v-label>
          </v-flex>
          <v-flex>{{ resource.scan_date }}</v-flex>
        </v-layout>
        <v-layout v-if="resource.permalink">
          <v-flex lg1>
            <v-label>Link</v-label>
          </v-flex>
          <v-flex>
            <a
              rel="noopener nofollow"
              target="_blank"
              :href="resource.permalink"
              >{{ resource.permalink }}</a
            >
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-layout v-if="resource.md5">
          <v-flex lg1>
            <v-label>MD5</v-label>
          </v-flex>
          <v-flex>{{ resource.md5 }}</v-flex>
        </v-layout>
        <v-layout v-if="resource.sha1">
          <v-flex lg1>
            <v-label>SHA1</v-label>
          </v-flex>
          <v-flex>{{ resource.sha1 }}</v-flex>
        </v-layout>
        <v-layout v-if="resource.sha256">
          <v-flex lg1>
            <v-label>SHA256</v-label>
          </v-flex>
          <v-flex>{{ resource.sha256 }}</v-flex>
        </v-layout>
        <v-divider></v-divider>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="title">Detections</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-layout v-if="resource.positives">
          <v-flex lg2>
            <v-progress-circular
              :rotate="90"
              :size="100"
              :width="15"
              :value="get_percentage()"
              :color="get_detection_color()"
            >
              <span class="font-weight-bold"
                >{{ get_percentage() }}&nbsp;%</span
              >
            </v-progress-circular>
          </v-flex>
          <v-flex lg1>
            <v-layout column>
              <v-spacer></v-spacer>
              <v-layout>
                <v-flex lg10>
                  <v-label>Positives</v-label>
                </v-flex>
                <v-flex>{{ resource.positives }}</v-flex>
              </v-layout>
              <v-layout>
                <v-flex lg10>
                  <v-label>Total</v-label>
                </v-flex>
                <v-flex>{{ resource.total }}</v-flex>
              </v-layout>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
    <v-divider></v-divider>

    <v-card>
      <v-card-title class="title">Scans</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-list three-line>
          <v-list-tile
            v-for="(results, engine, index) in resource.scans"
            :key="index"
          >
            <v-list-tile-content>
              <v-list-tile-title v-html="engine"></v-list-tile-title>
              <v-list-tile-sub-title>
                <v-layout align-center>
                  <v-flex lg1>
                    <span>Detected</span>
                  </v-flex>
                  <v-flex lg1>
                    <v-chip :color="detected_color(results.detected)">{{
                      results.detected
                    }}</v-chip>
                  </v-flex>
                  <v-flex lg1>
                    <span>Result</span>
                  </v-flex>
                  <v-flex v-if="results.result" lg4>
                    <v-chip>{{ results.result }}</v-chip>
                  </v-flex>
                  <v-flex v-else lg4>
                    <v-chip>-</v-chip>
                  </v-flex>
                  <v-flex lg1 v-if="results.version">
                    <span>Version</span>
                  </v-flex>
                  <v-flex lg2 v-if="results.version">
                    <v-chip>{{ results.version }}</v-chip>
                  </v-flex>
                  <v-flex v-if="results.update">
                    <span>Update</span>
                  </v-flex>
                  <v-flex v-if="results.update">
                    <v-chip>{{ results.update }}</v-chip>
                  </v-flex>
                </v-layout>
              </v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "virustotal",

  props: {
    plugin_data: Object
  },

  data: function() {
    return {};
  },

  methods: {
    get_percentage: function() {
      return Math.round((this.resource.positives / this.resource.total) * 100);
    },

    get_detection_color: function() {
      let percentage = this.get_percentage();

      if (percentage === 0) {
        return "green";
      }

      if (percentage > 0 && percentage <= 50) {
        return "yellow";
      }

      if (percentage > 50 && percentage < 70) {
        return "orange";
      }

      return "red";
    },

    detected_color: function(detected) {
      if (detected) {
        return "red";
      } else {
        return "blue";
      }
    }
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };
      return plugin_result;
    }
  }
};
</script>
