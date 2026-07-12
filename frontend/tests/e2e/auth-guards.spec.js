import { expect, test } from '@playwright/test';
import { attachApiMocks, seedAuth } from './helpers/mockApi';

const APP_URL = 'http://localhost:5173';

test('unauthenticated user is redirected to login for protected route', async ({ page }) => {
  await attachApiMocks(page, 'policyholder');
  await page.goto(`${APP_URL}/dashboard`);
  await expect(page).toHaveURL(/\/login$/);
  await expect(page.getByRole('heading', { name: /welcome back/i })).toBeVisible();
});

test('admin cannot open policyholder route and is redirected to admin dashboard', async ({ page }) => {
  await attachApiMocks(page, 'admin');
  await seedAuth(page, 'admin');
  await page.goto(`${APP_URL}/dashboard`);
  await expect(page).toHaveURL(/\/admin\/dashboard$/);
  await expect(page.getByRole('heading', { name: /admin dashboard/i })).toBeVisible();
});

test('agent cannot open admin route and is redirected to agent dashboard', async ({ page }) => {
  await attachApiMocks(page, 'agent');
  await seedAuth(page, 'agent');
  await page.goto(`${APP_URL}/admin/dashboard`);
  await expect(page).toHaveURL(/\/agent\/dashboard$/);
  await expect(page.getByRole('heading', { name: /agent dashboard/i })).toBeVisible();
});

test('unknown route falls back to role home page', async ({ page }) => {
  await attachApiMocks(page, 'policyholder');
  await seedAuth(page, 'policyholder');
  await page.goto(`${APP_URL}/this-route-does-not-exist`);
  await expect(page).toHaveURL(/\/dashboard$/);
});
