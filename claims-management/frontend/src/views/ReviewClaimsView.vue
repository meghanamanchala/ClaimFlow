<template>
  <section>
    <header class="page-head">
      <h1>Review Claim</h1>
      <p>Review details and make a decision on this claim</p>
    </header>

    <div class="agent-review-grid">
      <div>
        <article class="panel">
          <div class="review-card-header">
            <h2>CLM-2024-001</h2>
            <span class="badge badge-review">Under Review</span>
          </div>

          <div class="review-info-grid">
            <div>
              <p class="review-label">Type</p>
              <p>Auto Insurance</p>
            </div>
            <div>
              <p class="review-label">Policy #</p>
              <p>POL-2024-8834</p>
            </div>
            <div>
              <p class="review-label">Incident Date</p>
              <p>Feb 28, 2026</p>
            </div>
            <div>
              <p class="review-label">Claimed Amount</p>
              <p>$4,500</p>
            </div>
          </div>

          <div>
            <p class="review-label">Description</p>
            <p>
              Rear-end collision at intersection. Other driver ran red light. Police report filed.
              Vehicle requires bumper and trunk repair.
            </p>
          </div>
        </article>

        <article class="panel claim-documents-panel">
          <h2>Attached Documents</h2>
          <ul class="document-items">
            <li>
              <span>Police Report.pdf</span>
              <button type="button" class="link-btn">View</button>
            </li>
            <li>
              <span>Damage Photos.jpg</span>
              <button type="button" class="link-btn">View</button>
            </li>
            <li>
              <span>Repair Estimate.pdf</span>
              <button type="button" class="link-btn">View</button>
            </li>
          </ul>
        </article>
      </div>

      <div class="review-side-stack">
        <article class="panel">
          <h2>Policyholder</h2>
          <div class="policyholder-mini-card">
            <div class="avatar-soft">SM</div>
            <div>
              <p class="policyholder-name">Sarah Mitchell</p>
              <p class="policyholder-email">sarah@example.com</p>
            </div>
          </div>
          <button type="button" class="ghost-btn full-width">Send Message</button>
        </article>

        <article class="panel">
          <h2>Claim Progress</h2>
          <ol class="progress-list">
            <li class="progress-item">
              <div class="progress-dot is-done"></div>
              <div>
                <p class="progress-title">Submitted</p>
                <p class="progress-date">Mar 2, 2026</p>
              </div>
            </li>
            <li class="progress-item">
              <div class="progress-dot is-done"></div>
              <div>
                <p class="progress-title">Documents Verified</p>
                <p class="progress-date">Mar 3, 2026</p>
              </div>
            </li>
            <li class="progress-item">
              <div class="progress-dot is-active"></div>
              <div>
                <p class="progress-title">Agent Review</p>
                <p class="progress-date">Mar 5, 2026</p>
              </div>
            </li>
            <li class="progress-item">
              <div class="progress-dot is-upcoming"></div>
              <div>
                <p class="progress-title">Decision</p>
                <p class="progress-date">Pending</p>
              </div>
            </li>
            <li class="progress-item">
              <div class="progress-dot is-upcoming"></div>
              <div>
                <p class="progress-title">Payment</p>
                <p class="progress-date">Pending</p>
              </div>
            </li>
          </ol>
        </article>

        <article class="panel">
          <h2>Decision</h2>
          <label class="field">
            <span>Notes</span>
            <textarea rows="4" placeholder="Add review notes..."></textarea>
          </label>
          <div class="decision-actions">
            <button type="button" class="danger-btn">Reject</button>
            <button type="button" class="primary-btn">Approve</button>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
