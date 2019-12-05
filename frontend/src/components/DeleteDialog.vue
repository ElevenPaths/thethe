<template>
  <v-dialog v-model="show" persistent max-width="290">
    <v-card>
      <v-card-title class="headline">{{ title }}</v-card-title>
      <v-card-text>{{ text }}</v-card-text>
      <v-spacer></v-spacer>
      <v-card-actions>
        <v-flex>
          <v-btn color="green darken-1" flat @click.stop="dontdoit"
            >No, dismiss</v-btn
          >
          <v-btn color="red darken-1" flat @click.stop="doit">Yes, do it</v-btn>
        </v-flex>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "delete-dialog",
  props: ["title", "text", "show"],
  methods: {
    dontdoit: function() {
      this.$parent.$emit("dismiss");
    },
    doit: function() {
      this.$parent.$emit("dodelete");
    }
  }
};
</script>
