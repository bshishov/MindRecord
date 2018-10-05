<i18n>
{
  "en": {
    "myResults": "My results"
  },
  "ru": {
    "myResults": "Мои результаты"
  }
}
</i18n>

<template>
  <div class="hero">
    <div class="container">
      <h1>{{ $t('myResults') }}</h1>
      <h3 class="description"><i class="far fa-user fa-inverted"></i> {{ $store.getters.userId }}</h3>
    </div>
  </div>
</template>

<script>
    export default {
        name: "ProfilePage",
        data() {
          return {
            results: []
          }
        },
        mounted() {
          if(!this.$store.state.isAuthorized)
            this.$router.push('/');
        }
    }
</script>

<style scoped>
  .hero {
    text-align: center;
    background: #cce8ff;
    padding: 50px 0;
  }
  
  .hero .description {
    color: #8b8acc;
  }
</style>
