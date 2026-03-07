<template>
  <section>
    <header class="page-head">
      <h1>Settings</h1>
      <p>System configuration and preferences</p>
    </header>

    <article class="panel settings-panel">
      <h2>General</h2>
      <label class="field">
        <span>Company Name</span>
        <input type="text" value="ClaimFlow Inc." />
      </label>
      <label class="field">
        <span>Support Email</span>
        <input type="email" value="support@claimflow.com" />
      </label>
      <button type="button" class="primary-btn">Save Changes</button>
    </article>

    <article class="panel settings-panel">
      <h2>Notifications</h2>
      <ul class="setting-list">
        <li>
          <span>Email notifications for new claims</span>
          <button type="button" class="switch on"><span></span></button>
        </li>
        <li>
          <span>SMS alerts for status updates</span>
          <button type="button" class="switch"><span></span></button>
        </li>
        <li>
          <span>Daily summary reports</span>
          <button type="button" class="switch on"><span></span></button>
        </li>
        <li>
          <span>Agent assignment notifications</span>
          <button type="button" class="switch on"><span></span></button>
        </li>
      </ul>
    </article>

    <article class="panel settings-panel">
      <h2>Claim Processing</h2>
      <label class="field">
        <span>Auto-assign threshold ($)</span>
        <input type="number" value="5000" />
      </label>
      <label class="field">
        <span>Review deadline (days)</span>
        <input type="number" value="7" />
      </label>
      <ul class="setting-list">
        <li>
          <span>Auto-assignment</span>
          <button type="button" class="switch on"><span></span></button>
        </li>
      </ul>
      <button type="button" class="primary-btn">Save Changes</button>
    </article>
  </section>
</template>
