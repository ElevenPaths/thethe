import Vue from "vue";
import Vuex from "vuex";

import api_call from "../../utils/api";

Vue.use(Vuex);

const state = {
  iplist: [],
  domainlist: [],
  emaillist: [],
  hashlist: [],
  urllist: [],
  usernamelist: []
};

const actions = {
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
  }
};

const mutations = {
  reset_resource_lists: function() {
    Object.keys(state).forEach(el => (state[el] = []));
  },

  set_resource_list: function(commit, payload) {
    let resources = [];
    payload.server_response.forEach(resource => {
      resources.push(resource);
    });
    state[payload.mutation_args.list_name] = resources;
  },

  remove_resource: function(commit, payload) {
    let resource_list = payload.mutation_args.list_name;

    state[resource_list] = state[resource_list].filter(
      el => el._id !== payload.to_server.resource_id
    );
  },

  add_resource: function(commit, payload) {
    payload.server_response.forEach(resource => {
      let list_name = resource.type + "list";
      let new_resource = resource.new_resource;
      let resource_list = state[list_name];
      if (resource_list.some(el => el._id === new_resource._id)) {
        return;
      }
      resource_list.push(new_resource);
    });

    return payload.server_response;
  },

  add_update: async function(commit, update) {
    let url = "/api/get_resource";
    let resource_id = update.resource_id;
    let resource_type = update.resource_type;
    let resource_list = resource_type + "list";

    await api_call({
      url: url,
      resource_id: resource_id,
      resource_type: resource_type
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

      let resource = state[resource_list].find(el => el._id === resource_id);
      resource.plugins = resp_as_json.plugins;
      resource.tags = resp_as_json.tags;
    });
  }
};

const getters = {
  // reusable data accessors
  get_resources: state => resource_list => state[resource_list]
};

export default {
  state,
  getters,
  actions,
  mutations
};
