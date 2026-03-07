<template>
  <section>
    <header class="page-head">
      <h1>Analytics</h1>
      <p>System performance and claim statistics</p>
    </header>

    <section class="stat-grid">
      <article class="stat-card">
        <p class="stat-title">Total Claims</p>
        <p class="stat-value">{{ totalClaims }}</p>
        <p class="stat-note positive">Live</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Approval Rate</p>
        <p class="stat-value">{{ approvalRate }}%</p>
        <p class="stat-note positive">Approved + paid</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Avg Processing</p>
        <p class="stat-value">{{ avgProcessing }} days</p>
        <p class="stat-note positive">Timeline based</p>
      </article>
      <article class="stat-card">
        <p class="stat-title">Total Payouts</p>
        <p class="stat-value">{{ totalPayouts }}</p>
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
          <div class="donut-chart" :style="donutStyle"></div>
          <ul class="legend-list">
            <li v-for="item in statusLegend" :key="item.label">
              <span class="legend-dot" :style="{ background: item.color }"></span>{{ item.label }} {{ item.percent }}%
            </li>
          </ul>
        </div>
      </article>
    </section>

    <article class="panel analytics-line-panel">
      <h2>Avg Processing Time (Days)</h2>
      <svg viewBox="0 0 600 160" class="line-chart" preserveAspectRatio="none">
        <polyline :points="linePoints" class="line-path" />
      </svg>
      <div class="axis-labels">
        <span v-for="label in monthLabels" :key="label">{{ label }}</span>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { getClaims } from '../../services/api';
import { formatCurrency, getStatusLabel } from '../../services/claimTransforms';

const claims = ref([]);

const monthLabels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];

const totalClaims = computed(() => claims.value.length);

const approvalRate = computed(() => {
  if (!claims.value.length) {
    return 0;
  }

  const approved = claims.value.filter((claim) => ['approved', 'paid'].includes(String(claim.status || '').toLowerCase())).length;
  return Math.round((approved / claims.value.length) * 100);
});

const avgProcessing = computed(() => {
  const completed = claims.value.filter((claim) => claim.timeline?.length > 1);
  if (!completed.length) {
    return '0.0';
  }

  const avg =
    completed.reduce((sum, claim) => {
      const first = new Date(claim.timeline[0]?.date);
      const last = new Date(claim.timeline[claim.timeline.length - 1]?.date);
      return sum + Math.max(0, (last - first) / (1000 * 60 * 60 * 24));
    }, 0) / completed.length;

  return avg.toFixed(1);
});

const totalPayouts = computed(() => {
  const paidOrApproved = claims.value.filter((claim) => ['approved', 'paid'].includes(String(claim.status || '').toLowerCase()));
  const total = paidOrApproved.reduce((sum, claim) => sum + Number(claim.approvedAmount || claim.estimatedAmount || 0), 0);
  return formatCurrency(total);
});

const bars = computed(() => {
  const monthCounts = new Map(monthLabels.map((month) => [month, 0]));

  claims.value.forEach((claim) => {
    const created = new Date(claim.createdAt || claim.incidentDate);
    const month = created.toLocaleDateString('en-US', { month: 'short' });
    if (monthCounts.has(month)) {
      monthCounts.set(month, monthCounts.get(month) + 1);
    }
  });

  const max = Math.max(...monthCounts.values(), 1);
  return [...monthCounts.entries()].map(([month, count]) => ({
    month,
    value: Math.max(12, Math.round((count / max) * 100))
  }));
});

const statusLegend = computed(() => {
  const palette = {
    Approved: '#22c55e',
    'Under Review': '#3b82f6',
    Pending: '#f59e0b',
    Rejected: '#ef4444'
  };

  const groups = {
    Approved: 0,
    'Under Review': 0,
    Pending: 0,
    Rejected: 0
  };

  claims.value.forEach((claim) => {
    const status = getStatusLabel(claim.status);
    if (groups[status] !== undefined) {
      groups[status] += 1;
    }
  });

  const total = claims.value.length || 1;
  return Object.entries(groups).map(([label, count]) => ({
    label,
    percent: Math.round((count / total) * 100),
    color: palette[label]
  }));
});

const donutStyle = computed(() => {
  let current = 0;
  const segments = statusLegend.value.map((item) => {
    const start = current;
    const end = current + item.percent;
    current = end;
    return `${item.color} ${start}% ${end}%`;
  });

  return {
    background: `conic-gradient(${segments.join(', ')})`
  };
});

const linePoints = computed(() => {
  const values = bars.value.map((bar) => bar.value);
  const maxValue = Math.max(...values, 1);

  return values
    .map((value, index) => {
      const x = (600 / Math.max(values.length - 1, 1)) * index;
      const y = 140 - (value / maxValue) * 110;
      return `${x},${y}`;
    })
    .join(' ');
});

onMounted(async () => {
  try {
    const { data } = await getClaims();
    claims.value = data || [];
  } catch {
    claims.value = [];
  }
});
</script>
