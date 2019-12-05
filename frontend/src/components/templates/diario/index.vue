<template>
  <v-flex class="text-xs-left">
    <v-divider></v-divider>
    <v-layout row pt-2 wrap class="subheading">
      <v-flex v-if="!resource.is_document">
        <v-layout row align-start pa-2>
          <v-flex>This hash is not in DIARIO databases</v-flex>
        </v-layout>
      </v-flex>

      <v-flex v-else>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.document_type" lg2>
            <v-label>Document type:</v-label>
          </v-flex>
          <v-flex v-if="resource.document_type === 'pdf'" lg1>
            <v-icon color="red">mdi-pdf-box</v-icon>
          </v-flex>
          <v-flex v-if="resource.document_type === 'word'" lg1>
            <v-icon color="blue">mdi-file-word-box</v-icon>
          </v-flex>
          <v-flex v-if="resource.document_type === 'excel'" lg1>
            <v-icon color="green">mdi-file-excel-box</v-icon>
          </v-flex>
          <v-flex v-if="resource.document_type" lg2>{{
            resource.document_type
          }}</v-flex>
        </v-layout>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.prediction" lg2>
            <v-label>Prediction:</v-label>
          </v-flex>
          <v-flex v-if="resource.prediction === 'Goodware'" lg1>
            <v-icon color="green">thumb_up_alt</v-icon>
          </v-flex>
          <v-flex v-if="resource.prediction === 'Malware'" lg1>
            <v-icon color="red">thumb_down_alt</v-icon>
          </v-flex>
          <v-flex v-if="resource.prediction" lg2>{{
            resource.prediction
          }}</v-flex>
        </v-layout>
        <v-layout row align-start pa-2>
          <v-flex v-if="resource.status" lg2>
            <v-label>Status:</v-label>
          </v-flex>

          <v-flex v-if="resource.status === 'Analyzed'" lg1>
            <v-icon color="blue">thumb_up_alt</v-icon>
          </v-flex>
          <v-flex v-if="resource.status === 'Processing'" lg1>
            <v-icon color="yellow">scheduled</v-icon>
          </v-flex>
          <v-flex v-if="resource.status === 'Failed'" lg1>
            <v-icon color="red">sentiment_very_dissatisfied</v-icon>
          </v-flex>
          <v-flex>{{ resource.status }}</v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
    <v-divider v-if="resource.sub_documents"></v-divider>
    <v-flex v-if="resource.sub_documents" subheading
      >Number of macros/javascript {{ resource.sub_documents.length }}</v-flex
    >
    <v-flex>
      <v-layout column>
        <v-card
          v-for="(document, index) in resource.sub_documents"
          :key="index"
        >
          <v-expansion-panel>
            <v-expansion-panel-content>
              <template v-slot:header>
                <v-card-title>
                  <v-flex lg8>{{ document.hash }}</v-flex>
                  <v-flex>
                    <v-chip>{{ document.code.length }}</v-chip>
                    <span>bytes</span>
                  </v-flex>
                </v-card-title>
              </template>
              <v-card-text>
                <v-flex>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                      <v-divider></v-divider>
                      <v-btn
                        flat
                        color="grey"
                        v-on="on"
                        @click.stop="copy_content(index)"
                      >
                        <v-icon>file_copy</v-icon>
                      </v-btn>
                    </template>
                    <span>Copy to clipboard</span>
                  </v-tooltip>
                </v-flex>
                <v-textarea
                  v-model="document.code"
                  readonly
                  box
                  rows="32"
                  class="body-1"
                  :ref="`document_code_${index}`"
                ></v-textarea>
              </v-card-text>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-card>
      </v-layout>
    </v-flex>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "diario",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };
      return plugin_result;
    }
  },
  methods: {
    copy_content: async function(index) {
      await navigator.clipboard.writeText(
        this.$refs[`document_code_${index}`][0].value
      );
    }
  }
};
</script>
