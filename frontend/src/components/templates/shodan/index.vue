<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex lg5>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading">Hostnames</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <p
            v-for="(hostname, index) in resource.results.hostnames"
            :key="index"
            class="font-weight-bold"
          >
            {{ hostname }}
          </p>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex lg5>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading">Info</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="text-sm-left">
          <v-layout v-if="resource.results.os">
            <v-flex lg6>
              <v-label>OS:</v-label>
            </v-flex>
            <v-flex lg6>{{ resource.results.os }}</v-flex>
          </v-layout>

          <v-layout v-if="resource.results.org">
            <v-flex lg6>
              <v-label>Organization:</v-label>
            </v-flex>
            <v-flex lg6>{{ resource.results.org }}</v-flex>
          </v-layout>

          <v-layout v-if="resource.results.isp">
            <v-flex lg6>
              <v-label>ISP:</v-label>
            </v-flex>
            <v-flex lg6>{{ resource.results.isp }}</v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex lg12>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading">Services</span>
          <v-chip>{{ resource.results.services.length }}</v-chip>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text
          v-for="(service, index) in resource.results.services"
          :key="index"
        >
          <v-flex lg12>
            <v-layout
              v-if="service.transport || service.port || service.timestamp"
            >
              <v-flex lg4 pt-0>
                <v-chip label color="blue" class="font-weight-bold">
                  <v-icon left>call</v-icon>
                  {{ service.transport }}/{{ service.port }}
                </v-chip>
              </v-flex>
              <v-flex lg1 v-if="service.timestamp">
                <v-icon>access_time</v-icon>
              </v-flex>
              <v-flex lg3 v-if="service.timestamp">{{
                formatted_time(service.timestamp)
              }}</v-flex>
            </v-layout>
          </v-flex>

          <v-flex lg12 v-if="service.banner">
            <v-layout>
              <v-flex lg1>
                <v-label>Banner:</v-label>
              </v-flex>
              <v-flex>{{ service.banner }}</v-flex>
            </v-layout>
          </v-flex>

          <v-flex lg12 v-if="service.devicetype">
            <v-layout>
              <v-flex lg1>
                <v-label>Device type:</v-label>
              </v-flex>
              <v-flex>{{ service.devicetype }}</v-flex>
            </v-layout>
          </v-flex>

          <v-flex lg12 v-if="service.product">
            <v-layout>
              <v-flex lg1>
                <v-label>Product:</v-label>
              </v-flex>
              <v-flex>{{ service.product }}</v-flex>
            </v-layout>
          </v-flex>

          <v-flex lg12 v-if="service.data">
            <v-layout>
              <v-flex>
                <v-expansion-panel>
                  <v-expansion-panel-content>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on }">
                        <v-btn
                          flat
                          color="grey"
                          v-on="on"
                          @click.stop="copy_content(service.data)"
                        >
                          <v-icon>file_copy</v-icon>
                        </v-btn>
                      </template>
                      <span>Copy to clipboard</span>
                    </v-tooltip>

                    <template v-slot:header>
                      <v-label>Service probe (click to expand)</v-label>
                    </template>
                    <v-card>
                      <v-card-text>
                        <v-textarea
                          :value="service.data"
                          :readonly="true"
                          rows="16"
                          box
                        ></v-textarea>
                      </v-card-text>
                    </v-card>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "shodan",
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
