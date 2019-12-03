<template>
  <component :is="component" :plugin_data="data" v-if="component" />
</template>
<script>
export default {
  name: "dynamic-component",
  props: ["data", "type"],
  data() {
    return {
      component: null
    };
  },
  computed: {
    loader() {
      if (!this.type) {
        return null;
      }
      return () => import(`./templates/${this.type}/index.vue`);
    }
  },
  mounted() {
    this.loader()
      .then(() => {
        this.component = () => this.loader();
      })
      .catch(() => {
        console.log(`Error: template for plugin "${this.type}" not found`);
        //this.component = () => import("./templates/default");
      });
  }
};
</script>