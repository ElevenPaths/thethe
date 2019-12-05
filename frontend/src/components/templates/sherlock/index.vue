<template>
  <v-layout column pa-2 wrap>
    <v-flex>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading"
            >Found a user in {{ found_ones_length }} sites</span
          >
          <v-spacer></v-spacer>
          <v-chip class="body-1" label color="amber darken-4"
            >(be aware it might not be the same persona)</v-chip
          >
        </v-card-title>
        <v-divider></v-divider>
        <v-layout>
          <v-flex>
            <v-list two-line>
              <v-list-tile v-for="(entry, index) in found_ones(0)" :key="index">
                <v-list-tile-avatar>
                  <img
                    :src="get_favicon(entry.sitename)"
                    onerror="this.src='../../static/favicons/thethe_default.png'"
                  />
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title class="body-1">{{
                    entry.sitename
                  }}</v-list-tile-title>
                  <v-list-tile-sub-title class="body-2">
                    <a
                      target="_blank"
                      rel="noopener noreferer"
                      :href="entry.url_user"
                      >{{ entry.url_user }}</a
                    >
                  </v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-flex>
          <v-flex>
            <v-list two-line v-if="found_ones(1)">
              <v-list-tile v-for="(entry, index) in found_ones(1)" :key="index">
                <v-list-tile-avatar>
                  <img
                    :src="get_favicon(entry.sitename)"
                    onerror="this.src='../../static/favicons/thethe_default.png'"
                  />
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title class="body-1">{{
                    entry.sitename
                  }}</v-list-tile-title>
                  <v-list-tile-sub-title class="body-2">
                    <a
                      target="_blank"
                      rel="noopener noreferer"
                      :href="entry.url_user"
                      >{{ entry.url_user }}</a
                    >
                  </v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>

    <v-flex lg4 v-if="show_not_found">
      <v-card>
        <v-card-title primary-title>
          <span class="subheading">Not found</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-list two-line>
          <v-list-tile v-for="(entry, index) in not_found_ones" :key="index">
            <v-list-tile-avatar>
              <img :src="get_favicon(entry.sitename)" />
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title class="body-1">{{
                entry.sitename
              }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "sherlock",
  props: {
    plugin_data: Object
  },
  data: function() {
    return { show_not_found: false };
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data };
      return plugin_result;
    },

    found_ones_length: function() {
      return this.plugin_data.results.filter(elem => elem.exists === "yes")
        .length;
    },

    not_found_ones: function() {
      return this.plugin_data.results.filter(elem => elem.exists === "no");
    }
  },
  methods: {
    formatted_time: function(ts) {
      let t = new Date(ts);
      return `${t.toLocaleDateString()} at ${t.toLocaleTimeString()}`;
    },

    get_favicon: function(sitename) {
      return "../../static/favicons/" + sitename.toLowerCase() + ".ico";
    },

    found_ones: function(page) {
      let ordered_list = this.plugin_data.results
        .filter(elem => elem.exists === "yes")
        .sort();

      let items_per_page = ordered_list.length / 2;

      if (items_per_page < 1) {
        if (page > 0) {
          return null;
        } else {
          return ordered_list;
        }
      } else {
        return ordered_list.slice(
          page * items_per_page,
          items_per_page + page * items_per_page
        );
      }
    }
  }
};
</script>
