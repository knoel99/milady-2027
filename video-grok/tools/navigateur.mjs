import { chromium } from "playwright";

export const CHROME = {
  channel: "chrome",
  headless: true,
  args: [
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-lcd-text",
    "--disable-font-subpixel-positioning",
    "--font-render-hinting=none",
    "--force-color-profile=srgb",
  ],
};

export async function ouvrir(url, { largeur = 1920, hauteur = 1080 } = {}) {
  const browser = await chromium.launch(CHROME);
  const page = await browser.newPage({
    viewport: { width: largeur, height: hauteur },
    deviceScaleFactor: 1,
  });
  await page.goto(url, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  return { browser, page };
}
