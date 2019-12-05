<template>
  <v-dialog v-model="show" persistent max-width="760">
    <v-card>
      <v-card-title class="headline">API management</v-card-title>
      <v-divider></v-divider>
      <v-flex pt-2>Add/Change/Delete name,apikey pairs</v-flex>
      <v-flex>
        <v-card-text>
          <v-textarea
            box
            class="body-1"
            rows="18"
            v-model="apikeys"
          ></v-textarea>
        </v-card-text>
      </v-flex>
      <v-spacer></v-spacer>
      <v-divider></v-divider>
      <v-card-actions>
        <v-flex>
          <v-btn
            color="blue darken-1"
            flat
            @click.stop="send_apikeys(), $emit('apikeys-closed')"
            >Upload</v-btn
          >
          <v-btn color="red darken-1" flat @click.stop="$emit('apikeys-closed')"
            >Close</v-btn
          >
        </v-flex>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api_call from "../utils/api";

export default {
  name: "api-keys",
  props: { show: Boolean },
  data() {
    return {
      apikeys: ""
    };
  },

  methods: {
    send_apikeys: function() {
      let apikeys_as_string = this.apikeys.split("\n");
      let entries = [];
      for (let entry of apikeys_as_string) {
        let apikey = entry.trim().split(",");
        if (apikey.length == 2) {
          entries.push({ name: apikey[0], apikey: apikey[1] });
        }
      }

      let params = {
        url: "/api/upload_apikeys",
        entries: entries
      };

      api_call(params);
    },

    apikeys_to_csv: function(apikeys) {
      let csv = "";
      for (let entry of apikeys) {
        csv += `${entry.name},${entry.apikey}\r\n`;
      }
      return csv;
    },

    load_keys: function() {
      let params = {
        url: "/api/get_apikeys"
      };

      api_call(params).then(resp => {
        resp.data.sort((a, b) => {
          if (a.name > b.name) return 1;
          if (b.name > a.name) return -1;
          return 0;
        });
        this.apikeys = this.apikeys_to_csv(resp.data);
      });
    }
  },
  mounted: function() {
    this.load_keys();
  }
};
</script>
