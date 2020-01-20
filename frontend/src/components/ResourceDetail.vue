<template>
  <v-flex :class="{ [`lg${12 - grid_space}`]: true }">
    <v-card>
      <v-card-title primary-title v-if="resource" class="py-1">
        <v-card-text
          v-if="resource.resource_type === 'hash'"
          class="subheading text-xs-center pa-0"
          >{{ resource.hash }}</v-card-text
        >
        <v-card-text v-else class="subheading text-xs-center pa-0">{{
          resource.canonical_name
        }}</v-card-text>
      </v-card-title>
      <v-divider></v-divider>
      <v-tabs
        slider-color="red"
        v-model="active"
        v-if="resource.plugins.length > 0"
      >
        <v-tab ripple v-for="entry in sorted_plugin_list" :key="entry.index">{{
          entry.plugin.name
        }}</v-tab>
        <v-tabs-items>
          <v-tab-item v-for="entry in sorted_plugin_list" :key="entry.index" lazy>
            <dynamic-link
              :type="entry.plugin.name"
              :data="entry.plugin"
              :key="component_key"
            ></dynamic-link>
            <v-divider></v-divider>
            <v-flex>
              <v-layout column>
                <v-flex
                  v-if="entry.plugin.creation_time"
                  lg3
                  caption
                  text-xs-left
                  >Created:
                  {{ from_python_time(entry.plugin.creation_time) }}</v-flex
                >
                <v-flex v-if="entry.plugin.update_time" caption text-xs-left
                  >Last update:
                  {{ from_python_time(entry.plugin.update_time) }}</v-flex
                >
              </v-layout>
            </v-flex>
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
      <v-card-title primary-title v-else>
        <v-flex class="subheading text-xs-center">There is no data yet</v-flex>
      </v-card-title>
      <v-card-actions></v-card-actions>
    </v-card>
  </v-flex>
</template>

<script>
import DynamicLink from "./DynamicComponent";
import { from_python_time } from "../utils/utils";

export default {
  name: "resource-detail",
  props: {
    grid_space: Number,
    resource: Object
  },
  components: { DynamicLink },
  data: function() {
    return { active: 0, component_key: 0 };
  },
  computed: {
    sorted_plugin_list: function() {
      let plugins = this.resource.plugins.sort((a, b) => {
        if (a.name > b.name) {
          return 1;
        }

        if (a.name < b.name) {
          return -1;
        }

        return 0;
      });

      let plugin_list = [];
      for (const [i, plugin] of plugins.entries()) {
        plugin_list.push({ index: i, plugin: plugin });
      }
      return plugin_list;
    }
  },
  methods: {
    from_python_time: from_python_time
  },
  watch: {
    resource: {
      //HACK: Again, to reload dynamic component when new data arrives
      // https://michaelnthiessen.com/how-to-watch-nested-data-vue
      deep: true,
      handler: function() {
        this.component_key += 1;
      }
    }
  }
};
</script>
