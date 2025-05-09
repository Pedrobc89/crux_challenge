<template>
  <div>
    <h2>Table</h2>
    <table v-if="rows.length">
      <thead>
        <tr>
          <th v-for="(val, key) in rows[0]" :key="key">{{ key }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in rows" :key="i">
          <td v-for="(val, key) in row" :key="key">{{ val }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps(["rows"]);
</script>
