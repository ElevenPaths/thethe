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
        <!-- <h3>No remaining tasks now!</h3> -->
        <v-list-tile
          v-for="tile in tiles"
          :key="tile.title"
          @click="sheet = false"
        >
          <v-list-tile-title>{{ tile.title }}</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-bottom-sheet>
  </div>
</template>

<script>
export default {
  data: () => ({
    sheet: false,
    tiles: [
      { img: "keep.png", title: "Keep" },
      { img: "inbox.png", title: "Inbox" },
      { img: "hangouts.png", title: "Hangouts" },
      { img: "messenger.png", title: "Messenger" },
      { img: "google.png", title: "Google+" }
    ]
  })
};
</script>
