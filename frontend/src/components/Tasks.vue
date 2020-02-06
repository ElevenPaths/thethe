<template>
  <div class="text-xs-center">
    <v-bottom-sheet v-model="sheet" inset>
      <template v-slot:activator>
        <v-btn flat icon dark>
          <v-progress-circular
            indeterminate
            color="primary"
          ></v-progress-circular>
        </v-btn>
      </template>
      <v-list>
        <v-subheader>Remaining tasks...</v-subheader>
        <v-list-tile v-for="resource in loadingResources" :key="resource._id">
          <v-list-tile-title
            >Type: {{ resource.resource_type }} Name:
            {{ resource.canonical_name }}</v-list-tile-title
          >
        </v-list-tile>
      </v-list>
    </v-bottom-sheet>
  </div>
</template>

<script>
export default {
  data: () => ({
    sheet: false
  }),
  computed: {
    loadingResources() {
      return this.$store.getters.loadingResources;
    }
  }
};
</script>
