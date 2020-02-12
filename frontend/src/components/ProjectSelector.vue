<template>
  <v-layout fluid wrap>
    <v-flex offset-lg4 lg4 pt-5>
      <v-card
        v-on:dismiss="delete_dialog = !delete_dialog"
        v-on:dodelete="delete_project_with_confirmation"
      >
        <v-card-title>
          <v-card-text>
            <p class="headline blue--text text--lighten-2 text-xs-center">Project selection</p>
          </v-card-text>
        </v-card-title>
        <v-data-table v-if="true" :headers="headers" :items="projects">
          <template v-slot:items="props">
            <tr
              :class="{ selected: selected_project._id === props.item._id }"
              @click.stop="select_project(props.item)"
            >
              <td
                class="text-xs-left subheading"
                v-on:dblclick="open_project()"
              >{{ props.item.name }}</td>
              <td
                class="text-xs-left subheading"
              >{{ new Date(props.item.creation_date * 1000).toDateString() }}</td>
            </tr>
          </template>
        </v-data-table>
        <v-card-text v-else>
          <p class="title pa-2">There are no projects yet</p>
        </v-card-text>
        <delete-dialog
          title="Delete Project?"
          text="This project and all its references will be deleted. Are you sure?"
          :show="delete_dialog"
        ></delete-dialog>
      </v-card>
      <v-flex v-if="!user_is_creating_project">
        <v-btn
          class="font-weight-bold"
          small
          color="success"
          @click="user_is_creating_project = !user_is_creating_project"
        >New</v-btn>
        <v-btn
          class="font-weight-bold"
          :disabled="!is_project_selected"
          small
          color="primary"
          @click="open_project"
        >Open</v-btn>
        <v-btn
          class="font-weight-bold"
          :disabled="!is_project_selected"
          small
          color="error"
          @click="delete_dialog = true"
        >Delete</v-btn>
      </v-flex>
      <v-flex v-else>
        <v-form ref="new_project_form">
          <v-container>
            <v-layout row wrap>
              <v-text-field
                label="project name"
                required
                class="pt-0"
                v-model.trim="new_project_name"
              ></v-text-field>
              <v-flex>
                <v-btn class="font-weight-bold" small color="success" @click="create_project">Add</v-btn>
                <v-btn
                  class="font-weight-bold"
                  small
                  color="warning"
                  @click="user_is_creating_project = !user_is_creating_project"
                >Cancel</v-btn>
              </v-flex>
            </v-layout>
          </v-container>
        </v-form>
      </v-flex>
    </v-flex>
  </v-layout>
</template>

<script>
import api_call from "../utils/api";
import { object_is_empty } from "../utils/utils";
import { SET_PROJECT } from "../store/actions/project";

import {
  required,
  minLength,
  maxLength,
  alphaNum
} from "vuelidate/lib/validators";

import DeleteDialog from "./DeleteDialog";

export default {
  components: {
    DeleteDialog
  },
  name: "ProjectSelector",
  data() {
    return {
      headers: [
        { text: "Project Name", value: "name", align: "left" },
        { text: "Creation date", value: "creation_date" }
        //{ text: "Tags", value: "tags", sortable: false }
      ],
      projects: [],
      selected_project: {},
      user_is_creating_project: false,
      new_project_name: "",
      delete_dialog: false,
      active_project: ""
    };
  },
  methods: {
    open_project: function() {
      // Check if a project is open
      // Set selected_project in Vuex
      // Call to set_active_project to let it know to the server
      if (!object_is_empty(this.selected_project)) {
        const { selected_project } = this;
        this.$store.dispatch(SET_PROJECT, selected_project);
        this.set_active_project();
      }
    },

    get_active_project: function() {
      api_call({ url: "/api/get_active_project" })
        .then(resp => {
          if (resp.data.project_id) {
            this.active_project = resp.data.project_id;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },

    set_active_project: function() {
      // Call to server to let it know we've got an active project
      api_call({
        url: "/api/set_active_project",
        project_id: this.selected_project._id
      }).catch(err => {
        this.$notify({
          title: "Error",
          text: err.response.data.error_message,
          type: "error"
        });
      });
    },

    create_project: function() {
      let project_name = this.new_project_name;
      api_call({ url: "/api/new_project", name: project_name })
        .then(resp => {
          this.$notify({
            title: "Info",
            text: resp.data.success_message
          });
          this.get_projects();
        })
        .catch(err => {
          this.$notify({
            title: "Error",
            text: err.response.data.error_message,
            type: "error"
          });
        })
        .finally(_ => {
          this.$refs.new_project_form.reset();
          this.user_is_creating_project = false;
        });
    },

    get_projects: function() {
      api_call({ url: "/api/get_projects" })
        .then(resp => {
          this.projects = resp.data;
          this.$notify({
            title: "Info",
            text: `Loaded ${resp.data.length} projects`
          });
        })
        .catch(err => {
          console.log(err);
        });
    },

    select_project: function(project) {
      this.user_is_creating_project = false;
      if (project._id === this.selected_project._id) {
        this.selected_project = {};
      } else {
        this.selected_project = project;
      }
    },

    delete_project_with_confirmation: function() {
      this.delete_dialog = false;
      if (!object_is_empty(this.selected_project)) {
        api_call({
          url: "/api/delete_project",
          project_id: this.selected_project._id
        })
          .then(resp => {
            this.get_projects();
            this.selected_project = {};
            this.$notify({
              title: "Info",
              text: resp.data.success_message
            });
          })
          .catch(err => {
            this.$notify({
              title: "Error",
              text: err.response.data.error_message,
              type: "error"
            });
          });
      }
    }
  },
  computed: {
    is_project_selected: function() {
      // Used to know if a project has been selected just to activate 'open' button
      return !object_is_empty(this.selected_project);
    }
  },
  validations: {
    new_project_name: {
      required,
      alphaNum,
      minLength: minLength(6),
      maxLength: maxLength(64)
    }
  },
  mounted: async function() {
    // Load projects when the component is drawn for the first time
    if (this.$store.getters["is_authenticated"]) {
      await this.get_projects();
      await this.get_active_project();
    }
  }
};
</script>
