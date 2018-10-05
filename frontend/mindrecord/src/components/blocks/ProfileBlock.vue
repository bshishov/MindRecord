<i18n>
{
  "en": {
    "profile": {
      "myProfile": "My profile",
      "logout": "Logout",
      "signUp": "Sign Up",
      "signIn": "Sign In"
    }
  },
  "ru": {
    "profile": {
      "myProfile": "Мой профиль",
      "logout": "Выход",
      "signUp": "Регистрация",
      "signIn": "Вход"
    }
  }
}
</i18n>


<template>
  <div v-if="$store.state.isAuthorized">
    <div class="button group">
      <router-link :to="{ name: 'ProfilePage', params: {id: userId}}" class="primary button">
        <i class="fas fa-user"></i> {{ $t('profile.myProfile')}}
      </router-link>
      <div href="#" class="button" v-on:click="logout()"><i class="fas fa-sign-out-alt"></i> {{ $t('profile.logout')}}</div>
    </div>
  </div>
  <div v-else>
    <div class="login">
      <div class="button primary" v-on:click="togglePopup()">
        <i class="fas fa-sign-in-alt"></i> {{ $t('profile.signIn')}} / {{ $t('profile.signUp')}}
      </div>
      <div class="popup" v-show="showPopup">
        <LoginForm></LoginForm>
      </div>
    </div>
  </div>
</template>

<script>

import LoginForm from "./LoginForm";
export default {
  name: "ProfileBlock",
  components: {LoginForm},
  data() {
    return {
      showPopup: false
    }
  },
  computed: {
    isAuthorized: function() { return this.$store.state.isAuthorized },
    user: function() { return this.$store.state.user },
    userId: function() { return this.$store.getters.userId },
  },
  methods: {
    logout: function (event) {
      this.$store.dispatch('logout')
    },
    loginAnon: function (event) {
      this.$store.dispatch('loginAnonymous')
    },
    loginEmail: function (event) {
      // NOT IMPLEMENTED!
    },
    togglePopup: function (event) {
      this.showPopup = !this.showPopup;
    }
  },
  mounted() {
    this.showPopup = false;
  }
}
</script>

<style scoped>
  .login {
    position: relative;
    display: inline-block;
  }
  .login .popup {
    width: 300px;
    color: #fff;
    text-align: center;
    padding: 5px 0;
    margin-top: 20px;

    right:0;

    /* Position the tooltip text - see examples below! */
    position: absolute;
    z-index: 999;

    background: white;
    border-radius: 15px;
    box-shadow: 0px 0 20px rgba(0,0,0,0.3);


  }
</style>
