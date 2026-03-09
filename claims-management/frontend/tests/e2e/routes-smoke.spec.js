import { expect, test } from '@playwright/test';
import { attachApiMocks, seedAuth } from './helpers/mockApi';

const APP_URL = 'http://localhost:5173';

const ROUTE_MATRIX = [
  {
    role: 'policyholder',
    checks: [
      { path: '/dashboard', heading: 'Welcome back' },
      { path: '/submit-claim', heading: 'Submit New Claim' },
      { path: '/my-claims', heading: 'My Claims' },
      { path: '/documents', heading: 'Documents' },
      { path: '/claim-history', heading: 'Claim History' },
      { path: '/profile', heading: 'Edit Profile' },
      { path: '/notifications', heading: 'Notifications' }
    ]
  },
  {
    role: 'agent',
    checks: [
      { path: '/agent/dashboard', heading: 'Agent Dashboard' },
      { path: '/agent/assigned-claims', heading: 'Assigned Claims' },
      { path: '/agent/review-claims', heading: 'Review Claim' },
      { path: '/agent/messages', heading: 'Messages' },
      { path: '/agent/profile', heading: 'Edit Profile' },
      { path: '/agent/notifications', heading: 'Notifications' }
    ]
  },
  {
    role: 'admin',
    checks: [
      { path: '/admin/dashboard', heading: 'Admin Dashboard' },
      { path: '/admin/all-claims', heading: 'All Claims' },
      { path: '/admin/user-management', heading: 'User Management' },
      { path: '/admin/analytics', heading: 'Analytics' },
      { path: '/admin/permissions', heading: 'Permissions' },
      { path: '/admin/settings', heading: 'Settings' },
      { path: '/admin/profile', heading: 'Edit Profile' },
      { path: '/admin/notifications', heading: 'Notifications' }
    ]
  }
];

for (const group of ROUTE_MATRIX) {
  test.describe(`${group.role} route smoke`, () => {
    test.beforeEach(async ({ page }) => {
      await attachApiMocks(page, group.role);
      await seedAuth(page, group.role);
    });

    for (const check of group.checks) {
      test(`${check.path} renders`, async ({ page }) => {
        await page.goto(`${APP_URL}${check.path}`);
        await expect(page.getByRole('heading', { level: 1, name: new RegExp(check.heading, 'i') })).toBeVisible();
      });
    }
  });
}
