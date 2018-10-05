<template>
  <router-link :to="{ name: 'TestPage', params: { id: test.id }}" class="card">
    <div class="image">
      <img :src="cover" width="100%" :alt="test.name">
    </div>
    <div class="content">
      <div class="header">{{ test.name }}</div>
      <div class="description">{{ test.short_description }}</div>
    </div>
  </router-link>
</template>

<script>
  export default {
    props: ['test'],
    name: "TestCard",
    data() {
      return {
        cover: null
      }
    },
    mounted() {
      this.cover = `${this.$api.apiPath}/tests/${this.test.id}/cover`;
    }
  }
</script>

<style scoped>
  .card {
    display: block;
    min-width: 220px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 0 6px rgba(0,0,0,0.2);
    text-decoration: none;
    overflow: hidden;
    color: black;
    transition: all .2s ease-out;
  }
  .card:hover {
    transform: translate(0, -5px);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
  }
  .card > .image {
    background: #eee;
    width: 100%;
    display: block;
  }
  .card > .image > img {
    object-fit: cover;
    height: 200px;
    width: 100%;
  }
  .card > .content {
    padding: 12px;
  }
  .card > .content > .header {
    font-size: 1.3em;
  }
  .card > .content > .description {
    margin-top: 5px;
    font-size: 0.9em;
    color: #555 !important;
  }
</style>
