<i18n>
{
  "en": {
    "footer": {
      "message": "MindRecord - Cognition test platform",
      "author": "Boris Shishov"
    }
  },
  "ru": {
    "footer": {
      "message": "MindRecord - платформа для когнитивного тестирования",
      "author": "Борис Шишов"
    }
  }
}
</i18n>

<template>
  <footer class="footer">
    <div class="container">
      <p><LocaleSwitcher /></p>
      <p v-html="$t('footer.message')"></p>
      <p><a href='https://github.com/bshishov' title="GitHub" target="_blank">{{ $t('footer.author') }}</a> &copy; 2018</p>
    </div>
  </footer>
</template>

<script>
  import LocaleSwitcher from "./LocaleSwitcher";

  export default {
    name: "Footer",
    components: {LocaleSwitcher}
  }
</script>

<style scoped>
.footer {
  margin-top: 100px;
  text-align: center;
  color: #282828;
  font-size: 0.8em;
}
.footer p{
  margin-bottom: 1.5em;
}
</style>
