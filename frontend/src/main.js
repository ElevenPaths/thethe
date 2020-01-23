// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import Vuetify from "vuetify";
import Vuelidate from "vuelidate";
import Notifications from "vue-notification";
import CountryFlag from "vue-country-flag";

// Added import for Vuetify
import "vuetify/dist/vuetify.min.css";

// Added material icons
import "@mdi/font/css/materialdesignicons.css";

// Added file icons
import "css-file-icons/build/css-file-icons.css";

import router from "./router";
import store from "./store";
import App from "./App";

Vue.use(Vuetify);
Vue.use(Vuelidate);
Vue.use(Notifications);
Vue.use(CountryFlag);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  store,
  components: { App },
  template: "<App/>"
});
