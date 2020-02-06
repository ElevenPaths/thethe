<template>
  <div class="text-xs-center">
    <v-bottom-sheet v-model="sheet" inset>
      <template v-slot:activator>
        <slot></slot>
      </template>
      <v-list>
        <v-subheader>
          <span
            ><b>Available plugins</b>&nbsp; (click on a entry to launch
            task)</span
          >
        </v-subheader>
        <v-divider></v-divider>
        <v-list-tile
          v-for="plugin in plugin_list"
          :key="plugin.name"
          avatar
          two-line
        >
          <v-list-tile-avatar>
            <v-btn
              v-if="!plugin.apikey_in_ddbb && plugin.api_key"
              flat
              icon
              color="error"
              :href="plugin.api_doc"
              target="_blank"
            >
              <v-icon>
                warning
              </v-icon>
            </v-btn>
            <v-btn v-else flat icon style="visibility: hidden">
              <v-icon>
                warning
              </v-icon>
            </v-btn>
          </v-list-tile-avatar>
          <v-layout>
            <v-list-tile-avatar class="pt-2">
              <v-icon
                v-if="plugin.is_active"
                :color="avatar_color(plugin.last_update)"
                >warning</v-icon
              >
              <v-icon v-else :color="avatar_color(plugin.last_update)">
                info
              </v-icon>
            </v-list-tile-avatar>
            <v-btn
              class="text-lowercase"
              block
              large
              flat
              @click="
                launch(plugin);
                sheet = false;
              "
            >
              <v-list-tile-content>
                <v-list-tile-title class="subheading">{{
                  plugin.name
                }}</v-list-tile-title>
                <v-list-tile-sub-title>
                  <v-layout align-center>
                    <v-flex lg8>{{ plugin.description }}</v-flex>
                    <v-flex offset-lg1 v-if="plugin.last_update">
                      <v-layout align-center>
                        <span>Last update:&nbsp;</span>
                        <span>{{ plugin.last_update }}</span>
                      </v-layout>
                    </v-flex>
                  </v-layout>
                </v-list-tile-sub-title>
              </v-list-tile-content>
            </v-btn>
          </v-layout>
        </v-list-tile>
        <v-divider></v-divider>
        <v-subheader>
          <v-icon color="error" style="margin: 0px 8px">
            warning
          </v-icon>
          <span style="padding: 0px 10px"><b>API KEY needed!</b></span>
        </v-subheader>
      </v-list>
    </v-bottom-sheet>
  </div>
</template>

<script>
import api_call from "../utils/api";

export default {
  name: "PluginSelector",
  props: { resource: Object },
  data() {
    return {
      sheet: false,
      plugin_list: []
    };
  },
  mounted: function() {
    this.get_related_plugins();
  },
  methods: {
    get_related_plugins: function() {
      let params = {
        url: "/api/get_related_plugins",
        resource_id: this.resource._id,
        resource_type: this.resource.resource_type,
        project_id: this.$store.getters["get_opened_project"]._id
      };

      api_call(params)
        .then(resp => {
          this.plugin_list = resp.data;
        })
        .then(resp => this.update_pluginglist_dates());
    },
    loading: function(plugin) {
      this.$store.dispatch("loading", {
        _id: this.resource._id,
        resourceType: this.resource.resource_type,
        plugin: plugin
      });
    },
    launch: function(entry) {
      let params = {
        url: "/api/launch_plugin",
        resource_id: this.resource._id,
        resource_type: this.resource.resource_type,
        plugin_name: entry.name
      };

      this.loading(entry.name);
      api_call(params);
    },

    formatted_time: function(ts) {
      if (!ts) {
        return "Not launched yet";
      }
      let t = new Date(ts * 1000);
      return `${t.toLocaleDateString()} at ${t.toLocaleTimeString()}`;
    },

    avatar_color: function(date) {
      if (date !== null) return "blue";
      return "green";
    },

    update_pluginglist_dates: function() {
      for (let plugin of this.plugin_list) {
        let match = this.resource.plugins.find(
          elem => elem.name.localeCompare(plugin.name) == 0
        );
        if (typeof match !== "undefined") {
          plugin.last_update = this.formatted_time(match.update_time);
        } else {
          plugin.last_update = null;
        }
      }
    }
  },
  watch: {
    resource: {
      deep: true,
      handler: function() {
        this.update_pluginglist_dates();
      }
    }
  }
};
</script>
