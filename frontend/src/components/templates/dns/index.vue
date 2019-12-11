<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex v-if="not_null()">
      <v-flex lg4>
        <v-layout column>
          <v-flex>
            <v-flex v-if="resource.A">
              <v-card>
                <v-card-title primary-title>
                  <span class="subheading">Record A</span>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p
                    v-for="a_register in resource.A"
                    :key="a_register"
                    class="font-weight-bold"
                  >{{ a_register }}</p>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex v-if="resource.AAAA">
              <v-card>
                <v-card-title primary-title>
                  <span class="subheading">Record AAAA</span>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p v-for="aaaa_register in resource.AAAA" :key="aaaa_register">{{ aaaa_register }}</p>
                </v-card-text>
              </v-card>
            </v-flex>
          </v-flex>
        </v-layout>
      </v-flex>
      <v-flex lg4 v-if="resource.NS">
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <span class="subheading">Record NS</span>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <p v-for="ns_register in resource.NS" :key="ns_register">{{ ns_register }}</p>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-flex>
      <v-flex lg4 v-if="resource.MX" class="text-lg-left">
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <span class="subheading">Record MX</span>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <p v-for="mx_register in resource.MX" :key="mx_register">{{ mx_register }}</p>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-flex>
      <v-flex lg4 v-if="resource.SRV">
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Record SRV</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p v-for="srv_register in resource.SRV" :key="srv_register">{{ srv_register }}</p>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex lg12 v-if="resource.TXT" class="text-lg-left">
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <span class="subheading">Record TXT</span>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <p v-for="txt_register in resource.TXT" :key="txt_register">{{ txt_register }}</p>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-flex>
    </v-flex>
    <v-flex v-else text-xs-left>
      <v-layout>
        <v-flex pa-3>This resource does not have a DNS entry</v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "dns",
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
    not_null: function() {
      for (let property in this.resource) {
        if (this.resource[property]) {
          return true;
        }
      }
      return false;
    }
  }
};
</script>
