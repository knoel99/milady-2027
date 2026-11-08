import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
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
  const profil = mkdtempSync(join(tmpdir(), "navigateur-"));
  const browser = await chromium.launchPersistentContext(profil, {
    ...CHROME,
    viewport: { width: largeur, height: hauteur },
    deviceScaleFactor: 1,
  });
  const page = browser.pages()[0] ?? (await browser.newPage());
  await page.goto(url, { waitUntil: "load" });
  await page.waitForFunction(() => window.__scene);
  await page.evaluate(() => document.fonts.ready);
  return { browser, page };
}
