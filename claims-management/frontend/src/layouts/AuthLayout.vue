<template>
  <main class="auth-shell">
    <section class="auth-brand">
      <div class="orb orb-top"></div>
      <div class="orb orb-bottom"></div>

      <div class="brand-logo">
        <span class="brand-shield" aria-hidden="true">
          <svg viewBox="0 0 24 24" role="img" focusable="false">
            <path
              d="M12 3l7 3v5c0 4.7-2.9 8.8-7 10-4.1-1.2-7-5.3-7-10V6l7-3z"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M9.2 12.2l2 2 3.6-3.6"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </span>
        <span class="brand-name">ClaimFlow</span>
      </div>

      <div class="brand-copy">
        <h1>Streamline your insurance claims</h1>
        <p>
          A modern platform for managing insurance claims
          with speed, transparency, and ease.
        </p>
      </div>

      <div class="brand-stats">
        <article>
          <strong>50K+</strong>
          <span>Claims Processed</span>
        </article>
        <article>
          <strong>98%</strong>
          <span>Satisfaction Rate</span>
        </article>
        <article>
          <strong>24h</strong>
          <span>Avg Resolution</span>
        </article>
      </div>
    </section>

    <section class="auth-form-panel">
      <div class="auth-form-wrap">
        <slot />
      </div>
    </section>
  </main>
</template>
