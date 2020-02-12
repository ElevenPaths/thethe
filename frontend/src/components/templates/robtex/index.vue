<template>
  <v-layout row pt-2 wrap class="subheading">
    <template v-if="resource.results.status === 'ok'">
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">AS</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="text-xs-left">
            <v-flex>
              <v-label>AS:</v-label>
              {{ resource.results.as }}
            </v-flex>
            <v-flex>
              <v-label>name:</v-label>
              {{ resource.results.asname }}
            </v-flex>
            <v-flex>
              <v-label>description:</v-label>
              {{ resource.results.asdesc }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">BGP Route</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="text-xs-left">
            <v-flex>
              <v-label>whois-desc:</v-label>
              {{ resource.results.whoisdesc }}
            </v-flex>
            <v-flex>
              <v-label>route-desc:</v-label>
              {{ resource.results.routedesc }}
            </v-flex>
            <v-flex>
              <v-label>bgp-route:</v-label>
              {{ resource.results.bgproute }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Geo</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="text-xs-left">
            <v-flex>
              <v-label>City:</v-label>
              {{ resource.results.city }}
            </v-flex>
            <v-flex>
              <v-label>Country:</v-label>
              {{ resource.results.country }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.results.act && resource.results.act.length > 0">
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Active (forward) DNS</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text
            class="text-xs-left"
            v-for="(entry, index) in resource.results.act"
            :key="index"
          >
            <v-flex>
              <v-label>domain:</v-label>
              {{ entry.o }}
            </v-flex>
            <v-flex>
              <v-label>timestamp:</v-label>
              {{ formatted_time(entry.t) }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.results.acth && resource.results.acth.length > 0">
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Active DNS history</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text
            class="text-xs-left"
            v-for="(entry, index) in resource.results.acth"
            :key="index"
          >
            <v-flex>
              <v-label>domain:</v-label>
              {{ entry.o }}
            </v-flex>
            <v-flex>
              <v-label>timestamp:</v-label>
              {{ formatted_time(entry.t) }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.results.pas && resource.results.pas.length > 0">
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Pasive DNS</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text
            class="text-xs-left"
            v-for="(entry, index) in resource.results.pas"
            :key="index"
          >
            <v-flex>
              <v-label>domain:</v-label>
              {{ entry.o }}
            </v-flex>
            <v-flex>
              <v-label>timestamp:</v-label>
              {{ formatted_time(entry.t) }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex v-if="resource.results.pash && resource.results.pash.length > 0">
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Pasive DNS history</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text
            class="text-xs-left"
            v-for="(entry, index) in resource.results.pash"
            :key="index"
          >
            <v-flex>
              <v-label>domain:</v-label>
              {{ entry.o }}
            </v-flex>
            <v-flex>
              <v-label>timestamp:</v-label>
              {{ formatted_time(entry.t) }}
            </v-flex>
          </v-card-text>
        </v-card>
      </v-flex>
    </template>
    <template v-else>
      <v-flex>Robtex plugin ran but the response status was not ok</v-flex>
    </template>
  </v-layout>
</template>

<script>
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "robtex",
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
      return from_python_time(ts);
    },
    copy_content: async function(data) {
      await navigator.clipboard.writeText(data);
    }
  }
};
</script>
