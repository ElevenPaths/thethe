import Vue from "vue";
import Vuex from "vuex";

import { RESET_PROJECT, SET_PROJECT } from "../actions/project";
import { object_is_empty } from "../../utils/utils";

Vue.use(Vuex);

const state = {
  project: {}
};

const getters = {
  get_opened_project: state => state.project,
  is_project_opened: state => {
    if (object_is_empty(state.project)) {
      return false;
    } else {
      return true;
    }
  }
};

const actions = {
  [SET_PROJECT]: ({ commit, dispatch }, project) => {
    commit(SET_PROJECT, project);
    dispatch("get_resources", null, { root: true });
  },
  [RESET_PROJECT]: ({ state, commit, dispatch }) => {
    dispatch("reset_resource_lists", null, { root: true });
    commit(RESET_PROJECT);
  }
};

const mutations = {
  [SET_PROJECT]: (state, project) => {
    state.project = project;
  },
  [RESET_PROJECT]: state => {
    state.project = {};
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
