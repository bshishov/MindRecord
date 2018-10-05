import Vue from 'vue'
import Vuex from 'vuex'
import {accessTokenKey} from "./mindrecord";
import {api} from "./api";

Vue.use(Vuex)

// Mutations
const AUTH_STARTED = "AUTH_STARTED";
const AUTH_SUCCESS = "AUTH_SUCCESS";
const AUTH_LOGOUT = "AUTH_LOGOUT";
const AUTH_ERROR = "AUTH_ERROR";

export default new Vuex.Store({
  state: {
    pending: false,
    isAuthorized: api.isAuthorized,
    status: '',
    token: localStorage.getItem(accessTokenKey) || '',
    user : api.user
  },
  mutations: {
    [AUTH_STARTED] (state) {
      state.status = 'pending'
      state.pending = true
    },
    [AUTH_SUCCESS] (state, user) {
      state.status = 'success'
      state.isAuthorized = true
      state.pending = false
      state.user = user
    },
    [AUTH_LOGOUT](state) {
      state.isAuthorized = false
      state.user = undefined
    },
    [AUTH_ERROR](state, err) {
      state.status = 'error'
    }
  },
  actions: {
    loginAnonymous({commit}) {
      return new Promise((resolve, reject) => {
        commit(AUTH_STARTED);
        api.loginAnonymous()
          .then(resp => {
            commit(AUTH_SUCCESS, api.user)
            //dispatch()  // request user details
            resolve(resp)
          })
          .catch(err => {
            commit(AUTH_ERROR, err)
            reject(err)
          })
      });
    },
    login({commit}, credentials) {
      return new Promise((resolve, reject) => {
        commit(AUTH_STARTED);
        api.loginEmail(credentials.email, credentials.password)
          .then(resp => {
            commit(AUTH_SUCCESS, api.user)
            //dispatch()  // request user details
            resolve(resp)
          })
          .catch(err => {
            commit(AUTH_ERROR, err)
            reject(err)
          })
      });
    },
    logout({commit}) {
      return new Promise(resolve => {
        api.logout();
        commit(AUTH_LOGOUT);
        resolve()
      });
    },
  },
  getters : {
    authStatus: state => state.status,
    userId: state => state.user? state.user['sub'] : undefined,
    userRole: state => state.user? state.user['role'] : undefined,
    isAdmin: state => state.user? state.user['role'] === 'admin': false,
  }
})
