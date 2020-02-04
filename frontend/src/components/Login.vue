<template>
  <v-app id="login" :dark="true">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-card class="elevation-12">
            <v-toolbar color="grey darken-3" dark flat>
              <v-spacer>
                <v-toolbar-title>The Threat Hunting Environment</v-toolbar-title>
              </v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form class="login" @submit.prevent="login" id="login-form">
                <v-text-field
                  label="Login"
                  name="login"
                  prepend-icon="person"
                  type="text"
                  v-model="username"
                  autocomplete="off"
                ></v-text-field>
                <v-text-field
                  id="password"
                  label="Password"
                  name="password"
                  prepend-icon="lock"
                  type="password"
                  v-model="password"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn type="submit" color="primary" form="login-form">Login</v-btn>
            </v-card-actions>
            <template v-if="auth_status === 'error'">
              <v-alert
                type="error"
                dismissible
                :value="true"
              >User does not exist or Password is wrong</v-alert>
            </template>
          </v-card>
        </v-layout>
        <status-bar></status-bar>
        <!-- <img src="../../static/images/logo_lab_11paths.png" height="64" /> -->
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import StatusBar from "./StatusBar";

import { AUTH_REQUEST } from "../store/actions/auth";
import { mapGetters } from "vuex";

export default {
  components: {
    StatusBar
  },
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    login: function() {
      const { username, password } = this;
      this.$store
        .dispatch(AUTH_REQUEST, { username, password })
        .then(() => {
          this.$router.push("/");
        })
        .catch(err => console.log(err.data.error_message));
    }
  },
  computed: {
    ...mapGetters({ auth_status: "auth_status" })
  },

  beforeMount: function() {
    if (this.$store.getters["is_authenticated"]) {
      this.$router.push("/");
    }
  }
};
</script>
