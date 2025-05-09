<template>
  <div v-if="data && data.length">
    <h2>Time Series</h2>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from "vue";
import { Chart } from "chart.js/auto";

const props = defineProps({
  data: Array,
});

const canvas = ref(null);
let chart = null;

// Function to render or update the chart
const renderChart = async () => {
  if (!props.data?.length) return;

  await nextTick(); // Wait for DOM to update

  const ctx = canvas.value?.getContext("2d");
  if (!ctx) return;

  const labels = props.data.map((point) => point.t);
  const values = props.data.map((point) => point.value);

  // Destroy previous chart if it exists
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: props.label || "Time Series",
          data: values,
          borderColor: "blue",
          borderWidth: 1,
          pointRadius: 0,
        },
      ],
    },
    options: {
      responsive: true,
      animation: false,
      scales: {
        x: {
          title: { display: true, text: "t (seconds)" },
        },
        y: {
          title: { display: true, text: "Value" },
        },
      },
    },
  });
};

onMounted(renderChart);

// Rerender whenever `data` changes
watch(() => props.data, renderChart, { deep: true });
</script>
