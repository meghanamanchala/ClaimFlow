<template>
  <section>
    <header class="page-head">
      <h1>Analytics</h1>
      <p>System performance and claim statistics</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Total Claims</p>
        <p class="stat-value">156</p>
        <p class="stat-note positive">+12%</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Approval Rate</p>
        <p class="stat-value">73%</p>
        <p class="stat-note positive">+5%</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Avg Processing</p>
        <p class="stat-value">2.4 days</p>
        <p class="stat-note positive">-0.3 days</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Total Payouts</p>
        <p class="stat-value">$284K</p>
      </article>
    </section>

    <section class="dashboard-grid admin-grid">
      <article class="panel">
        <h2>Monthly Claims</h2>
        <div class="bar-chart">
          <div class="bar-col" v-for="bar in bars" :key="bar.month">
            <div class="bar" :style="{ height: `${bar.value}%` }"></div>
            <span>{{ bar.month }}</span>
          </div>
        </div>
      </article>

      <article class="panel">
        <h2>Claims by Status</h2>
        <div class="donut-wrap">
          <div class="donut-chart"></div>
          <ul class="legend-list">
            <li><span class="legend-dot approved"></span>Approved 45%</li>
            <li><span class="legend-dot review"></span>Under Review 25%</li>
            <li><span class="legend-dot pending"></span>Pending 20%</li>
            <li><span class="legend-dot rejected"></span>Rejected 10%</li>
          </ul>
        </div>
      </article>
    </section>

    <article class="panel analytics-line-panel">
      <h2>Avg Processing Time (Days)</h2>
      <svg viewBox="0 0 600 160" class="line-chart" preserveAspectRatio="none">
        <polyline points="0,30 100,45 200,40 300,60 400,55 500,58 600,62" class="line-path" />
        <g class="line-points">
          <circle cx="0" cy="30" r="3"></circle>
          <circle cx="100" cy="45" r="3"></circle>
          <circle cx="200" cy="40" r="3"></circle>
          <circle cx="300" cy="60" r="3"></circle>
          <circle cx="400" cy="55" r="3"></circle>
          <circle cx="500" cy="58" r="3"></circle>
          <circle cx="600" cy="62" r="3"></circle>
        </g>
      </svg>
      <div class="axis-labels">
        <span>Oct</span>
        <span>Nov</span>
        <span>Dec</span>
        <span>Jan</span>
        <span>Feb</span>
        <span>Mar</span>
      </div>
    </article>
  </section>
</template>

<script setup>
const bars = [
  { month: 'Oct', value: 52 },
  { month: 'Nov', value: 75 },
  { month: 'Dec', value: 63 },
  { month: 'Jan', value: 86 },
  { month: 'Feb', value: 80 },
  { month: 'Mar', value: 92 }
];
</script>
