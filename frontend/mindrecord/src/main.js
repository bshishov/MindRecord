// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import VueI18n from 'vue-i18n'

import router from './router'
import {api} from "./api";
import App from './App'

Vue.use(VueI18n)




Vue.prototype.$api = api;

const getNavigatorLanguage = () => {
  if (navigator.languages && navigator.languages.length) {
    return navigator.languages[0];
  } else {
    return navigator.userLanguage || navigator.language || navigator.browserLanguage || 'en';
  }
}

const defaultLang = getNavigatorLanguage().substring(0, 2);
let lang = localStorage.getItem('lang') || defaultLang;
console.log('Lang:', lang)

const i18n = new VueI18n({ locale: lang })
import store from "./store"

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>',
  i18n
})


