<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex lg5>
      <v-flex>
        <v-card v-if="!resource.ptr.length == 'N/D'">
          <v-card-title primary-title>
            <span class="subheading">PTR</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p
              v-for="ptr_record in resource.ptr"
              :key="ptr_record"
              class="font-weight-bold"
            >
              {{ ptr_record }}
            </p>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Network</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-layout row>
              <v-flex lg-6 class="text-xs-left">
                <v-layout column>
                  <v-flex>
                    <v-label>CIDR:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Handle:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Name:</v-label>
                  </v-flex>
                  <v-flex v-if="resource.network.country">
                    <v-label>Country:</v-label>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex lg-6 class="text-xs-right">
                <v-layout column>
                  <v-flex>{{ resource.network.cidr }}</v-flex>
                  <v-flex>{{ resource.network.handle }}</v-flex>
                  <v-flex>{{ resource.network.name }}</v-flex>
                  <v-flex v-if="resource.network.country">
                    <country-flag
                      :country="resource.network.country"
                    ></country-flag>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>

    <v-flex>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading">ASN</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-layout row>
            <v-flex lg-3 class="text-xs-left">
              <v-layout column>
                <v-flex>
                  <v-label>Number:</v-label>
                </v-flex>
                <v-flex>
                  <v-label>CIDR:</v-label>
                </v-flex>
                <v-flex>
                  <v-label>Date:</v-label>
                </v-flex>
                <v-flex>
                  <v-label>Description:</v-label>
                </v-flex>
                <v-flex>
                  <v-label>Registry:</v-label>
                </v-flex>
                <v-flex>
                  <v-label>Country:</v-label>
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex class="text-xs-right">
              <v-layout column>
                <v-flex>{{ resource.asn.asn }}</v-flex>
                <v-flex>{{ resource.asn.asn_cidr }}</v-flex>
                <v-flex>{{ resource.asn.asn_date }}</v-flex>
                <v-flex>{{ resource.asn.asn_description }}</v-flex>
                <v-flex>{{ resource.asn.asn_registry }}</v-flex>
                <v-flex>
                  <country-flag
                    :country="resource.asn.asn_country_code"
                  ></country-flag>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "basic",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };

      plugin_result.ptr = make_unique_list(plugin_result.ptr);

      return plugin_result;
    }
  }
};
</script>
