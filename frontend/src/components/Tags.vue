<template>
  <v-flex>
    <v-flex v-if="resource.tags && resource.tags.length > 0">
      <v-flex>
        <v-btn
          v-for="tag in resource.tags"
          :key="tag.name"
          class="font-weight-bold text-lowercase"
          :color="tag.color"
          small
          round
        >
          {{ tag.name }}
          <v-icon @click.stop="tag_to_resource(tag)" right>mdi-close-circle</v-icon>
        </v-btn>
      </v-flex>
    </v-flex>
    <v-flex v-else>No tags</v-flex>

    <v-flex v-if="show_tags">
      <v-flex v-if="tags.length > 0">
        <v-label>Available tags</v-label>
        <v-flex>
          <v-btn
            v-for="tag in available_tags"
            :key="tag.name"
            :color="tag.color"
            class="font-weight-bold text-lowercase"
            small
            round
            @click="tag_to_resource(tag)"
          >{{ tag.name }}</v-btn>
        </v-flex>
      </v-flex>
      <v-flex v-else>No tags yet</v-flex>
      <v-flex>
        <v-dialog v-model="tag_dialog" width="250">
          <template v-slot:activator="{ on }">
            <v-btn flat icon v-on="on">
              <v-icon color="green">mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>Name</v-card-title>
            <v-card-text>
              <v-text-field
                outline
                single-line
                required
                v-model.trim="new_tag_name"
                label="no spaces, only alpha"
                ref="tag_name_field"
              ></v-text-field>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-title>Color</v-card-title>
            <v-layout row pb-3>
              <v-flex xs12>
                <v-btn
                  v-for="color in tag_colors"
                  :key="color"
                  :value="color"
                  fab
                  dark
                  small
                  :color="color"
                  @click.stop="new_tag_color = color"
                ></v-btn>
              </v-flex>
            </v-layout>
            <v-divider></v-divider>
            <v-card-actions>
              <v-flex>
                <v-btn color="primary" @click.stop="new_tag()">add</v-btn>
              </v-flex>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-flex>
    </v-flex>
  </v-flex>
</template>

<script>
import api_call from "../utils/api";

export default {
  name: "Tags",
  props: {
    resource: {
      type: Object,
      default: {}
    },
    show_tags: { type: Boolean, default: false }
  },
  data() {
    return {
      tags: [],
      tag_dialog: false,
      tag_colors: [],
      new_tag_name: null,
      new_tag_color: "blue"
    };
  },

  computed: {
    available_tags: function() {
      if (this.resource.tags === undefined) {
        return this.tags;
      }

      return this.tags.filter(
        that_tag =>
          !this.resource.tags.some(elem => elem.name === that_tag.name)
      );
    }
  },
  methods: {
    new_tag() {
      this.tag_dialog = !this.tag_dialog;
      let tag = { name: this.new_tag_name, color: this.new_tag_color };
      let payload = {
        url: "/api/add_new_tag",
        tag: tag
      };
      api_call(payload);

      this.new_tag_color = "blue";
      this.$refs.tag_name_field.reset();
      this.load_tags();
    },

    load_tags() {
      let payload = {
        url: "/api/get_tags"
      };
      api_call(payload).then(resp => (this.tags = resp.data.tags));

      payload = {
        url: "/api/get_tag_colors"
      };
      api_call(payload).then(resp => (this.tag_colors = resp.data.tag_colors));
    },

    tag_to_resource(tag) {
      let payload = {
        url: "/api/tag_to_resource",
        resource_id: this.resource._id,
        resource_type: this.resource.resource_type,
        tag: tag
      };
      api_call(payload).then(resp => {
        this.$emit("shake");
      });
    }
  },
  mounted: function() {
    this.load_tags();
  }
};
</script>
