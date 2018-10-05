<i18n>
{
  "en": {
    "start": "Start"
  },
  "ru": {
    "start": "Начать"
  }
}
</i18n>

<template>
  <div class="hero">
    <div class="container">
      <h1 class="caption">{{ test.name }}</h1>
      <h3 class="description">{{ test.short_description }}</h3>
      <router-link :to="{ name: 'TestRunPage', params: { id: test.id }}" class="big primary button">{{ $t('start') }}</router-link>
    </div>
  </div>
</template>

<script>
  export default {
    name: "TestPage",
    data() {
      return {
        test: {
          name: null,
          short_description: null,
        }
      }
    },
    mounted: function () {
      let testId = this.$route.params.id;
      this.$api.request(`/tests/${testId}`).then(function (data) {
        console.log(data);
        this.test = data;
      }.bind(this)).catch(function () {
        this.$router.push('/error/404');
      }.bind(this));
    }
  }
</script>

<style scoped>
  .hero {
    text-align: center;
    background: #c8ffdd;
    padding: 50px 0;
  }
  .hero  .description {
    margin-bottom: 30px;
  }
</style>
