<template>
  <div class="text-xs-center">
    <v-bottom-sheet v-model="sheet" inset>
      <template v-slot:activator>
        <v-btn flat icon dark>
          <v-progress-circular :size="20" :width="2" indeterminate color="primary"></v-progress-circular>
        </v-btn>
      </template>
      <v-list>
        <v-subheader>Remaining tasks...</v-subheader>
        <v-list-tile v-for="(resource, index) in runningTasks" :key="index">
          <v-list-tile-avatar>
            <v-progress-circular :size="20" :width="2" indeterminate color="primary"></v-progress-circular>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ resource.plugin }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ resource.canonicalName }} - {{ resource.resourceType }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <!-- <v-list-tile-title>Resource: {{ resource.canonicalName }} Plugin: {{ resource.plugin }} Type: {{ resource.resourceType }}</v-list-tile-title> -->
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
    runningTasks: function() {
      return this.$store.state.resourcelist.running;
    }
  }
};
</script>
