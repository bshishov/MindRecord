<i18n>
{
  "en": {
    "loginAnon": "Sign in anonymously",
    "or": "or",
    "emailLabel": "Email",
    "emailPlaceholder": "qwerty@example.com",
    "passwordLabel": "Password",
    "signUp": "Sign Up",
    "signIn": "Sign In"
  },
  "ru": {
    "loginAnon": "Войти анонимно",
    "or": "или",
    "emailLabel": "Email",
    "emailPlaceholder": "qwerty@example.com",
    "passwordLabel": "Пароль",
    "signUp": "Регистрация",
    "signIn": "Вход"
  }
}
</i18n>

<template>
  <div class="form">
    <div class="primary button" v-on:click="loginAnon()">{{ $t('loginAnon') }}</div>
    <div style="width:90%">
      <div class="or">{{ $t('or') }}</div>
    </div>
    <form @submit.prevent="loginEmail({ email, password })">
      <div class="field">
        <label>{{ $t('emailLabel') }}</label>
        <input type="email" class="text" name="email" :placeholder="$t('emailPlaceholder')" v-model="email"/>
      </div>
      <div class="field">
        <label>{{ $t('passwordLabel') }}</label>
        <input type="password" class="text" name="password" v-model="password"/>
      </div>
      <div class="field">
        <button type="submit" class="primary button">{{ $t('signIn')}} / {{ $t('signUp')}}</button>
      </div>
    </form>
  </div>
</template>

<script>
  export default {
    name: "LoginForm",
    data() {
      return {
        email: "",
        password: ""
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
        this.$store.dispatch('login', {
          email: this.email,
          password: this.password
        })
      },
    }
  }
</script>

<style scoped>
  .form {
    padding: 10px;
    display: flex;
    flex-flow: column;
    align-items: center;
    justify-content: center;
    color: black;
  }

  .or {
    margin: 10px 0;
    color: #aaa;
    display: flex;
    flex-direction: row;
  }
  .or:before, .or:after{
    content: "";
    flex: 1 1;
    border-bottom: 1px solid #aaa;
    margin: auto;
  }

  form {
    padding: 0 10px;
    text-align: center;
  }

  form .field {
    margin-top: 20px;
    margin-bottom: 10px;
  }

  form .field label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 0.8em;
  }

  input.text {
    background: #fbfbfb;
    margin: 0 auto;
    width: 93%;
    padding: 10px 10px;
    border-radius: 8px;
    border: 1px solid #e3e3e3;
    font-size: 1.1em;
    transition: all 0.3s ease-in-out;
  }

  input.text::placeholder {
    color: #ccc;
  }

  input.text:focus {
    outline: none;
    box-shadow: 0 0 8px rgba(100,255,100,1);
    background: white;
  }
</style>
