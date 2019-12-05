<template>
  <v-layout column>
    <div ref="network" id="network"></div>
  </v-layout>
</template>

<script>
import { Network } from "vis-network";

export default {
  name: "simple-vis-network",
  props: {
    nodes: {
      type: Array,
      default: function() {
        return [
          { id: "0", label: "0" },
          { id: "1", label: "1" },
          { id: "2", label: "2" },
          { id: "3", label: "3" },
          { id: "4", label: "4" }
        ];
      }
    },
    edges: {
      type: Array,
      default: function() {
        return [
          { from: "1", to: "0" },
          { from: "1", to: "2" }
        ];
      }
    }
  },
  data: function() {
    return {
      network: null,
      container: this.$refs.network,
      options: {
        manipulation: {
          enabled: true,
          initiallyActive: true,
          deleteNode: function(deleteData, callback) {
            callback(deleteData);
          }
        },
        edges: { width: 2 },
        nodes: {
          shape: "square",
          size: 30,
          margin: 10,
          font: {
            size: 15,
            color: "#ffffff"
          },
          borderWidth: 2
        },
        interaction: {
          dragNodes: true,
          dragView: true,
          selectable: true,
          zoomView: false
        },
        physics: {
          enabled: true,
          barnesHut: {
            avoidOverlap: 1
          }
        }
      }
    };
  },

  computed: {},

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
    this.network = new Network(this.container, data, this.options);
    setTimeout(() => {
      this.network.fit();
    }, 2000);
  },
  updated() {
    this.network.fit();
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
