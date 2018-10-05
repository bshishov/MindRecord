<template>
  <tr>
    <td>
      <div class="header">{{ header }}</div>
      <div class="description" v-if="description">{{ description }}</div>
    </td>
    <td class="value">{{ value }} {{ units }}</td>
  </tr>
</template>

<script>
    export default {
      name: "ResultRow",
      props: ['header', 'description', 'value', 'units']
    }
</script>

<style scoped>

</style>
