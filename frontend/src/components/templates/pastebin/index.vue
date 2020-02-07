<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex lg12>
      <v-flex>
        <v-card v-if="resource.results">
          <v-card-title primary-title>
            <span class="subheading">
              Pastes
              <v-chip>{{ resource.results.length }}</v-chip>
            </span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-card v-for="(paste, index) in resource.results" :key="index">
              <v-card-title v-if="paste.title" class="font-weight-bold">
                {{
                paste.title
                }}
              </v-card-title>
              <v-card-title v-else class="grey--text">Untitled paste</v-card-title>
              <v-divider></v-divider>
              <v-card-text class="pt-2">
                <v-layout class="text-sm-left">
                  <v-flex lg2>
                    <v-label>User:&nbsp;</v-label>
                    <span v-if="paste.user">{{ paste.user }}</span>
                    <span v-else class="grey--text">No user</span>
                  </v-flex>
                  <v-flex v-if="paste.date" lg4>
                    <v-label>Paste date:&nbsp;</v-label>
                    {{ from_python_time(paste.date) }}
                  </v-flex>
                  <v-flex v-if="paste.hits" lg3>
                    <v-label>Paste hits:</v-label>
                    {{ paste.hits }}
                  </v-flex>
                </v-layout>
              </v-card-text>
              <v-card-text class="pt-2">
                <v-layout class="text-sm-left">
                  <v-flex v-if="paste.syntax" lg2>
                    <v-label>Syntax:</v-label>
                    {{ paste.syntax }}
                  </v-flex>
                  <v-flex v-if="paste.size" lg4>
                    <v-label>Size:</v-label>
                    {{ paste.size }} bytes
                  </v-flex>
                  <v-flex v-if="paste.md5" lg4>
                    <v-label>MD5:</v-label>
                    {{ paste.md5 }}
                  </v-flex>
                </v-layout>
              </v-card-text>
              <v-card-text class="pt-2">
                <v-layout class="text-sm-left">
                  <v-flex lg4>
                    <v-label>Link:&nbsp;</v-label>
                    <span class="font-weight-thin">
                      <a
                        target="blank"
                        rel="noopener noreferer"
                        :href="get_paste_link(paste.paste_key)"
                      >{{ get_paste_link(paste.paste_key) }}</a>
                    </span>
                  </v-flex>
                  <v-flex v-if="paste.expire" lg3>
                    <v-label>Expire:&nbsp;</v-label>
                    <span v-if="paste.expire != 0">{{ paste.expire }}</span>
                    <span v-else>Never</span>
                  </v-flex>
                </v-layout>
              </v-card-text>

              <v-expansion-panel>
                <v-expansion-panel-content>
                  <template v-slot:header>
                    <v-label>Saved copy (toggle to view)</v-label>
                  </template>
                  <v-card>
                    <paste-viewer :paste_id="paste._id"></paste-viewer>
                  </v-card>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-card>
            <v-divider></v-divider>
          </v-card-text>
        </v-card>
        <v-card v-else>
          <v-flex>No results</v-flex>
        </v-card>
      </v-flex>
    </v-flex>
  </v-layout>
</template>

<script>
import PasteViewer from "../../PasteViewer";
import { make_unique_list, from_python_time } from "../../../utils/utils";

export default {
  name: "pastebin",

  components: {
    PasteViewer
  },

  props: {
    plugin_data: Object
  },

  data: function() {
    return {};
  },

  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data };
      return plugin_result;
    }
  },

  methods: {
    get_paste_link: function(pastekey) {
      return "https://pastebin.com/raw/" + pastekey;
    },

    a2b: function(b_string) {
      return atob(b_string);
    },

    from_python_time: from_python_time
  }
};
</script>
