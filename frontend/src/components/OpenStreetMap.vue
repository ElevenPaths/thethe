<template>
  <div id="map"></div>
</template>

<script>
import "leaflet";

export default {
  name: "OpenStreetMap",
  props: { lat: Number, lon: Number },
  data() {
    return {};
  },
  mounted: function() {
    let geoip_map = L.map("map", {
      center: [this.lat, this.lon],
      zoom: 14,
      maxZoom: 14,
      minZoom: 14,
      zoomControl: false,
      dragging: false
    });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(geoip_map);
  }
};
</script>

<style scoped>
.map {
  height: 480px;
  width: 600px;
}
</style>
