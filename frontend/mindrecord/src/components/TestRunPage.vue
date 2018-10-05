<template>
  <div class="container">
    <iframe id="frame"
            :src="framePath"
            class="frame"
            sandbox="allow-scripts"
            width="100%"
            height="500px"
            frameborder="0"
            scrolling="no"></iframe>
    <div class="dimmer" v-show="dimmer">
      <div class="content">
        <Loader></Loader>
      </div>
    </div>
  </div>
</template>

<script>
  import Loader from "./blocks/Loader";
  let parseUrl = (function () {
    let a = document.createElement('a');
    return function (url) {
      a.href = url;
      return {
        host: a.host,
        hostname: a.hostname,
        pathname: a.pathname,
        port: a.port,
        protocol: a.protocol,
        search: a.search,
        hash: a.hash
      };
    }
  })();

  export default {
    name: "TestRunPage",
    components: {Loader},
    data() {
      return {
        framePath: null,
        test: {
          name: null,
          short_description: null,
        },
        dimmer: false
      }
    },
    created: function() {
        let urlInfo = parseUrl(this.$api.apiPath);
        let frameOrigin = `${urlInfo.protocol}//${urlInfo.host}`;
        const frame = document.getElementById('frame');
        console.log('[TEST RUN] Frame origin:', frameOrigin);
        window.addEventListener("message", function(e) {
          console.log('[TEST RUN] Message:', e);

          if (e.origin === "null" && e.source === frame.contentWindow){
            let testData = e.data;
            console.log('[TEST RUN] Received data:', testData);
          }
        }, false);
    },
    mounted: function() {
      let testId = this.$route.params.id;
      this.$api.getTest(testId).then(function (data) {
        console.log(data);
        this.test = data;

        if (!this.$store.state.isAuthorized) {
          console.log('[TEST RUN] Anonymous authorization');
          this.$store.dispatch('loginAnonymous')
        }

        this.framePath = `${this.$api.apiPath}/tests/${testId}/web/?attempts=1`;

        window.addEventListener("message", (e) => {
          console.log('[TEST RUN] Message:', e);

          if (e.origin === "null" && e.source === frame.contentWindow){
            this.dimmer = true;
            let testData = e.data;
            console.log('[TEST RUN] Received data:', testData);
            this.$api.postResults(testId, testData).then(function(response) {
              let resultsId = response['results_id']
              if (resultsId)
                this.$router.push(`/tests/${testId}/results/${resultsId}`)
            }.bind(this));
          }
        }, false);
      }.bind(this)).catch(function () {
        this.$router.push('/error/404');
      }.bind(this));
    }
  }
</script>

<style scoped>
  .frame {
    background: white;
    border-radius: 10px;
    border: 1px solid #eee;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
  }
  .dimmer {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
  }

  .dimmer > .content {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 400px;
    height: 200px;
    margin-top: -100px;
    margin-left: -200px;
    background: white;
    border-radius: 20px;
    box-shadow: 0px 0 40px rgba(0,0,0,0.3);

    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
