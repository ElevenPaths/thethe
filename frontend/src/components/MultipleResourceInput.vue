<template>
  <v-layout row>
    <v-dialog v-model="dialog" width="700">
      <template v-slot:activator="{ on }">
        <v-btn fab bottom right color="blue" dark fixed v-on="on">
          <v-icon>add</v-icon>
        </v-btn>
      </template>
      <v-flex xs12>
        <v-card v-if="!validate">
          <v-card-title>
            <span class="headline">Resources</span>
          </v-card-title>
          <v-label v-if="preprocess_resources">{{ preprocess_resources.length }} resources in total</v-label>
          <v-divider />
          <v-card-text>
            <v-flex fluid class="subheading">
              <v-form ref="resource_form">
                <v-textarea
                  ref="resource_list_textarea"
                  v-model="resource_list_model"
                  box
                  rows="1"
                  class="body-1"
                  auto-grow="true"
                  label="Paste or enter resources"
                />
                <v-divider />
              </v-form>
              <v-btn color="primary" @click.stop="validate = true">VALIDATE</v-btn>
            </v-flex>
          </v-card-text>
        </v-card>
        <v-card v-else>
          <v-card-title class="headline">Validated resources</v-card-title>
          <v-divider></v-divider>
          <v-flex v-if="preprocess_resources">
            <v-label>
              Check heuristic detection. You can move back to fix any
              entry or change its type later.
            </v-label>
            <v-divider></v-divider>
          </v-flex>
          <v-flex v-else headline>
            <v-label>No entries yet</v-label>
          </v-flex>
          <v-card-text>
            <v-flex fluid>
              <v-list>
                <v-list-tile v-for="item in preprocess_resources" :key="item.resource">
                  <v-flex>
                    <v-list-tile-avatar>
                      <v-chip :color="item.color" label class="font-weight-bold">{{ item.type }}</v-chip>
                    </v-list-tile-avatar>
                  </v-flex>
                  <v-flex>
                    <v-list-tile-content>{{ item.resource }}</v-list-tile-content>
                  </v-flex>
                </v-list-tile>
              </v-list>
            </v-flex>
            <v-divider></v-divider>
            <v-layout>
              <v-flex>
                <v-btn color="primary" @click.stop="validate = false">BACK</v-btn>
              </v-flex>
              <v-flex v-if="preprocess_resources">
                <v-btn
                  color="green"
                  @click.stop="[validate = false, dialog = false, send()]"
                >Upload {{ preprocess_resources.length }} items</v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-dialog>
  </v-layout>
</template>

<script>
import validator from "validator";
import api_call from "../utils/api";

export default {
  name: "MultipleResourceInput",
  data() {
    return {
      resource_list: null,
      resource_list_model: "",
      validate: false,
      dialog: false
    };
  },
  watch: {
    dialog: {
      handler: function(old_value, new_value) {
        if (this.$refs.resource_form && !new_value) {
          this.$refs.resource_form.reset();
          this.resource_list = [];
        }
        this.validate = false;
      }
    }
  },
  computed: {
    preprocess_resources() {
      if (!this.resource_list_model) return;
      let values = this.resource_list_model.trim().split("\n");
      let classified_resources = [];

      values.forEach(element => {
        let resource_type = this.classify(element);
        classified_resources.push({
          resource: element,
          type: resource_type.type,
          color: resource_type.color
        });
      });

      return classified_resources;
    }
  },
  methods: {
    classify(resource) {
      if (validator.isIP(resource, [4])) {
        return { type: "ip", color: "green" };
      }

      if (validator.isEmail(resource)) {
        return { type: "email", color: "blue" };
      }

      if (
        validator.isURL(resource, {
          protocols: ["http", "https", "hxxp", "ftp"],
          require_valid_protocol: true,
          require_protocol: true
        })
      ) {
        return { type: "url", color: "orange" };
      }

      if (validator.isFQDN(resource)) {
        return { type: "domain", color: "green" };
      }

      if (
        validator.isHash(resource, "md5") ||
        validator.isHash(resource, "sha1") ||
        validator.isHash(resource, "sha256") ||
        validator.isHash(resource, "sha384") ||
        validator.isHash(resource, "sha512")
      ) {
        return { type: "hash", color: "purple" };
      }

      // Default case, treat as a username
      return { type: "username", color: "red" };
    },
    send() {
      this.preprocess_resources.forEach(new_resource => {
        let payload = {
          to_server: {
            url: "/api/create_resource",
            resource_name: new_resource.resource,
            resource_type: new_resource.type
          },
          mutation: "add_resource"
        };
        this.$store.dispatch("resource_action", payload);
      });
    }
  }
};
</script>

<style scoped>
.v-list {
  max-height: 500px;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
