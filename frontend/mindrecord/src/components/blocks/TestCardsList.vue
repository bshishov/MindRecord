<template>
  <div>
    <div class="cards" v-if="tests">
      <TestCard v-for="test in tests" :key="test.id" v-bind:test="test"/>
    </div>
    <Loader v-else></Loader>
  </div>
</template>

<script>
  import TestCard from "./TestCard";
  import Loader from "./Loader";
  export default {
  name: 'TestCardsList',
    components: {Loader, TestCard},
    data() {
    return {
      tests: undefined
    }
  },
  mounted() {
    this.$api.request('/tests').then(tests => {
      this.tests = tests;
    })
  }
}
</script>

<style scoped>
  .cards {
    display: flex;
    flex-flow: row wrap;
    align-items: stretch;
    justify-content: space-around;
  }
  .cards > .card {
    margin-bottom: 20px;
    width: calc(1/5*100% - (1 - 1/5)*10px);
    box-sizing: border-box;
  }
</style>
