<template>
  <v-flex class="text-xs-left">
    <v-divider></v-divider>
    <v-layout align-center>
      <v-flex lg2>
        <v-label>Discovered mails</v-label>
      </v-flex>
      <v-flex lg2 font-weight-bold>
        <v-chip color="blue">{{ resource.emails.length }}</v-chip>
      </v-flex>
      <v-flex lg1>
        <v-label>Domain</v-label>
      </v-flex>
      <v-flex lg2 font-weight-bold>
        <v-chip color="blue">{{ resource.domain }}</v-chip>
      </v-flex>
      <v-flex lg1>
        <v-label>Disposable</v-label>
      </v-flex>
      <v-flex font-weight-bold>
        <v-chip color="blue">
          <span v-if="resource.disposable">disposable mail</span>
          <span v-else>non disposable mail</span>
        </v-chip>
      </v-flex>
      <v-flex>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn flat color="grey" v-on="on" @click.stop="copy_content">
              <v-icon>file_copy</v-icon>
            </v-btn>
          </template>
          <span>Copy emails to clipboard</span>
        </v-tooltip>
      </v-flex>
    </v-layout>
    <v-divider></v-divider>

    <v-flex>
      <v-expansion-panel>
        <v-expansion-panel-content
          v-for="email in resource.emails"
          :key="email.value"
        >
          <template v-slot:header>
            <v-layout align-center>
              <v-flex subheading lg3>{{ email.value }}</v-flex>
              <v-flex lg1>
                <v-label>Sources</v-label>
              </v-flex>
              <v-flex title lg2>
                <v-chip>{{ email.sources.length }}</v-chip>
              </v-flex>
              <v-flex lg2 subheading>Confidence Score</v-flex>
              <v-flex lg1>
                <v-progress-circular
                  :rotate="360"
                  :size="75"
                  :width="15"
                  :value="email.confidence"
                  :color="confidence_score_color(email.confidence)"
                  >{{ email.confidence }}%</v-progress-circular
                >
              </v-flex>
              <v-flex lg1 subheading>
                <v-layout column>
                  <v-flex v-if="email.linkedin">
                    <v-icon color="blue">mdi-linkedin-box</v-icon>
                    <a
                      rel="noopener noreferer"
                      target="_blank"
                      :href="`https://linkedin.com/in/${email.linkedin}`"
                      >{{ email.linkedin }}</a
                    >
                  </v-flex>
                  <v-flex v-if="email.twitter">
                    <v-icon color="blue lighten-2">mdi-twitter</v-icon>
                    <a
                      rel="noopener noreferer"
                      target="_blank"
                      :href="`https://twitter.com/${email.twitter}`"
                      >{{ email.twitter }}</a
                    >
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </template>
          <v-divider></v-divider>
          <v-card>
            <v-card-text>
              <v-flex v-for="(source, index) in email.sources" :key="index">
                <v-flex>
                  <v-layout>
                    <v-flex lg1>
                      <v-label>Domain</v-label>
                    </v-flex>
                    <v-flex lg3>{{ source.domain }}</v-flex>
                    <v-flex lg2>
                      <v-label>Still on page</v-label>
                    </v-flex>
                    <v-flex lg2>
                      <v-label>Extracted on</v-label>
                    </v-flex>
                    <v-flex lg2>
                      <v-label>Last seen</v-label>
                    </v-flex>
                  </v-layout>
                  <v-layout justify-center>
                    <v-flex offset-lg2 lg2>
                      <v-chip>{{ source.still_on_page }}</v-chip>
                    </v-flex>
                    <v-flex lg2>
                      <v-chip>{{ source.extracted_on }}</v-chip>
                    </v-flex>
                    <v-flex lg2>
                      <v-chip>{{ source.last_seen_on }}</v-chip>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex>
                  <v-layout>
                    <v-flex lg1>
                      <v-label>URI</v-label>
                    </v-flex>
                    <v-flex>
                      <a
                        rel="noopener noreferer"
                        target="_blank"
                        :href="source.uri"
                        >{{ source.uri }}</a
                      >
                    </v-flex>
                  </v-layout>
                </v-flex>

                <v-divider></v-divider>
              </v-flex>
            </v-card-text>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-flex>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "hunterio",
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
    confidence_score_color: function(score) {
      if (score < 33) {
        return "red";
      } else if (score >= 33 && score <= 66) {
        return "yellow";
      } else if (score > 66) {
        return "green";
      }

      return "blue";
    },
    copy_content: async function() {
      let emails = this.resource.emails.map(elem => elem.value);
      await navigator.clipboard.writeText(emails);
    }
  }
};
</script>
