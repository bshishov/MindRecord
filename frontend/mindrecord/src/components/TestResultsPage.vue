<i18n>
{
  "en": {
    "retry": "Retry",
    "next": "Next"
  },
  "ru": {
    "retry": "Ещё раз",
    "next": "Далее"
  }
}
</i18n>

<template>
    <div class="container">
      <div v-if="test" class="result-container">
        <h2>{{ test.name }}</h2>
        <ResultCard :test="test" :result="result" />

        <div class="buttons" v-if="canRestart">
          <router-link :to="{ name: 'TestRunPage', params: { id: test.id }}" class="big button">
            <i class="fas fa-undo"></i> {{ $t('retry') }}
          </router-link>
          <div class="big primary button">{{ $t('next') }}</div>
        </div>
      </div>
      <Loader v-else></Loader>
      <div v-if="isAdmin" class="system">
        <a href="javascript:void(0)" v-on:click="logResultLog()">Log</a>
        <a href="javascript:void(0)" v-on:click="logResultErrorLog()">Error Log</a>
      </div>
    </div>
</template>

<script>
  import ResultCard from "./blocks/ResultCard";
  import Loader from "./blocks/Loader";
  export default {
    name: "TestResultsPage",
    components: {Loader, ResultCard},
    data() {
      return {
        test: null,
        result: null
      }
    },
    methods: {
      restart: function (event) {
        this.$router.push(`/tests/${this.test.id}/run`)
      },
      logResultLog: function () {
        this.$api.getResultsLog(this.result.id).then(res => {
          console.log(res);
        })
      },
      logResultErrorLog: function () {
        this.$api.getResultsErrorLog(this.result.id).then(res => {
          console.log(res);
        })
      }
    },
    mounted() {
      this.$api.getResults(this.$route.params.rid).then((result) => {
        this.result = result;

        this.$api.getTest(result.test).then((data) => {
          this.test = data;
        });
      });
    },
    computed: {
      canRestart: function() {
        if (!this.result || !this.result.test || !this.result.user)
          return false;

        return this.result.user === this.$store.getters.userId;
      },
      isAdmin: function () {
        return this.$store.getters.isAdmin;
      }
    }
  }
</script>

<style scoped>
  .result-container {
    margin: 0 auto;
    text-align: center;
  }
  .buttons {
    margin-top: 20px;
  }
</style>
