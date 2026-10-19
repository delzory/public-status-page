const { defineConfig, devices } = require('@playwright/test');
const path = require('node:path');

module.exports = defineConfig({
  testDir: './tests/browser',
  retries: 0,
  reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:8765' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['Pixel 7'] } },
  ],
  webServer: {
    cwd: path.resolve(__dirname, '../..'),
    command: 'python3 -m http.server 8765 --bind 127.0.0.1 --directory public',
    url: 'http://127.0.0.1:8765',
    reuseExistingServer: false,
  },
});
