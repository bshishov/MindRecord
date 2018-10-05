<template>
  <div class="error message">
    Ошибка {{ $route.params.code }}
  </div>
</template>

<script>
  export default {
    name: "ErrorPage",
    data() {
      return {}
    }
  }
</script>

<style scoped>

</style>
