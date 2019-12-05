<template>
  <v-flex>
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn flat color="grey" v-on="on" @click.stop="copy_content">
          <v-icon>file_copy</v-icon>
        </v-btn>
      </template>
      <span>Copy to clipboard</span>
    </v-tooltip>
    <v-textarea
      v-model="textarea_value"
      readonly
      box
      rows="32"
      class="body-1"
      ref="paste_content"
    ></v-textarea>
  </v-flex>
</template>

<script>
import api_call from "../utils/api";

export default {
  name: "paste-viewer",
  props: { paste_id: String },
  data() {
    return { textarea_value: "" };
  },
  methods: {
    copy_content: async function() {
      await navigator.clipboard.writeText(this.textarea_value);
    }
  },
  mounted: function() {
    let params = { url: "/api/load_paste", paste_id: this.paste_id };
    api_call(params)
      .then(resp => {
        this.textarea_value = resp.data;
      })
      .catch(resp => console.log("error loading paste:" + resp));
  }
};
</script>
