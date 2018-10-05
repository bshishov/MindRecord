<template>
  <header class="header">
    <div class="container">
      <div class="left menu">
        <router-link :to="{ name: 'HomePage'}" class="item">
          <img src="../../assets/logo.png" alt="MindRecord" height="30">
        </router-link>
      </div>
      <div class="right menu">
        <ProfileBlock></ProfileBlock>
      </div>
    </div>
  </header>
</template>

<script>
import ProfileBlock from "./ProfileBlock";
import LocaleSwitcher from "./LocaleSwitcher";

export default {
  name: "Header",
  components: {LocaleSwitcher, ProfileBlock}
}
</script>

<style scoped>
  .header{
    margin-bottom: 50px;
  }

  .header > .container {
    display: flex;
    flex-flow: row wrap;

    align-items: stretch;
    justify-content: space-between;
  }
</style>
