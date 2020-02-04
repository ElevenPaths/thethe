<template>
  <v-layout class="pa-1">
    <v-flex :class="{ [`lg${grid_space}`]: true }" v-if="there_are_resources_in_list || search">
      <v-card
        v-on:dismiss="remove_resource = !remove_resource"
        v-on:dodelete="remove_resource_with_confirmation"
      >
        <v-card-title class="pa-0">
          <v-card-text>
            <v-flex class="subheading blue--text text--lighten-2 text-xs-center ma-0 pa-0">
              <v-flex>
                <slot name="title"></slot>
                ({{ resource_count }})
              </v-flex>
            </v-flex>
          </v-card-text>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-actions v-if="a_resource_is_selected">
          <v-flex px-2>
            <v-layout align-center justify-center row>
              <v-flex>
                <plugin-selector :resource="selected_resource">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                      <v-btn icon flat color="blue" v-on="on">
                        <v-icon>extension</v-icon>
                      </v-btn>
                    </template>
                    <span>Run plugins for this item</span>
                  </v-tooltip>
                </plugin-selector>
              </v-flex>
              <v-flex>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn icon flat color="orange" v-on="on" @click.stop="toggle_tags">
                      <v-icon>local_offer</v-icon>
                    </v-btn>
                  </template>
                  <span>Tag this item</span>
                </v-tooltip>
              </v-flex>
              <v-flex>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn icon flat color="green" v-on="on" @click.stop="copy_resource_to_json">
                      <v-icon>mdi-json</v-icon>
                    </v-btn>
                  </template>
                  <span>Copy to clipboard resource in JSON</span>
                </v-tooltip>
              </v-flex>

              <v-flex>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      flat
                      icon
                      color="red"
                      v-on="on"
                      @click.stop="remove_resource = !remove_resource"
                    >
                      <v-icon>delete_forever</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove item from project</span>
                </v-tooltip>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-card-actions>
        <v-card-title class="pa-1 ma-0" v-if="!a_resource_is_selected">
          <v-layout align-center>
            <v-flex>
              <v-text-field
                v-model="search"
                prepend-icon="search"
                label="Search"
                single-line
                hide-details
                clearable
                class="pa-1 ma-0"
              ></v-text-field>
            </v-flex>
            <v-flex>
              <v-chip>{{ resource_list.length }}/{{ resource_count }}</v-chip>
            </v-flex>
            <v-flex>
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn icon flat color="grey" v-on="on" @click.stop="copy_resource_list">
                    <v-icon>mdi-content-copy</v-icon>
                  </v-btn>
                </template>
                <span>Copy to clipboard resource list</span>
              </v-tooltip>
            </v-flex>
          </v-layout>
        </v-card-title>
        <v-flex>
          <v-list>
            <v-list-tile
              v-for="item in resource_list"
              :key="item._id"
              avatar
              @click="select_resource(item)"
              active-class="selected"
              :class="{ selected: selected_resource._id === item._id }"
            >
              <v-list-tile-content>
                <v-list-tile-title v-text="item.canonical_name"></v-list-tile-title>
                <v-list-tile-sub-title v-if="headers.length > 1">
                  {{
                  item[headers[1].value]
                  }}
                </v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-flex>
        <v-flex>
          <v-flex v-if="a_resource_is_selected">
            <v-divider></v-divider>
            <tags :resource="selected_resource" :show_tags="open_tags" @shake="tag_shake"></tags>
          </v-flex>
        </v-flex>
        <delete-dialog
          title="Are you sure?"
          text="This will unlink the resource from this project"
          :show="remove_resource"
        ></delete-dialog>
      </v-card>
    </v-flex>
    <v-flex v-if="!there_are_resources_in_list">
      <v-container bg fill-height grid-list-md text-xs-center>
        <v-layout justify-center align-center row wrap>
          <v-flex pt-5>
            <v-spacer>
              <div class="headline white--text">No resources yet</div>
            </v-spacer>
          </v-flex>
        </v-layout>
      </v-container>
    </v-flex>
    <resource-detail
      v-if="a_resource_is_selected"
      :resource="selected_resource"
      :grid_space="grid_space"
      :key="component_key"
    ></resource-detail>
    <v-flex v-if="!a_resource_is_selected && resource_list.length > 0">
      <v-flex>{{ selected_resource.tags }}</v-flex>
    </v-flex>
  </v-layout>
</template>

<script>
import DeleteDialog from "./DeleteDialog";
import ResourceDetail from "./ResourceDetail";
import PluginSelector from "./PluginSelector";
import Tags from "./Tags";

import { object_is_empty } from "../utils/utils";

export default {
  // 'data' must be a function if we don't want to share state between instantiation of the same components
  name: "resource-listing",
  components: {
    DeleteDialog,
    ResourceDetail,
    PluginSelector,
    Tags
  },
  props: {
    sortcriteria: {
      type: Function,
      default: (a, b) => {
        if (a.canonical_name < b.canonical_name) return -1;
        if (a.canonical_name > b.canonical_name) return 1;
        return 0;
      }
    },
    resourceType: String,
    headers: Array,
    grid_space: Number
  },
  data: function() {
    return {
      selected_resource: {},
      remove_resource: false,
      search: "",
      component_key: 0,
      resource_count: 0,
      open_tags: false
    };
  },
  computed: {
    resource_list: function() {
      let resources = this.$store.getters.get_resources(this.resourceType);
      this.resource_count = resources.length;

      resources = resources.sort(this.sortcriteria);

      if (!this.search) {
        return resources;
      } else {
        return resources.filter(resource => {
          // So users are able to search by a complete hash
          if (resource.resource_type === "hash") {
            return resource.hash.includes(this.search);
          } else {
            return resource.canonical_name.includes(this.search);
          }
        });
      }
    },

    there_are_resources_in_list: function() {
      return this.resource_list.length === 0 ? false : true;
    },

    a_resource_is_selected: function() {
      return !object_is_empty(this.selected_resource);
    }
  },
  methods: {
    copy_resource_to_json: async function() {
      await navigator.clipboard.writeText(
        JSON.stringify(this.selected_resource, null, 2)
      );
    },

    copy_resource_list: async function() {
      let resource_list = [];

      if (this.resource_list[0].resource_type === "hash") {
        resource_list = this.resource_list.map(elem => elem.hash).join("\n");
      } else {
        resource_list = this.resource_list
          .map(elem => elem.canonical_name)
          .join("\n");
      }

      await navigator.clipboard.writeText(resource_list);
    },

    select_resource: function(resource) {
      if (this.selected_resource._id === resource._id) {
        this.selected_resource = {};
      } else {
        this.selected_resource = resource;
        //TODO: Check if this (toggle_tags) is reactiveable good practice (bad smell) or it should be moved to watched
        this.open_tags = false;
        this.rerender_component();
      }
    },

    filter_by_name: function(resource, token) {
      return resource.name.search(token) === -1 ? false : true;
    },

    remove_resource_with_confirmation: function() {
      this.remove_resource = false;
      let payload = {
        resource_id: this.selected_resource._id
      };

      this.$store.dispatch("remove_resource", payload);
      this.selected_resource = {};
    },

    toggle_tags: function() {
      this.open_tags = !this.open_tags;
    },

    tag_shake: function() {
      let payload = {
        resource_id: this.selected_resource._id
      };
      this.$store.dispatch("update_resource", payload);
    },

    //HACK: This is a hack to re-render component details in other to maintain plugin tabs integrity
    // https://michaelnthiessen.com/force-re-render/
    rerender_component: function() {
      this.component_key += 1;
    }
  }
};
</script>

<style scoped>
.v-list {
  max-height: 500px;
  overflow-y: auto;
}
</style>
