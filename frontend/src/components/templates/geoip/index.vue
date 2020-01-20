<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex lg5>
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Geolocalization</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-layout row>
              <v-flex lg-6 class="text-xs-left">
                <v-layout column>
                  <v-flex>
                    <v-label>Continent:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Country:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Region:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>City:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Zip:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Latitude:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Longitude:</v-label>
                  </v-flex>
                  <v-flex v-if="resource.country_code">
                    <v-label>Flag:</v-label>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex lg-6 class="text-xs-right">
                <v-layout column>
                  <v-flex>{{ resource.continent_name }}</v-flex>
                  <v-flex>{{ resource.country_name }}</v-flex>
                  <v-flex>{{ resource.region_name }}</v-flex>
                  <v-flex>{{ resource.city }}</v-flex>
                  <v-flex>{{ resource.zip }}</v-flex>
                  <v-flex>{{ resource.latitude }}</v-flex>
                  <v-flex>{{ resource.longitude }}</v-flex>
                  <v-flex v-if="resource.country_code">
                    <country-flag :country="resource.country_code"></country-flag>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>

    <v-flex>
      <v-card>
        <v-card-title primary-title>
          <span class="subheading">OpenStreetMap</span>
        </v-card-title>
        <v-divider></v-divider>
        <l-map :zoom="zoom" :center="center" :options="mapOptions" style="height: 360px; z-index: 0;">
          <l-tile-layer :url="url" :attribution="attribution" />
          <l-marker :lat-lng="withPopup"></l-marker>
        </l-map>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";

export default {
  name: "geoip",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  props: {
    plugin_data: Object
  },
  data: function() {
    return {
      zoom: 14,
      center: latLng(
        this.plugin_data.results.latitude,
        this.plugin_data.results.longitude
      ),
      url: "https://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
      withPopup: latLng(
        this.plugin_data.results.latitude,
        this.plugin_data.results.longitude
      ),
      currentZoom: 11.5,
      currentCenter: latLng(
        this.plugin_data.results.latitude,
        this.plugin_data.results.longitude
      ),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5
      }
    };
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_data.results };
      return plugin_result;
    }
  }
};
</script>
