// Renders resume/index.html and fa/resume/index.html — served locally,
// exactly as GitHub Pages would serve them — to the two downloadable PDFs
// in assets/files/. This keeps the PDFs permanently in sync with the site:
// whenever the resume page content changes, the next push regenerates them.
const puppeteer = require("puppeteer");
const http = require("http");
const handler = require("serve-handler");
const path = require("path");

const ROOT = path.join(__dirname, "..", "..");
const PORT = 8080;

const PAGES = [
  { url: "resume/", out: "assets/files/Aria-CV-En.pdf" },
  { url: "fa/resume/", out: "assets/files/Aria-CV-Fa.pdf" },
];

async function main() {
  const server = http.createServer((req, res) =>
    serveHandlerSafe(req, res, { public: ROOT, cleanUrls: true })
  );
  await new Promise((resolve) => server.listen(PORT, resolve));

  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  for (const { url, out } of PAGES) {
    const page = await browser.newPage();
    await page.goto(`http://localhost:${PORT}/${url}`, {
      waitUntil: "networkidle0",
    });
    await page.emulateMediaType("print");
    await page.pdf({
      path: path.join(ROOT, out),
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
    });
    await page.close();
    console.log("Wrote", out);
  }

  await browser.close();
  server.close();
}

function serveHandlerSafe(req, res, opts) {
  return handler(req, res, opts);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
