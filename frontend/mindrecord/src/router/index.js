import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'

import HomePage from '../components/HomePage.vue'
import TestPage from '../components/TestPage.vue'
import ProfilePage from '../components/ProfilePage.vue'
import ErrorPage from '../components/ErrorPage.vue'
import TestRunPage from '../components/TestRunPage'
import TestResultsPage from '../components/TestResultsPage'


Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [
    {path: '/', name: HomePage.name, component: HomePage},

    {path: '/tests/:id', name: TestPage.name, component: TestPage},
    {path: '/tests/:id/run', name: TestRunPage.name, component: TestRunPage},
    {path: '/tests/:id/results/:rid', name: TestResultsPage.name, component: TestResultsPage},

    {path: '/playlist/:id', name: TestPage.name, component: TestPage},

    {path: '/profile/:id', name: ProfilePage.name, component: ProfilePage, meta: {requiresAuth: true}},
    {path: '/error/', name: ErrorPage.name, component: ErrorPage},
    {path: '/error/:code', name: ErrorPage.name, component: ErrorPage},
  ]
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.state.isAuthorized) {
      next()
      return
    }
    next('/')
  } else {
    next()
  }
})

export default router
