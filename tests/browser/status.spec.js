const { test, expect } = require('@playwright/test');

test('services render, category controls work, and details open', async ({ page, request }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  // External analytics/CMS services are not dependencies of this smoke test.
  await page.route('**/*', route => {
    const url = new URL(route.request().url());
    return url.hostname === '127.0.0.1' ? route.continue() : route.abort();
  });
  const response = await page.goto('/');
  expect(response.status()).toBe(200);
  const api = await (await request.get('/index.json')).json();
  await expect(page).toHaveTitle(api.title);
  await expect(page.locator('.component')).toHaveCount(api.systems.length);
  const categories = page.locator('.category--titled');
  for (const category of await categories.all()) {
    const header = category.locator('.category__head');
    const statuses = await category.locator('.component').evaluateAll(elements =>
      elements.map(element => element.dataset.status));
    const expected = ['down', 'disrupted', 'notice'].find(status => statuses.includes(status)) || 'ok';
    await expect(header).toHaveAttribute('data-status', expected);
    await expect(header.locator('.category-status')).not.toBeEmpty();
    const wasClosed = (await category.getAttribute('class')).includes('category--closed');
    await header.click();
    await expect(category).toHaveClass(wasClosed ? /category--open/ : /category--closed/);
    await header.click();
    await expect(category).toHaveClass(wasClosed ? /category--closed/ : /category--open/);
  }
  const links = await page.locator('.component > a').evaluateAll(elements =>
    elements.map(element => element.getAttribute('href')));
  for (const link of links) {
    const detail = await request.get(link);
    expect(detail.status(), `Service details ${link}`).toBe(200);
  }
  const firstCategory = categories.first();
  if ((await firstCategory.getAttribute('class')).includes('category--closed')) {
    await firstCategory.locator('.category__head').click();
  }
  await firstCategory.locator('.component > a').first().click();
  await expect(page).toHaveURL(/\/affected\//);
  expect(errors).toEqual([]);
});
