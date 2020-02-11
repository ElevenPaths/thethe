<template>
  <v-flex v-if="resource.response_code === 0" class="font-weight-medium" subheading>
    <v-card>
      <v-card-title>Resource is not in VirusTotal</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <span class="red--text">{{ resource.verbose_msg }}</span>
      </v-card-text>
    </v-card>
  </v-flex>
  <v-flex v-else class="text-xs-left">
    <v-layout wrap>
      <v-flex xs6 lg6 grow>
        <v-card v-if="resource.domain_siblings">
          <v-card-title class="subheading">
            <v-layout>
              <v-flex xs2>Siblings</v-flex>
              <v-flex xs2>
                <v-chip>{{ domain_siblings_filter_list.length }}</v-chip>
              </v-flex>
              <v-flex>
                <v-text-field
                  v-model="filter_siblings"
                  prepend-icon="filter_list"
                  label="Filter"
                  single-line
                  hide-details
                  clearable
                  class="pa-1 ma-0"
                ></v-text-field>
              </v-flex>

              <v-flex xs2>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      flat
                      color="grey"
                      v-on="on"
                      @click.stop="
                        copy_content(
                          transform_into_lines(domain_siblings_filter_list)
                        )
                      "
                    >
                      <v-icon>file_copy</v-icon>
                    </v-btn>
                  </template>
                  <span>Copy to clipboard</span>
                </v-tooltip>
              </v-flex>
            </v-layout>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex class="siblings_list">
              <div v-for="(domain, index) in domain_siblings_filter_list" :key="index">{{ domain }}</div>
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.whois" xs5 lg5>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>Whois</v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn flat color="grey" v-on="on" @click.stop="copy_content(resource.whois)">
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex>
              <v-textarea rows="10" readonly :value="resource.whois" class="caption"></v-textarea>
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.https_certificate_date" xs4 lg4 shrink>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>Certificate date</v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    color="grey"
                    v-on="on"
                    @click.stop="copy_content(resource.https_certificate_date)"
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy UNIX time to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex class="text-xs-center">
              {{
              get_time(resource.https_certificate_date)
              }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.dns_records_date" xs4 lg4 shrink>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>DNS record date</v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    color="grey"
                    v-on="on"
                    @click.stop="copy_content(resource.dns_records_date)"
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy UNIX time to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex class="text-xs-center">
              {{
              get_time(resource.dns_records_date)
              }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.undetected_downloaded_samples" xs10 lg10>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>Undetected downloaded samples</v-flex>
            <v-flex>
              <v-chip>
                {{
                resource.undetected_downloaded_samples.length
                }}
              </v-chip>
            </v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    color="grey"
                    v-on="on"
                    @click.stop="
                      copy_content(
                        resource.undetected_downloaded_samples
                          .map(elem => elem.sha256)
                          .join('\n')
                      )
                    "
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy hashes to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex>
              <v-card v-for="(item, index) in resource.undetected_downloaded_samples" :key="index">
                <v-card-title>
                  <v-flex>{{ item.sha256 }}</v-flex>
                  <v-flex>{{ item.date }}</v-flex>
                  <v-flex>
                    <v-progress-circular
                      :rotate="90"
                      :size="100"
                      :width="15"
                      :value="get_percentage(item.positives, item.total)"
                      :color="get_detection_color(item.positives, item.total)"
                    >
                      <span class="font-weight-bold">
                        {{
                        get_percentage(item.positives, item.total)
                        }}&nbsp;%
                      </span>
                    </v-progress-circular>
                  </v-flex>
                </v-card-title>
              </v-card>
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.detected_downloaded_samples" xs10 lg10>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>Detected downloaded samples</v-flex>
            <v-flex>
              <v-chip>{{ resource.detected_downloaded_samples.length }}</v-chip>
            </v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    color="grey"
                    v-on="on"
                    @click.stop="
                      copy_content(
                        resource.detected_downloaded_samples
                          .map(elem => elem.sha256)
                          .join('\n')
                      )
                    "
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy hashes to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex>
              <v-card v-for="(item, index) in resource.detected_downloaded_samples" :key="index">
                <v-card-title>
                  <v-flex>{{ item.sha256 }}</v-flex>
                  <v-flex>{{ item.date }}</v-flex>
                  <v-flex>
                    <v-progress-circular
                      :rotate="90"
                      :size="100"
                      :width="15"
                      :value="get_percentage(item.positives, item.total)"
                      :color="get_detection_color(item.positives, item.total)"
                    >
                      <span class="font-weight-bold">
                        {{
                        get_percentage(item.positives, item.total)
                        }}&nbsp;%
                      </span>
                    </v-progress-circular>
                  </v-flex>
                </v-card-title>
              </v-card>
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.detected_urls.length > 0" xs10 lg10>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>Detected URLs</v-flex>
            <v-flex>
              <v-chip>{{ resource.detected_urls.length }}</v-chip>
            </v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    color="grey"
                    v-on="on"
                    @click.stop="
                      copy_content(
                        resource.detected_urls.map(elem => elem.url).join('\n')
                      )
                    "
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy URLs to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex>
              <v-card v-for="(item, index) in resource.detected_urls" :key="index">
                <v-card-title>
                  <v-flex>{{ item.url }}</v-flex>
                  <v-flex>{{ item.scan_date }}</v-flex>
                  <v-flex>
                    <v-progress-circular
                      :rotate="90"
                      :size="100"
                      :width="15"
                      :value="get_percentage(item.positives, item.total)"
                      :color="get_detection_color(item.positives, item.total)"
                    >
                      <span class="font-weight-bold">
                        {{
                        get_percentage(item.positives, item.total)
                        }}&nbsp;%
                      </span>
                    </v-progress-circular>
                  </v-flex>
                </v-card-title>
              </v-card>
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.resolutions.length > 0" xs10 lg10>
        <v-card>
          <v-card-title class="subheading">
            <v-flex>Resolutions</v-flex>
            <v-flex>
              <v-chip>{{ resource.resolutions.length }}</v-chip>
            </v-flex>
            <v-spacer></v-spacer>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    flat
                    color="grey"
                    v-on="on"
                    @click.stop="
                      copy_content(
                      resource.resolutions.map(elem => elem.ip_address).join('\n')
                      )
                    "
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy IP to clipboard</span>
              </v-tooltip>
            </v-flex>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex>
              <v-card v-for="(item, index) in resource.resolutions" :key="index">
                <v-card-title>
                  <v-flex>{{ item.ip_address }}</v-flex>
                  <v-flex>{{ item.last_resolved }}</v-flex>
                </v-card-title>
              </v-card>
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-flex>
</template>

<script>
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "vt_domain",

  props: {
    plugin_data: Object
  },

  data: function() {
    return { filter_siblings: "" };
  },

  methods: {
    get_percentage: function(positives, total) {
      if (total == 0) return 0;

      return Math.round((positives / total) * 100);
    },

    get_detection_color: function(positives, total) {
      let percentage = this.get_percentage(positives, total);

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
    },

    copy_content: async function(elem) {
      await navigator.clipboard.writeText(elem);
    },

    transform_into_lines: function(items) {
      return items.join("\n");
    },

    get_time: function(t) {
      return from_python_time(t);
    }
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };
      // if (typeof plugin_result.undetected_downloaded_samples === "undefined") {
      //   plugin_result.undetected_downloaded_samples = [];
      // }
      // if (typeof plugin_result.detected_downloaded_samples === "undefined") {
      //   plugin_result.detected_downloaded_samples = [];
      // }
      return plugin_result;
    },

    domain_siblings_filter_list: function() {
      let siblings = this.resource.domain_siblings;

      if (!this.filter_siblings) {
        return siblings;
      } else {
        return siblings.filter(elem => {
          return elem.includes(this.filter_siblings);
        });
      }
    }
  }
};
</script>

<style scoped>
.siblings_list {
  max-height: 500px;
  overflow-y: auto;
}
</style>
