<i18n>
{
  "en": {"loading": "Loading..."},
  "ru": {"loading": "Загрузка..."}
}
</i18n>

<template>
  <div class="loader">
    <div class="lds-dual-ring"></div>
    <div class="caption" v-if="caption">{{ caption }}</div>
    <div class="caption" v-else>{{ $t('loading') }}</div>
  </div>
</template>

<script>
  export default {
    props: ['caption'],
    name: "Loader"
  }
</script>

<style scoped>
  .loader {
    text-align: center;
  }

  .lds-dual-ring {
    display: inline-block;
    width: 64px;
    height: 64px;
  }
  .lds-dual-ring:after {
    content: " ";
    display: block;
    width: 46px;
    height: 46px;
    margin: 1px;
    border-radius: 50%;
    border: 5px solid #ccc;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
  }
  @keyframes lds-dual-ring {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
