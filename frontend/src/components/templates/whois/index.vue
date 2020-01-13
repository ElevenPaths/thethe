<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex lg3>
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Names</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p
              v-for="domain_name in resource.domain_name"
              :key="domain_name"
              class="font-weight-bold"
            >{{ domain_name }}</p>
          </v-card-text>
        </v-card>
        <v-divider class="pt-3"></v-divider>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">DNS servers</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p v-for="dns in resource.name_servers" :key="dns">{{ dns }}</p>
          </v-card-text>
        </v-card>
        <v-divider class="pt-3"></v-divider>
        <v-card v-if="resource.whois_server">
          <v-card-title primary-title>
            <span class="subheading">Whois server</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-flex>{{ resource.whois_server }}</v-flex>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>

    <v-flex lg4>
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Dates</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-layout row>
              <v-flex lg-6 class="text-xs-left">
                <v-layout column>
                  <v-flex>
                    <v-label>Created:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Updated:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Expiration:</v-label>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex lg-6 class="text-xs-right">
                <v-layout column>
                  <v-flex>{{ resource.creation_date }}</v-flex>
                  <v-flex>{{ resource.updated_date }}</v-flex>
                  <v-flex>{{ resource.expiration_date }}</v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>

        <v-divider class="pt-3"></v-divider>
        <v-card v-if="resource.whois_server">
          <v-card-title primary-title>
            <span class="subheading">Contact</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="text-xs-left">
            <v-layout>
              <v-flex>
                <v-layout column>
                  <v-flex v-for="email in resource.emails" :key="email">
                    {{
                    email
                    }}
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>

    <v-flex lg5>
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Persona</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="text-xs-left">
            <v-layout column>
              <v-layout>
                <v-flex lg3>
                  <v-label>Registrar:</v-label>
                </v-flex>
                <v-flex>{{ resource.registrar }}</v-flex>
              </v-layout>
              <v-layout v-if="resource.registrar_url">
                <v-flex lg3>
                  <v-label>Registrar URL:</v-label>
                </v-flex>
                <v-flex>{{ resource.registrar_url }}</v-flex>
              </v-layout>
              <v-layout>
                <v-flex lg3>
                  <v-label>Organization:</v-label>
                </v-flex>
                <v-flex>
                  <v-layout column>
                    <v-flex>{{ resource.org }}</v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>

              <v-layout v-if="resource.name">
                <v-flex lg3>
                  <v-label>Name:</v-label>
                </v-flex>
                <v-flex>
                  <v-layout column>
                    <v-flex>{{ resource.name }}</v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-layout v-if="resource.address">
                <v-flex lg3>
                  <v-label>Address:</v-label>
                </v-flex>
                <v-flex>
                  <v-layout column>
                    <v-flex>{{ resource.address }}</v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-layout v-if="resource.city">
                <v-flex lg3>
                  <v-label>City:</v-label>
                </v-flex>
                <v-flex>
                  <v-layout column>
                    <v-flex>{{ resource.city }}</v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-layout v-if="resource.state">
                <v-flex lg3>
                  <v-label>State:</v-label>
                </v-flex>
                <v-flex>
                  <v-layout column>
                    <v-flex>{{ resource.state }}</v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-layout v-if="resource.zipcode">
                <v-flex lg3>
                  <v-label>Zipcode:</v-label>
                </v-flex>
                <v-flex>
                  <v-layout column>
                    <v-flex>{{ resource.zipcode }}</v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
              <v-layout v-if="resource.country">
                <v-flex lg3>
                  <v-label>Country:</v-label>
                </v-flex>
                <v-flex v-if="resource.country">
                  <v-layout column>
                    <v-flex>
                      <country-flag :country="resource.country"></country-flag>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "whois",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  methods: {
    is_country_code: function(code) {
      if (code.length > 3) {
        return false;
      }
    }
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };

      plugin_result.domain_name = make_unique_list(plugin_result.domain_name);

      plugin_result.creation_date = make_unique_list(
        plugin_result.creation_date
      )[0];

      plugin_result.expiration_date = make_unique_list(
        plugin_result.expiration_date
      )[0];

      plugin_result.updated_date = make_unique_list(
        plugin_result.updated_date
      )[0];

      plugin_result.name_servers = make_unique_list(plugin_result.name_servers);

      plugin_result.emails = make_unique_list(plugin_result.emails);

      plugin_result.org = make_unique_list(plugin_result.org, false)[0];

      if (plugin_result.country) {
        plugin_result.country = this.is_country_code(plugin_result.country);
      }

      return plugin_result;
    }
  }
};
</script>
