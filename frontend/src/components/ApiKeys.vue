<template>
  <v-dialog v-model="show" persistent max-width="760">
    <v-card>
      <v-card-title class="headline">API Keys Management</v-card-title>
      <v-card-text>
        <v-container>
          <div v-if="apikeys.length">
            <api-keys-item
              v-for="apikey in apikeys"
              v-model="apikey.apikey"
              :key="apikey.name"
              :service="apikey.name"
              :apikey="apikey.apikey"
              @remove="removeKey"
              @input="modified = true"
            ></api-keys-item>
          </div>
          <b v-else>No API Keys yet...</b>
          <base-input-service v-show="add" :reset="!add" @add="addKey"></base-input-service>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-flex>
          <v-btn color="green darken-1" flat @click="add = !add">Add</v-btn>
          <v-btn
            color="blue darken-1"
            flat
            :disabled="!modified"
            @click.stop="send_apikeys(), $emit('apikeys-closed')"
          >Save</v-btn>
          <v-btn
            color="red darken-1"
            flat
            @click.stop="
              $emit('apikeys-closed');
              add = false;
            "
          >Close</v-btn>
        </v-flex>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api_call from "../utils/api";
import ApiKeysItem from "./ApiKeysItem.vue";
import BaseInputService from "./BaseInputService.vue";

export default {
  props: { show: Boolean },
  components: {
    ApiKeysItem,
    BaseInputService
  },
  data() {
    return {
      apikeys: [],
      add: false,
      delKeys: [],
      modified: false
    };
  },
  methods: {
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
        this.apikeys = resp.data;
      });
    },
    send_apikeys: function() {
      var params = {
        url: "/api/upload_apikeys",
        entries: this.apikeys
      };

      api_call(params);

      if (this.delKeys.length) {
        var params = {
          url: "/api/remove_apikeys",
          entries: this.delKeys
        };

        api_call(params);

        this.delKeys = [];
      }

      this.modified = false;
    },
    addKey(service, api) {
      this.apikeys.push({
        name: service,
        apikey: api
      });
      this.add = false;
      this.modified = true;
    },
    removeKey(keyToRemove) {
      this.apikeys = this.apikeys.filter(apikey => {
        return apikey.name !== keyToRemove;
      });

      this.delKeys.push({ name: keyToRemove });
      this.modified = true;
    }
  },
  mounted: function() {
    if (this.$store.getters["is_authenticated"]) {
      this.load_keys();
    }
  }
};
</script>
