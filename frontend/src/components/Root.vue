<template>
  <v-app :dark="true">
    <v-toolbar class="grey darken-3" dark flat dense>
      <!-- <v-toolbar-title class="light-grey--text">TheehT</v-toolbar-title> -->
      <img src="static/images/thethe_big.png" height="36" width="100" />
      <v-spacer></v-spacer>
      <v-chip
        label
        color="primary"
        v-if="is_project_opened"
        class="ma-2 title"
      >{{ get_opened_project.name }}</v-chip>
      <v-menu offset-y dark>
        <template v-slot:activator="{ on }">
          <v-avatar size="36" color="#666666" v-on="on">
            <v-icon dark>mdi-account-circle-outline</v-icon>
          </v-avatar>
        </template>
        <v-list class="text-lg-left">
          <v-list-tile @click="switch_project" v-if="is_project_opened">
            <v-list-tile-avatar>
              <v-icon>eject</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>Change project</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-divider></v-divider>

          <v-list-tile class="caption" @click.stop="show_apikeys_f(true)">
            <api-keys :show="show_apikeys" @apikeys-closed="show_apikeys_f(false)"></api-keys>

            <v-list-tile-avatar>
              <v-icon>call</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>API Keys</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-divider></v-divider>
          <v-list-tile @click="logout" class="caption">
            <v-list-tile-avatar>
              <v-icon>logout</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>Logout</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
    <v-container fluid grid-list-lg pt-1 px-0>
      <div v-if="!is_project_opened">
        <project-selector></project-selector>
      </div>
      <v-flex v-else>
        <v-tabs v-model="active" slider-color="red">
          <v-tab ripple>NETWORK</v-tab>
          <v-tab ripple>DOMAIN</v-tab>
          <v-tab ripple>URL</v-tab>
          <v-tab ripple>HASH</v-tab>
          <v-tab ripple>EMAILS</v-tab>
          <v-tab ripple>USERNAMES</v-tab>
          <v-spacer></v-spacer>
          <v-tab ripple>FLOW</v-tab>
          <v-tab ripple>ANALYSIS</v-tab>
          <v-tabs-items>
            <v-tab-item>
              <v-layout wrap>
                <v-flex>
                  <resource-listing
                    :sortcriteria="sort_ip_addresses"
                    :headers="ip_table_headers"
                    :resourceDescription="ip_resource_description"
                    :grid_space="3"
                  >
                    <template v-slot:title>IP Address</template>
                  </resource-listing>
                </v-flex>
              </v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-layout wrap>
                <v-flex>
                  <resource-listing
                    :resourceDescription="domain_resource_description"
                    :headers="domain_table_headers"
                    :grid_space="3"
                  >
                    <template v-slot:title>Domains</template>
                  </resource-listing>
                </v-flex>
              </v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-layout row wrap>
                <v-flex>
                  <resource-listing
                    :resourceDescription="url_resource_description"
                    :headers="url_table_headers"
                    :grid_space="4"
                  >
                    <template v-slot:title>URLs</template>
                  </resource-listing>
                </v-flex>
              </v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-layout row wrap>
                <v-flex>
                  <resource-listing
                    :resourceDescription="hash_resource_description"
                    :headers="hash_table_headers"
                    :grid_space="3"
                  >
                    <template v-slot:title>Hashes</template>
                  </resource-listing>
                </v-flex>
              </v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-layout row wrap>
                <v-flex>
                  <resource-listing
                    :resourceDescription="email_resource_description"
                    :headers="email_table_headers"
                    :grid_space="3"
                  >
                    <template v-slot:title>Emails</template>
                  </resource-listing>
                </v-flex>
              </v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-layout row wrap>
                <v-flex>
                  <resource-listing
                    :resourceDescription="username_resource_description"
                    :headers="username_table_headers"
                    :grid_space="3"
                  >
                    <template v-slot:title>Usernames</template>
                  </resource-listing>
                </v-flex>
              </v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-layout row wrap pt-2>Flows</v-layout>
            </v-tab-item>
            <v-tab-item>
              <v-flex offset-lg1 lg10>
                <simple-vis-network></simple-vis-network>
              </v-flex>
            </v-tab-item>
          </v-tabs-items>
        </v-tabs>
      </v-flex>
      <resource-input v-if="is_project_opened"></resource-input>
    </v-container>
    <status-bar></status-bar>
    <notifications position="bottom right" :ignoreDuplicates="true" />
  </v-app>
</template>

<script>
import ResourceListing from "./ResourceListing";
import ProjectSelector from "./ProjectSelector";
import ResourceInput from "./ResourceInput";
import SimpleVisNetwork from "./SimpleVisNetwork";
import ApiKeys from "./ApiKeys";

import StatusBar from "./StatusBar";

import { AUTH_LOGOUT } from "../store/actions/auth";
import { RESET_PROJECT } from "../store/actions/project";
import { mapGetters } from "vuex";
import compare_ip_addreses from "../utils/sort";

export default {
  components: {
    ResourceListing,
    ProjectSelector,
    ResourceInput,
    StatusBar,
    SimpleVisNetwork,
    ApiKeys
  },

  data: function() {
    return {
      active: null,
      show_apikeys: false,
      hash_resource_description: {
        type: "hash",
        resource_list: "hashlist"
      },
      ip_resource_description: {
        type: "ip",
        resource_list: "iplist"
      },
      domain_resource_description: {
        type: "domain",
        resource_list: "domainlist"
      },
      email_resource_description: {
        type: "email",
        resource_list: "emaillist"
      },
      username_resource_description: {
        type: "username",
        resource_list: "usernamelist"
      },
      url_resource_description: {
        type: "url",
        resource_list: "urllist"
      },
      ip_table_headers: [
        {
          text: "IP",
          value: "address"
        }
      ],
      domain_table_headers: [
        {
          text: "DOMAIN",
          value: "domain"
        }
      ],
      email_table_headers: [
        {
          text: "EMAIL",
          value: "email"
        }
      ],
      username_table_headers: [
        {
          text: "USERNAME",
          value: "username"
        }
      ],
      hash_table_headers: [
        {
          text: "HASH",
          value: "hash"
        },
        {
          text: "TYPE",
          value: "hash_type"
        }
      ],
      url_table_headers: [
        {
          text: "URL",
          value: "full_url"
        }
      ],
      sort_ip_addresses: compare_ip_addreses
    };
  },

  methods: {
    logout: function() {
      this.$store
        .dispatch(AUTH_LOGOUT)
        .then(() => {
          this.$store.dispatch(RESET_PROJECT);
        })
        .then(() => {
          this.$router.push("/login");
        });
    },

    show_apikeys_f: function(show) {
      this.show_apikeys = show;
    },

    //TODO: Before switch project check if there are pending operations
    switch_project: function() {
      this.$store.dispatch(RESET_PROJECT);
    }
  },

  computed: {
    ...mapGetters(["get_opened_project", "is_project_opened"]),
    username: function() {
      return this.$store.getters["username"];
    }
  },

  mounted: function() {
    setInterval(() => {
      this.$store.dispatch("update");
    }, 10000);
  }

  //TODO: Commented to let dev mode be kind when reloading components
  /*   beforeMount: function() {
    if (this.$store.getters["auth_status"] === "") {
      this.$router.push("/login");
    }
  } */
};
</script>

<style>
.selected {
  background-color: #666666;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgb(48, 47, 47);
  box-shadow: inset 0 0 6px rgb(46, 31, 31);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgb(95, 94, 94);
  box-shadow: inset 0 0 6px rgb(117, 115, 115);
}
</style>
