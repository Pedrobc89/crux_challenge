<template>
  <div>
    <h2>Random Number</h2>
    <p v-if="value !== null">{{ value }}</p>
  </div>
</template>

<script setup>
defineProps(["value"]);
</script>
