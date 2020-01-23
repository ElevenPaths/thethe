<template>
  <v-dialog v-model="dialog" width="600">
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" fab bottom right color="red" dark fixed>
        <v-icon>add</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-container>
        <v-flex fluid offset-xs1 xs10>
          <v-form @submit.prevent="submit_button" ref="resource_form">
            <v-text-field
              v-model="resource"
              placeholder="Enter IP, Domain, URL, Email or Hash"
              clearable
              single-line
              outline
              ref="resource_text_field"
              v-on:keydown="hola"
            ></v-text-field>
            <v-divider></v-divider>
            <v-flex>
              <v-radio-group v-model="radio_group">
                <v-radio
                  v-for="n in resource_type_list"
                  :key="n"
                  :label="`${n}`"
                  :value="n"
                ></v-radio>
              </v-radio-group>
            </v-flex>
          </v-form>
          <v-btn color="primary" @click.prevent="submit_button">SUBMIT</v-btn>
        </v-flex>
        <v-flex v-if="prevent_send">
          <v-alert type="error" dismissible :value="true"
            >You have to put a resource and select a resource type</v-alert
          >
        </v-flex>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "ResourceInput",
  data() {
    return {
      dialog: false,
      prevent_send: false,
      resource: "",
      resource_type: "",
      resource_type_list: ["IP", "Domain", "Hash", "URL", "Username", "Email"],
      radio_group: 1
    };
  },
  methods: {
    submit_button() {
      if (this.resource == "" || this.radio_group == 1) {
        this.prevent_send = true;
        return;
      }
      let payload = {
        to_server: {
          url: "/api/create_resource",
          resource_name: this.resource,
          resource_type: this.radio_group
        },
        mutation: "add_resource"
      };
      this.$store.dispatch("resource_action", payload);
      this.$refs.resource_form.reset();
      this.dialog = false;
      this.prevent_send = false;
    },
    hola() {
      console.log("holaaa");
    }
  }
};
</script>
