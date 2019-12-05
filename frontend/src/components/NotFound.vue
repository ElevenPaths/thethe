<template>
  <v-app id="notfound" :dark="true">
    <h1 class="subheading grey--text">Dashboard</h1>
    <v-container>
      <v-layout row wrap justify-space-around>
        <v-flex xs12 md6 lg12>
          <v-btn outline block class="primary">ONE</v-btn>
        </v-flex>
        <v-flex xs4 md2>
          <v-btn outline block class="primary">TWO</v-btn>
        </v-flex>
        <v-flex xs4 md2>
          <v-btn outline block class="primary">THREE</v-btn>
        </v-flex>
        <v-flex xs4 md2>
          <v-btn outline block class="primary">FOUR</v-btn>
        </v-flex>
      </v-layout>
      <v-layout row wrap justify-space-around>
        <v-flex xs4 md3>
          <v-btn outline block class="success">FIVE</v-btn>
        </v-flex>
        <v-flex xs4 md3>
          <v-btn outline block class="success">SIX</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container>
      <v-layout pa-2>
        <v-flex text-lg-left>A</v-flex>
        <v-flex text-xs-right>B</v-flex>
        <v-flex>C</v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>
