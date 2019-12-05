<template>
  <v-layout column pa-2 wrap>
    <v-flex>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading" v-if="resource.length > 0">
            This account has been found leaked in
            <b>{{ resource.length }}</b> sites
          </span>
          <span class="subheading" v-else
            >This account has not been found leaked in any site</span
          >
          <v-spacer></v-spacer>
          <v-chip class="body-1" label color="blue">
            Results brought thanks to&nbsp;
            <a href="https://haveibeenpwned.com/" rel="noreferer noopener"
              >haveibeenpwned.com</a
            >
          </v-chip>
        </v-card-title>
        <v-divider></v-divider>
        <v-card v-for="site in resource" :key="site.Name">
          <v-card-title>
            <v-flex lg1>
              <v-img :src="path_to_logo(site.LogoPath)" alt="Site logo"></v-img>
            </v-flex>
            <v-flex lg3 class="text-xs-left" offset-lg1>
              <v-layout column>
                <v-flex>
                  <v-label>Site:</v-label>
                  <span class="subheading">{{ site.Name }}</span>
                </v-flex>
                <v-flex>
                  <v-label>Leak name:</v-label>
                  <span class="subheading">{{ site.Title }}</span>
                </v-flex>
              </v-layout>
            </v-flex>
            <v-flex class="text-xs-left">
              <v-layout column>
                <v-flex>
                  <v-label>Breach date:</v-label>
                  <span class="subheading">{{
                    formatted_time(site.BreachDate)
                  }}</span>
                </v-flex>
                <v-flex>
                  <v-chip class="subheading"
                    >{{
                      new Intl.NumberFormat().format(site.PwnCount)
                    }}
                    leaks</v-chip
                  >
                </v-flex>
              </v-layout>
            </v-flex>

            <v-flex>
              <v-layout align-start justify-start row>
                <v-tooltip bottom v-if="site.IsVerified">
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      <v-flex justify-start lg2>
                        <v-icon color="green">done</v-icon>
                      </v-flex>
                    </span>
                  </template>
                  <span>Breach has been verified</span>
                </v-tooltip>
                <v-tooltip bottom v-else>
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      <v-flex lg2>
                        <v-icon color="red">clear</v-icon>
                      </v-flex>
                    </span>
                  </template>
                  <span>Breach has NOT been verified</span>
                </v-tooltip>

                <v-tooltip bottom v-if="site.IsFabricated">
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      <v-flex lg2>
                        <v-icon color="yellow">build</v-icon>
                      </v-flex>
                    </span>
                  </template>
                  <span>This leak has been fabricated</span>
                </v-tooltip>

                <v-tooltip bottom v-if="site.IsSensitived">
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      <v-flex lg2>
                        <v-icon color="orange">priority_high</v-icon>
                      </v-flex>
                    </span>
                  </template>
                  <span>This leak contain sensitive data!</span>
                </v-tooltip>

                <v-tooltip bottom v-if="site.IsRetired">
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      <v-flex lg2>
                        <v-icon>error_outline</v-icon>
                      </v-flex>
                    </span>
                  </template>
                  <span>This leak contain sensitive data!</span>
                </v-tooltip>

                <v-tooltip bottom v-if="site.IsSpamList">
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      <v-flex lg2>
                        <v-icon color="blue">subject</v-icon>
                      </v-flex>
                    </span>
                  </template>
                  <span>This leak was included in a SPAM list</span>
                </v-tooltip>
              </v-layout>
            </v-flex>

            <v-card-text class="text-xs-left">
              <v-layout>
                <v-flex lg1 class="title">
                  <v-label>Description</v-label>
                </v-flex>
                <v-flex offset-lg1>
                  <span v-html="site.Description"></span>
                </v-flex>
              </v-layout>
            </v-card-text>

            <v-card-text class="text-xs-left">
              <v-layout>
                <v-flex lg1 class="title">
                  <v-label>Data classes</v-label>
                </v-flex>
                <v-flex offset-lg1>
                  <v-chip
                    v-for="(_class, index) in site.DataClasses"
                    :key="index"
                    disabled
                    color="light-blue darken-4"
                    >{{ _class }}</v-chip
                  >
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card-title>
          <v-divider></v-divider>
        </v-card>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "haveibeenpwned",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let data = { ...this.plugin_data };
      return data.results;
    }
  },
  methods: {
    formatted_time: function(ts) {
      let t = new Date(ts);
      return `${t.toLocaleDateString()}`;
    },
    path_to_logo: function(path) {
      return "static/logos/" + path.split("/").slice(-1)[0];
    }
  }
};
</script>
