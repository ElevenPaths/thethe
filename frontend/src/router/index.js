import Vue from "vue";
import Router from "vue-router";

const routerOptions = [
  { path: "/", component: "Root" },
  { path: "/login", component: "Login" },
  { path: "*", component: "Root" }
];

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  };
});

Vue.use(Router);

let router = new Router({
  routes,
  mode: "history"
});

export default router;
