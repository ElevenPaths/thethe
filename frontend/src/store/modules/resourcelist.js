import Vue from "vue";
import Vuex from "vuex";

import api_call from "../../utils/api";

Vue.use(Vuex);

const state = {
  resources: []
};

const actions = {
  get_resources: async function({ commit, getters }) {
    let url = "/api/get_resources2";
    let project_id = getters.get_opened_project._id;

    await api_call({ url: url, project_id: project_id })
      .then(resp => {
        commit("set_resources", resp.data);
      })
      .catch(err => console.log(err));
  },

  add_new_resource: async function({ commit }, payload) {
    let url = "/api/create_resource";
    await api_call({
      url: url,
      resource_name: payload.resource_name,
      resource_type: payload.resource_type
    })
      .then(resp => {
        commit("set_resources", resp.data);
      })
      .catch(err => console.log(err));
  },

  remove_resource: async function({ commit }, payload) {
    let url = "/api/unlink_resource";
    await api_call({
      url: url,
      resource_id: payload.resource_id
    })
      .then(_ => {
        commit("unlink_resource", payload.resource_id);
      })
      .catch(err => console.log(err));
  },

  resource_action: async function({ commit }, payload) {
    await api_call({ ...payload.to_server }).then(resp => {
      payload.server_response = resp.data;
      commit(payload.mutation, { ...payload });
    });
  },

  update: async function({ commit }) {
    let url = "/api/ping";

    await api_call({ url: url })
      .then(resp => {
        if (resp.data.length > 0) {
          resp.data.forEach(update => {
            commit("add_update", update);
          });
        }
      })
      .catch(err => console.log(err));
  },

  reset_resource_lists: function({ commit }) {
    commit("reset_resource_lists");
  },

  update_resource: async function({ commit }, payload) {
    commit("add_update", payload);
  },

  loading({ commit }, payload) {
    commit("loading", payload);
  }
};

const mutations = {
  set_resources: function(commit, resources) {
    resources.forEach(resource => {
      if (state.resources.some(el => el._id === resource._id)) {
        return;
      } else {
        state.resources.push(resource);
      }
    });
  },

  reset_resource_lists: function() {
    state.resources = [];
  },

  unlink_resource: function(commit, resource_id) {
    state.resources = state.resources.filter(el => el._id !== resource_id);
  },

  add_update: async function(commit, update) {
    let url = "/api/get_resource";
    let resource_id = update.resource_id;

    await api_call({
      url: url,
      resource_id: resource_id
    }).then(resp => {
      let resp_as_json = null;
      try {
        resp_as_json = JSON.parse(resp.data);
        // state[resource_list] = state[resource_list].filter(
        //   el => el._id !== resp_as_json._id
        // );
        // state[resource_list].push(resp_as_json);
      } catch (error) {
        resp_as_json = resp.data;
      }

      let resource = state.resources.find(el => el._id === resource_id);
      resource.plugins = resp_as_json.plugins;
      resource.tags = resp_as_json.tags;
    });
  },

  loading: function(state, payload) {
    let resource = state.resources.find(el => el._id === payload._id);
    let plugin = resource.plugins.find(el => el.name === payload.plugin);
    if (plugin) {
      plugin.results = "loading";
    } else {
      resource.plugins.push({
        name: payload.plugin,
        results: "loading"
      });
    }
  }
};

const getters = {
  // reusable data accessors
  get_resources: state => resource_type => {
    return state.resources.filter(elem => elem.resource_type === resource_type);
  },
  loadingResources: state => {
    return state.resources.filter(plugins =>
      plugins.plugins.some(results => results.results === "loading")
    );
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
