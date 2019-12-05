<template>
  <v-flex>
    <v-card>
      <v-card>
        <v-card-title class="subheading">Email Reputation</v-card-title>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex>
            <v-label>First seen:</v-label>
            {{ resource.details.first_seen }}
          </v-flex>
          <v-flex>
            <v-label>Last seen:</v-label>
            {{ resource.details.last_seen }}
          </v-flex>
        </v-layout>
        <v-divider></v-divider>

        <v-layout row wrap>
          <v-flex lg3>
            <v-flex>
              <v-label>Reputation</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="reputation()">{{ resource.reputation }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Suspicious</v-label>
            </v-flex>
            <v-flex>
              <v-icon color="red" v-if="resource.suspicious"
                >mdi-emoticon-devil-outline</v-icon
              >
              <v-icon color="green" v-else>mdi-hand-okay</v-icon>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>References</v-label>
            </v-flex>
            <v-flex>
              <v-chip>{{ resource.references }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Blacklisted</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.blacklisted)">{{
                resource.details.blacklisted
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Leaked</v-label>
            </v-flex>
            <v-flex>
              <v-chip
                :color="chip_color(resource.details.credentials_leaked)"
                >{{ resource.details.credentials_leaked }}</v-chip
              >
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Recent leak</v-label>
            </v-flex>
            <v-flex>
              <v-chip
                :color="chip_color(resource.details.credentials_leaked_recent)"
                >{{ resource.details.credentials_leaked_recent }}</v-chip
              >
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Data breach</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.data_breach)">{{
                resource.details.data_breach
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Malicious activity</v-label>
            </v-flex>
            <v-flex>
              <v-chip
                :color="chip_color(resource.details.malicious_activity)"
                >{{ resource.details.malicious_activity }}</v-chip
              >
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Recent MA</v-label>
            </v-flex>
            <v-flex>
              <v-chip
                :color="chip_color(resource.details.malicious_activity_recent)"
                >{{ resource.details.malicious_activity_recent }}</v-chip
              >
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>SPAM</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.spam)">{{
                resource.details.spam
              }}</v-chip>
            </v-flex>
          </v-flex>
        </v-layout>
      </v-card>

      <v-card>
        <v-card-title class="subheading">Domain</v-card-title>
        <v-divider></v-divider>
        <v-layout row wrap>
          <v-flex lg3>
            <v-flex>
              <v-label>Age</v-label>
            </v-flex>
            <v-flex>
              <v-chip>{{ resource.details.days_since_domain_creation }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Disposable mail</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.disposable)">{{
                resource.details.disposable
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Domain exists</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.domain_exists)">{{
                resource.details.domain_exists
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Reputation</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.domain_reputation)">{{
                resource.details.domain_reputation
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Free mail</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.free_provider)">{{
                resource.details.free_provider
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Deliverable</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.deliverable)">{{
                resource.details.deliverable
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>New domain</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.new_domain)">{{
                resource.details.new_domain
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>DMARC</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.dmarc_enforced)">{{
                resource.details.dmarc_enforced
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>SPF Strict</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.spf_strict)">{{
                resource.details.spf_strict
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Spoofable</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.spoofable)">{{
                resource.details.spoofable
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Valid MX</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.valid_mx)">{{
                resource.details.valid_mx
              }}</v-chip>
            </v-flex>
          </v-flex>
          <v-flex lg3>
            <v-flex>
              <v-label>Suspicious TLD</v-label>
            </v-flex>
            <v-flex>
              <v-chip :color="chip_color(resource.details.suspicious_tld)">{{
                resource.details.suspicious_tld
              }}</v-chip>
            </v-flex>
          </v-flex>
        </v-layout>
      </v-card>

      <v-card>
        <v-card-title class="subheading">Profiles</v-card-title>
        <v-divider></v-divider>
        <v-layout row align-content-start>
          <v-flex v-for="site in resource.details.profiles" :key="site">
            <v-chip color="blue">{{ site }}</v-chip>
          </v-flex>
        </v-layout>
      </v-card>
    </v-card>
  </v-flex>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "emailrep",
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
    reputation: function() {
      let level = {
        high: "green",
        medium: "yellow",
        low: "red",
        none: "blue"
      };

      return level[this.resource.reputation];
    },
    chip_color: function(item) {
      if (item) {
        return "green";
      }
      return "red";
    }
  }
};
</script>
