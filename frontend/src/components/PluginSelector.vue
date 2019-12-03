<template>
  <div class="text-xs-center">
    <v-bottom-sheet v-model="sheet" inset>
      <template v-slot:activator>
        <slot></slot>
      </template>
      <v-list>
        <v-subheader>
          <b>Available plugins</b>&nbsp; (click on a entry to launch task)
        </v-subheader>
        <v-divider></v-divider>
        <v-list-tile
          v-for="plugin in plugin_list"
          :key="plugin.name"
          @click="launch(plugin); sheet = false"
          two-line
        >
          <v-list-tile-avatar>
            <v-icon v-if="plugin.is_active" :color="avatar_color(plugin.last_update)">warning</v-icon>
            <v-icon v-else :color="avatar_color(plugin.last_update)">info</v-icon>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ plugin.name }}</v-list-tile-title>
            <v-list-tile-sub-title>
              <v-layout align-center>
                <v-flex lg6>{{ plugin.description }}</v-flex>
                <v-flex v-if="plugin.last_update">
                  <v-layout align-center>
                    <span>Last update:&nbsp;</span>
                    <span>{{ plugin.last_update }}</span>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
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
  methods: {
    launch: function(entry) {
      let params = {
        url: "/api/launch_plugin",
        resource_id: this.resource._id,
        resource_type: this.resource.resource_type,
        plugin_name: entry.name
      };

      // TODO: Signal plugin launching
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
