<template>
  <v-layout row>
    <v-flex xs11 sm11 md11>
      <v-text-field
        :value="apikey"
        :label="service"
        :append-icon="show_api ? 'visibility' : 'visibility_off'"
        :type="show_api ? 'text' : 'password'"
        @click:append="show_api = !show_api"
        @input="$emit('input', $event)"
      ></v-text-field>
    </v-flex>
    <v-flex>
      <v-btn icon @click="$emit('remove', service)">
        <v-icon>delete</v-icon>
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: ["service", "apikey", "apikey2"],
  data() {
    return {
      show_api: false
    };
  }
};
</script>
