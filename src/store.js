/* eslint no-param-reassign: ["error", { "props": false }] */
import Vue from 'vue';
import Vuex from 'vuex';
import { authenticate } from './api';
import { EventBus, isValidJwt } from './utils';

Vue.use(Vuex);

const getters = {
  isAuthenticated(state) {
    return isValidJwt(state.jwt.token);
  },
};

const actions = {
  login(context, userData) {
    return authenticate(userData)
      .then(response => context.commit('setJWTToken', { jwt: response.data }))
      .catch((error) => {
        EventBus.$emit('failedAuthentication', error);
      });
  },
};

const mutations = {
  setJWTToken(state, payload) {
    localStorage.token = payload.jwt.token;
    state.jwt = payload.jwt;
  },
};

const state = {
  jwt: '',
};

const store = new Vuex.Store({
  actions,
  mutations,
  state,
  getters,
});

export default store;
