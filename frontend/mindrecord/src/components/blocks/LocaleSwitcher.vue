<template>
  <div class="locale-changer">
    <a class="ui tiny button" v-if="$i18n.locale !== 'en'" v-on:click="setLang('en')" href="javascript:;">In English</a>
    <a class="ui tiny button" v-if="$i18n.locale !== 'ru'" v-on:click="setLang('ru')" href="javascript:;">На русском</a>
  </div>
</template>

<script>
    export default {
      name: "LocaleSwitcher",
      data () {
        return { langs: ['ru', 'en'] }
      },
      methods: {
        setLang: function (lang) {
          if(lang in ['ru', 'en'])
            console.log('Setting language to', lang)
            localStorage.setItem('lang', lang);
            this.$i18n.locale = lang;
        }
      }
    }
</script>

<style scoped>
</style>
