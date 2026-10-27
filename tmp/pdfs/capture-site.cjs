const { chromium } = require('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const { pathToFileURL } = require('node:url');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const localPage = pathToFileURL('D:/Рабочий стол/projeckts/!AlpenPharma/Oxacant/dist/index.html').href;
  await page.goto(localPage, {
    waitUntil: 'load',
    timeout: 60000,
  });
  await page.waitForTimeout(4000);
  await page.screenshot({
    path: 'D:/Рабочий стол/projeckts/!AlpenPharma/Oxacant/tmp/pdfs/oxacant-fullpage.png',
    fullPage: true,
  });
  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
