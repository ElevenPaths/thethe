<template>
  <v-flex>
    <v-expansion-panel accordion>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">General</span>
        </template>
        <v-flex offset-lg1 class="scrollable">
          <v-layout column>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">SHA1:</v-flex>
              <v-flex>{{ resource.hashPath }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">SHA256:</v-flex>
              <v-flex>{{ resource.sha256 }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">MD5:</v-flex>
              <v-flex>{{ resource.md5 }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Title:</v-flex>
              <v-flex>{{ resource.title }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Platform:</v-flex>
              <v-flex>{{ resource.platform }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Origin:</v-flex>
              <v-flex>{{ resource.origin }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Category:</v-flex>
              <v-flex>{{ resource.categoryName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Size:</v-flex>
              <v-flex>{{ resource.size }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Market Size:</v-flex>
              <v-flex>{{ resource.marketSize }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Downloads:</v-flex>
              <v-flex>{{ resource.numDownloads }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Version Code:</v-flex>
              <v-flex>{{ resource.versionCode }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Package Name:</v-flex>
              <v-flex>{{ resource.packageName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Price:</v-flex>
              <v-flex>{{ resource.price }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Version String:</v-flex>
              <v-flex>{{ resource.versionString }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Minimun SDK Version:</v-flex>
              <v-flex>{{ resource.minSdkVersion }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Target SDK Version:</v-flex>
              <v-flex>{{ resource.targetSdkVersion }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Files:</v-flex>
              <v-flex>{{ resource.nFiles }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Images:</v-flex>
              <v-flex>{{ resource.nImages }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of API Keys:</v-flex>
              <v-flex>{{ resource.nMetadataApiKeys }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Activities:</v-flex>
              <v-flex>{{ resource.nActivities }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Activity Alias:</v-flex>
              <v-flex>{{ resource.nActivityAlias }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Services:</v-flex>
              <v-flex>{{ resource.nServices }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Receivers:</v-flex>
              <v-flex>{{ resource.nReceivers }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Providers:</v-flex>
              <v-flex>{{ resource.nProviders }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of AdNetworks:</v-flex>
              <v-flex>{{ resource.nAdNetworks }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Class Names:</v-flex>
              <v-flex>{{ resource.nClassNames }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Method Names:</v-flex>
              <v-flex>{{ resource.nMethodNames }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Domains:</v-flex>
              <v-flex>{{ resource.nDomains }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Developer Domains:</v-flex>
              <v-flex>{{ resource.nDeveloperDomains }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of Email Domains:</v-flex>
              <v-flex>{{ resource.nEmailDomains }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Number of URI Domains:</v-flex>
              <v-flex>{{ resource.nURIDomains }}</v-flex>
            </v-layout>
          </v-layout>
        </v-flex>
      </v-expansion-panel-content>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">Certificate</span>
        </template>
        <v-flex offset-lg1 class="scrollable">
          <v-layout column>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Fingerprint:</v-flex>
              <v-flex>{{ resource.certificateFingerprint }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Issuer Common Name:</v-flex>
              <v-flex>{{ resource.certificateIssuerCommonName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Issuer State:</v-flex>
              <v-flex>{{ resource.certificateIssuerState }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Issuer Locality:</v-flex>
              <v-flex>{{ resource.certificateIssuerLocality }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Issuer Organization Name:</v-flex>
              <v-flex>{{ resource.certificateIssuerOrganizationName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Issuer Organization Unit Name:</v-flex>
              <v-flex>
                {{
                resource.certificateIssuerOrganizationUnitName
                }}
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Subject Common Name:</v-flex>
              <v-flex>{{ resource.certificateSubjectCommonName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Subject Country Name:</v-flex>
              <v-flex>{{ resource.certificateSubjectCountryName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Subject State:</v-flex>
              <v-flex>{{ resource.certificateSubjectState }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Subject Locality:</v-flex>
              <v-flex>{{ resource.certificateSubjectLocality }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Subject Organization Name:</v-flex>
              <v-flex>{{ resource.certificateSubjectOrganizationName }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Subject Organization Unit Name:</v-flex>
              <v-flex>
                {{
                resource.certificateSubjectOrganizationUnitName
                }}
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Public Key:</v-flex>
              <v-flex>
                <v-textarea no-resize rows="4" :value="resource.certificatePublicKey" solo readonly></v-textarea>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Public Key Info:</v-flex>
              <v-flex>{{ resource.certificatePublicKeyInfo }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Signature Algorithm:</v-flex>
              <v-flex>{{ resource.certificateSignatureAlgorithm }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">AutoSigned:</v-flex>
              <v-flex>{{ resource.certificateAutoSigned }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Serial Number:</v-flex>
              <v-flex>{{ resource.certificateSerialNumber }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Validity Gap Seconds:</v-flex>
              <v-flex>{{ resource.certificateValidityGapSeconds }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Validity Gap Rounded Years:</v-flex>
              <v-flex>{{ resource.certificateValidityGapRoundedYears }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Valid From:</v-flex>
              <v-flex>{{ resource.certificateValidFrom }}</v-flex>
            </v-layout>
            <v-layout>
              <v-flex lg4 class="font-weight-bold subtitle-1">Valid To:</v-flex>
              <v-flex>{{ resource.certificateValidTo }}</v-flex>
            </v-layout>
          </v-layout>
        </v-flex>
      </v-expansion-panel-content>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">Permissions</span>
        </template>
        <v-flex offset-lg1 class="scrollable">
          <v-flex
            class="subtitle-1"
            v-for="premission in resource.permissionName"
            :key="premission"
          >{{ premission }}</v-flex>
        </v-flex>
      </v-expansion-panel-content>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">Links</span>
        </template>
        <v-flex offset-lg1 class="scrollable">
          <v-flex class="subtitle-1" v-for="link in resource.links" :key="link">
            <a v-bind:href="link">{{ link }}</a>
          </v-flex>
        </v-flex>
      </v-expansion-panel-content>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">Email Domains</span>
        </template>
        <v-flex offset-lg1 class="scrollable">
          <v-flex class="subtitle-1" v-for="email in resource.emailDomains" :key="email">{{ email }}</v-flex>
        </v-flex>
      </v-expansion-panel-content>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">URI Domains</span>
        </template>
        <v-flex offset-lg1 class="scrollable">
          <v-flex class="subtitle-1" v-for="uri in resource.URIDomains" :key="uri">
            <a v-bind:href="uri">{{ uri }}</a>
          </v-flex>
        </v-flex>
      </v-expansion-panel-content>
      <v-expansion-panel-content>
        <template v-slot:header>
          <span class="title">Manifest</span>
        </template>
        <v-flex offset-lg1>
          <v-layout>
            <v-flex lg4 class="font-weight-bold subtitle-1">Header Built By:</v-flex>
            <v-flex>{{ resource.manifestHeaderBuiltBy }}</v-flex>
          </v-layout>
          <v-layout>
            <v-flex lg4 class="font-weight-bold subtitle-1">Header Version:</v-flex>
            <v-flex>{{ resource.manifestHeaderVersion }}</v-flex>
          </v-layout>
          <v-layout>
            <v-flex lg4 class="font-weight-bold subtitle-1">Header Created By:</v-flex>
            <v-flex>{{ resource.manifestHeaderCreatedBy }}</v-flex>
          </v-layout>
        </v-flex>
        <v-flex class="scrollable">
          <pre pre class="prettyprint"><code class="language-xml">{{code}}</code></pre>
        </v-flex>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-flex>
</template>
<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "tacyt",
  props: {
    plugin_data: Object
  },
  data: function() {
    return {
      code: this.formatXml(this.plugin_data.results.androidXMLManifest)
    };
  },
  computed: {
    resource: function() {
      let run_prettify = document.createElement("script");
      run_prettify.setAttribute(
        "src",
        "https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"
      );
      run_prettify.async = true;
      document.head.appendChild(run_prettify);
      let plugin_result = { ...this.plugin_data.results };
      //TODO: cambiar return por plugin_result cuando este listo el backend
      return plugin_result;
    }
  },
  created() {
    PR.prettyPrint();
  },
  methods: {
    copy_content: async function(index) {
      await navigator.clipboard.writeText(
        this.$refs[`document_code_${index}`][0].value
      );
    },

    formatXml: (this.formatXml = function(xml) {
      var reg = /(>)\s*(<)(\/*)/g; // updated Mar 30, 2015
      var wsexp = / *(.*) +\n/g;
      var contexp = /(<.+>)(.+\n)/g;
      xml = xml
        .replace(reg, "$1\n$2$3")
        .replace(wsexp, "$1\n")
        .replace(contexp, "$1\n$2");
      var pad = 0;
      var formatted = "";
      var lines = xml.split("\n");
      var indent = 0;
      var lastType = "other";
      // 4 types of tags - single, closing, opening, other (text, doctype, comment) - 4*4 = 16 transitions
      var transitions = {
        "single->single": 0,
        "single->closing": -1,
        "single->opening": 0,
        "single->other": 0,
        "closing->single": 0,
        "closing->closing": -1,
        "closing->opening": 0,
        "closing->other": 0,
        "opening->single": 1,
        "opening->closing": 0,
        "opening->opening": 1,
        "opening->other": 1,
        "other->single": 0,
        "other->closing": -1,
        "other->opening": 0,
        "other->other": 0
      };

      for (var i = 0; i < lines.length; i++) {
        var ln = lines[i];

        // Luca Viggiani 2017-07-03: handle optional <?xml ... ?> declaration
        if (ln.match(/\s*<\?xml/)) {
          formatted += ln + "\n";
          continue;
        }
        // ---

        var single = Boolean(ln.match(/<.+\/>/)); // is this line a single tag? ex. <br />
        var closing = Boolean(ln.match(/<\/.+>/)); // is this a closing tag? ex. </a>
        var opening = Boolean(ln.match(/<[^!].*>/)); // is this even a tag (that's not <!something>)
        var type = single
          ? "single"
          : closing
          ? "closing"
          : opening
          ? "opening"
          : "other";
        var fromTo = lastType + "->" + type;
        lastType = type;
        var padding = "";

        indent += transitions[fromTo];
        for (var j = 0; j < indent; j++) {
          padding += "\t";
        }
        if (fromTo == "opening->closing")
          formatted = formatted.substr(0, formatted.length - 1) + ln + "\n";
        // substr removes line break (\n) from prev loop
        else formatted += padding + ln + "\n";
      }

      return formatted;
    })
  }
};
</script>

<style scoped>
.scrollable {
  max-height: 30rem;
  overflow-y: scroll;
  overflow-x: hidden;
}
body {
  width: 200px;
  margin: 0 auto;
}

::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(201, 201, 201, 1);
  box-shadow: inset 0 0 6px rgba(201, 201, 201, 1);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(201, 201, 201, 1);
  box-shadow: inset 0 0 6px rgba(201, 201, 201, 1);
}
.v-expansion-panel__container {
  box-shadow: inset 0 0 6px rgba(201, 201, 201, 1);
  border-radius: 5px;
  margin-bottom: 0.5rem;
}
a {
  text-decoration: none;
  color: #fff;
}
a:hover {
  font-weight: bold;
}
</style>
