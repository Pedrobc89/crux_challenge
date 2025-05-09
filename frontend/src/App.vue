<template>
  <div>
    <h1>Crux Data Viewer</h1>
    <button @click="getData">Get Data</button>

    <NumberDisplay :value="number" />
    <TimeSeriesChart :data="timeSeries" :label="timeSeriesLabel" />
    <TableDisplay :rows="table" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import NumberDisplay from "./components/NumberDisplay.vue";
import TableDisplay from "./components/TableDisplay.vue";
import TimeSeriesChart from "./components/TimeSeriesChart.vue";

const number = ref(null);
const table = ref([]);
const timeSeries = ref([]);
const timeSeriesLabel = ref("");

async function getData() {
  number.value = null;
  table.value = [];
  timeSeries.value = [];
  timeSeriesLabel.value = "Time Series";

  const response = await fetch("/aggregate-data");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop();

    for (const line of lines) {
      if (!line.trim()) continue;
      const obj = JSON.parse(line);
      if (obj.path === "/random-int") {
        number.value = obj.data;
      } else if (obj.path === "/table") {
        table.value = obj.data;
      } else if (obj.path === "/time-series") {
        timeSeries.value = obj.data;
      }
    }
  }
}
</script>
