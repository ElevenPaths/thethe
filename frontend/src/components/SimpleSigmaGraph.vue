<template>
  <div ref="network" id="network"></div>
</template>

<script>
import { sigma } from "sigma-webpack";

export default {
  name: "simple-sigma-graph",
  props: {
    grid_space: Number,
    nodes: {
      type: Array,
      default: function() {
        return [
          { id: "0", label: "0", size: 1, color: "#f00" },
          { id: "1", label: "1", size: 1, color: "#f00" },
          { id: "2", label: "2", size: 1, color: "#f00" },
          { id: "3", label: "3", size: 1, color: "#f00" },
          { id: "4", label: "4", size: 1, color: "#f00" }
        ];
      }
    },
    edges: function() {
      return [];
    }
  },
  data: function() {
    return {
      network: null,
      container: ""
    };
  },

  computed: {},
  watch: {
    options: {
      deep: true,
      handler(o) {
        this.network.setOptions(o);
      }
    }
  },

  created: function() {
    this.network = null;
  },

  beforeDestroy: function() {
    this.network.destroy();
  },

  mounted() {
    this.container = this.$refs.network;
    var data = {
      nodes: this.nodes,
      edges: this.edges
    };
    this.network = new sigma("network");
    this.network.graph.addNode({
      id: "0",
      label: "0",
      size: 30,
      color: "#aaa",
      x: Math.Random(),
      y: Math.Random()
    });
    this.network.refresh();
  }
};
</script>

<style>
.vis-network:focus {
  outline: none !important;
  border: 1px !important;
}

#network {
  height: 800px;
  width: 100%;
}
</style>