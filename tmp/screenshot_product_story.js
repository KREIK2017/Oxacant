const { chromium } = require("C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  });

  for (const [name, viewport] of Object.entries({
    desktop: { width: 1440, height: 1200 },
    mobile: { width: 390, height: 844 },
  })) {
    const page = await browser.newPage({ viewport });
    await page.goto("http://127.0.0.1:4174/#loesung", { waitUntil: "networkidle" });
    await page.locator("#loesung").scrollIntoViewIfNeeded();
    await page.screenshot({
      path: `tmp/product-story-${name}.png`,
      fullPage: false,
    });
    await page.locator("#loesung").screenshot({
      path: `tmp/product-story-${name}-full.png`,
    });
    const result = await page.locator("#loesung").evaluate((section) => ({
      sections: section.querySelectorAll(":scope > section").length,
      benefits: section.querySelectorAll(".product-benefits li").length,
      width: section.getBoundingClientRect().width,
      scrollWidth: document.documentElement.scrollWidth,
      viewportWidth: window.innerWidth,
    }));
    console.log(name, JSON.stringify(result));
    await page.close();
  }

  await browser.close();
})();
