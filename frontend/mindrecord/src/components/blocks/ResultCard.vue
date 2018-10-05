<i18n>
{
  "en": {
    "result": {
      "metric": "Metric",
      "score": "Score",
      "processing": {
        "error": "Results processing error :(",
        "progress": "Processing..."
      }
    }
  },
  "ru": {
    "result": {
      "metric": "Показатель",
      "score": "Результат",
      "processing": {
        "error": "Ошибка расчета :(",
        "progress": "Обрабатываем..."
      }
    }
  }
}
</i18n>

<template>
  <div class="result-container">
    <table class="result" v-if="result.state == 'processed'">
      <thead>
        <tr>
          <td width="70%">{{ $t('result.metric') }}</td>
          <td width="30%">{{ $t('result.score') }}</td>
        </tr>
      </thead>
      <tbody>
        <ResultRow v-for="m in metrics" :key="m.id" :header="m.name" :description="m.description" :value="m.value" :units="m.units"></ResultRow>
      </tbody>
      <tfoot>
        <tr><td colspan="2">{{ result.processed | fromIso }}</td></tr>
      </tfoot>
    </table>
    <div class="result" v-if="result.state == 'raw'">
      <Loader :caption="$t('result.processing.progress')"></Loader>
    </div>
    <div class="result error" v-if="result.state == 'fail'">
      {{ $t('result.processing.error') }}
      <div class="message">Id: {{ result.id }}</div>
    </div>
  </div>
</template>

<script>
  import ResultRow from "./ResultRow";
  import Loader from "./Loader";

  const resultsPollInterval = 1000;

  export default {
    components: {Loader, ResultRow},
    props: ['result', 'test'],
    name: "ResultCard",
    computed: {
      metrics: function () {
        let values = this.result.data;
        let outputs = this.test.outputs;
        if (!outputs || !values)
          return undefined;

        let metrics = [];
        for (let key in outputs) {
          let outputSpec = outputs[key];
          let val = '-';
          if(key in values)
            val = values[key];

          metrics.push({
            id: key,
            name: outputSpec.name,
            description: outputSpec.description,
            value: val,
            units: outputSpec.units})
        }
        return metrics;
      }
    },
    filters: {
      fromIso: function (value) {
        return new Date(value).toString();
      }
    },
    mounted() {
      if(this.result.state === 'raw' && this.result.id !== undefined){
        let check = function () {
          this.$api.getResults(this.result.id).then(res => {
            this.result = res;
            if (res.state === 'raw')
              setTimeout(check, resultsPollInterval)
          });
        }.bind(this)

        setTimeout(check, resultsPollInterval)
      }
    }
  }
</script>

<style>
  .result {
    background: #efefef;
    border-radius: 15px;
    width: 400px;
    box-shadow: 0 0 5px rgba(0,0,0,0.2);
    margin: 0 auto;
    text-align: left;
  }

  table.result {
    display: block;
  }

  div.result {
    padding: 20px 0;
  }

  div.result.error {
    padding: 20px 0;
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    background: rgba(167, 0, 0, 0.34);
  }

  div.result.error .message {
    margin-top: 10px;
    font-size: 0.6em;
    font-weight: normal;
  }

  table.result thead td {
    padding: 15px 15px;
    font-size: 1.2em;
    font-weight: bold;
    border-bottom: 1px solid #ccc;
  }

  table.result tbody td {
    background: white;
    padding: 10px 15px;
    border-bottom: 1px solid #ccc;
    vertical-align: middle;
  }

  table.result tbody td .header {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 5px;
  }

  table.result tbody .value {
    font-size: 1.2em;
    font-weight: bold;
  }

  table.result tbody td .description {
    font-size: 0.8em;
  }

  table.result tfoot td {
    padding: 10px 15px;
    font-size: 0.8em;
  }
</style>
