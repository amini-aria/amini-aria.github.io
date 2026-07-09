# ARIA CV

من آریا امینی (Aria Amini) هستم و این، قالب سایت شخصی و رزومه‌ای است که برای خودم ساختم و اسمش رو گذاشتم **ARIA CV**. این فایل رو نوشتم تا اگه یه روز خودم یا یه نفر دیگه خواست این قالب رو دوباره بفهمه یا ازش استفاده کنه، بدونه دقیقاً چی کجاست و چرا اینطوری ساخته شده.

## این قالب چیه

یک سایت شخصی و رزومه‌ی دوزبانه (انگلیسی/فارسی) است که کاملاً استاتیک است — یعنی نه فریم‌ورک دارد، نه مرحله‌ی build، فقط HTML و CSS و کمی جاوااسکریپت خام. هویت بصری‌اش از دنیای زمین‌شناسی و فسیل‌ها می‌آید: یک پالت رنگی خاکی و کرم‌رنگ، فسیل‌های خطی (تریلوبیت، آمونیت، سرخس) که به‌آرامی در پس‌زمینه حرکت می‌کنند، و یک کارت هیرو شیشه‌ای که رنگش با حرکت موس کمی تغییر می‌کند.

## چرا استاتیک، بدون build

قبل از این نسخه چند بار سراغ فریم‌ورک‌های سنگین‌تر (Hugo، Jekyll) رفتم و هر بار توی مرحله‌ی deploy روی GitHub Pages گیر کردم. نتیجه این شد که ساده‌ترین راه، مطمئن‌ترین راه است: فایل‌های HTML خام که مستقیم با گزینه‌ی «Deploy from a branch» در تنظیمات Pages منتشر می‌شوند، بدون هیچ workflow یا وابستگی بیرونی.

## ساختار فایل‌ها

```
index.html                 صفحه اصلی، انگلیسی
resume/index.html          صفحه رزومه کامل، انگلیسی
publications/index.html    صفحه مقالات/پژوهش/تألیف‌ها، انگلیسی (خودکار از رزومه پر می‌شود)

fa/index.html               صفحه اصلی، فارسی
fa/resume/index.html        صفحه رزومه کامل، فارسی
fa/publications/index.html  صفحه مقالات/پژوهش/تألیف‌ها، فارسی

assets/css/style.css        تمام استایل‌ها، توکن‌های رنگی، انیمیشن‌ها
assets/js/app.js            منو، اسکرول، تاریخ خودکار، مکانیزم آینه‌کردن رزومه
assets/img/                 وکتورها و تصویر پروفایل
assets/files/                نسخه‌های PDF رزومه
```

## زبان و جهت متن

انگلیسی زبان پیش‌فرض و در ریشه‌ی سایت است؛ فارسی کاملاً راست‌چین و زیر مسیر `/fa/` قرار دارد. جهت‌دهی با `dir="ltr"` یا `dir="rtl"` روی تگ `<html>` هر صفحه مشخص می‌شود و بقیه‌ی چیدمان (فاصله‌ها، ترازها) با CSS logical properties (مثل `padding-inline-start` به‌جای `padding-left`) خودش را با آن هماهنگ می‌کند. نکته‌ی مهم: فونت‌های فارسی هرگز نباید `letter-spacing` یا `text-transform: uppercase` بگیرند — این دو باعث از‌هم‌گسیختگی حروف در کلمات فارسی می‌شوند.

## چیدمان رنگ و فونت

```css
:root {
  --cream: #F1E7D5;      /* پس‌زمینه اصلی */
  --umber: #7A4B2E;      /* رنگ اصلی، قهوه‌ای خاکی */
  --clay: #B5623B;       /* رنگ دوم، رس/سفال */
  --olive: #6E7A4F;       /* رنگ سوم، زیتونی */
  --sand-gold: #C9A227;   /* لهجه‌ی طلایی، مصرف کم */
}
```
فونت انگلیسی ترکیب Fraunces (برای عنوان‌ها) و Inter (برای متن) است؛ فونت فارسی Vazirmatn.

## رزومه: یک منبع، چند نمایش

صفحه‌ی رزومه یک HTML ساده و پشت‌سرهم است — هر بخش داخل یک `<section class="resume__block">` با یک عنوان (`resume__block-title`) و چند مورد (`resume__entry`). برای ویرایش، کافی است متن را مستقیم عوض کنید:

```html
<section class="resume__block">
  <p class="resume__block-title">Section Title</p>
  <div class="resume__entry">
    <div class="resume__entry-head">
      <span class="resume__entry-role">Role or Title</span>
      <span class="resume__entry-period">Start – End</span>
    </div>
    <p class="resume__entry-org">Organization Name</p>
  </div>
</section>
```

بخش‌هایی که هنوز محتوای واقعی ندارند به‌جای متن ساختگی، یک نسخه‌ی خالیِ همین قالب را با کلاس `resume__entry--placeholder` نشان می‌دهند (کادر خط‌چین با فیلدهای داخل کروشه)، تا وقتی محتوا آماده شد، چیدمان از قبل آماده باشد.

صفحه‌ی «مقاله، پژوهش و تألیف‌ها» هیچ محتوای مستقلی ندارد؛ در لحظه‌ی بارگذاری، با جاوااسکریپت صفحه‌ی رزومه را فچ می‌کند و فقط بخش‌های مشخصی (مثلاً Research Experience، Publications، Books، Conferences) را از آن کپی می‌کند. یعنی یک متن را فقط یک‌بار در رزومه می‌نویسید و همان‌جا هم می‌ماند.

## تاریخ «آخرین ویرایش»

بالای صفحه‌ی رزومه، تاریخ آخرین commit مربوط به همان فایل از GitHub API خوانده می‌شود (بدون نیاز به build). برای فارسی، تاریخ میلادی با یک تابع کوچک به شمسی تبدیل می‌شود.

## دو نسخه PDF

فایل‌های `assets/files/Aria-CV-En.pdf` و `Aria-CV-Fa.pdf` جدا از طراحی سایت ساخته شده‌اند: سیاه‌وسفید، فشرده، مناسب چاپ و سیستم‌های ATS. این‌ها به‌صورت خودکار از HTML سایت تولید نمی‌شوند — هر وقت محتوای رزومه به‌طور محسوس تغییر کرد، باید این دو فایل هم دستی (یا با کمک ابزار مولد PDF) به‌روزرسانی شوند.

## یک ویژگی آزمایشی

در بالای هر صفحه یک آیکون فسیل کوچک هست که بین صفحه‌ها فرق می‌کند (تریلوبیت در صفحه اصلی، آمونیت در رزومه، سرخس در انتشارات). با قانون CSS به اسم `@view-transition`، مرورگرهایی که از Cross-Document View Transitions پشتیبانی می‌کنند (فعلاً عمدتاً مرورگرهای مبتنی بر Chromium)، هنگام رفتن از صفحه‌ای به صفحه‌ی دیگر این آیکون را با یک ترانزیشن نرم به شکل جدید تبدیل می‌کنند. در مرورگرهایی که این ویژگی را ندارند، فقط یک جابه‌جایی معمولی اتفاق می‌افتد — هیچ‌چیز خراب نمی‌شود.

## انتشار

```
Settings → Pages → Build and deployment → Source → "Deploy from a branch"
Branch: main   —   Folder: / (root)
```
همین. بدون workflow، بدون build، بدون وابستگی بیرونی.

---
---

# ARIA CV (English)

I am Aria Amini, and this is the personal-site-and-résumé template I built for myself, named **ARIA CV**. I'm writing this file so that if I — or anyone else — ever need to understand this template again, it's clear what lives where and why it was built this way.

## What this is

A bilingual (English/Persian) personal site and résumé that is fully static — no framework, no build step, just plain HTML, CSS, and a little vanilla JavaScript. Its visual identity comes from geology and fossils: an earthy, cream-and-brown palette, faint line-art fossils (trilobite, ammonite, fern) drifting slowly in the background, and a glass hero card whose tint shifts gently as the mouse moves across it.

## Why static, no build

Before this version, I went through a couple of heavier frameworks (Hugo, Jekyll) and got stuck at the GitHub Pages deployment step each time. The conclusion: the simplest approach is also the most reliable one — plain HTML files published directly through the "Deploy from a branch" option in Pages settings, with no workflow and no external dependency.

## File structure

```
index.html                 Home page, English
resume/index.html          Full résumé, English
publications/index.html    Papers/research/publications page, English (auto-filled from the résumé)

fa/index.html               Home page, Persian
fa/resume/index.html        Full résumé, Persian
fa/publications/index.html  Papers/research/publications page, Persian

assets/css/style.css        All styling, color tokens, animations
assets/js/app.js            Menu, scroll behavior, the auto-date logic, the résumé-mirroring mechanism
assets/img/                 Vectors and the profile photo
assets/files/                The downloadable résumé PDFs
```

## Language and text direction

English is the default language and lives at the site root; Persian is fully right-to-left and lives under `/fa/`. Direction is set once via `dir="ltr"` or `dir="rtl"` on each page's `<html>` tag, and the rest of the layout (spacing, alignment) follows automatically through CSS logical properties (e.g. `padding-inline-start` instead of `padding-left`). One rule worth remembering: Persian text must never get `letter-spacing` or `text-transform: uppercase` — both break how the letters join within a word.

## Color and type system

```css
:root {
  --cream: #F1E7D5;      /* primary background */
  --umber: #7A4B2E;      /* primary accent, earthy brown */
  --clay: #B5623B;       /* secondary accent, terracotta */
  --olive: #6E7A4F;       /* tertiary accent, olive */
  --sand-gold: #C9A227;   /* gold highlight, used sparingly */
}
```
The English typeface pairs Fraunces (headings) with Inter (body text); the Persian typeface is Vazirmatn.

## Résumé: one source, several views

The résumé page is plain, sequential HTML — each section sits in a `<section class="resume__block">` with a title (`resume__block-title`) and one or more entries (`resume__entry`). To edit, just change the text directly:

```html
<section class="resume__block">
  <p class="resume__block-title">Section Title</p>
  <div class="resume__entry">
    <div class="resume__entry-head">
      <span class="resume__entry-role">Role or Title</span>
      <span class="resume__entry-period">Start – End</span>
    </div>
    <p class="resume__entry-org">Organization Name</p>
  </div>
</section>
```

Sections that don't have real content yet show an empty version of the same layout, marked with the `resume__entry--placeholder` class (a dashed box with bracketed fields), so the layout is already in place once the content is ready.

The "Papers, Research & Publications" page has no content of its own. On load, it fetches the résumé page with JavaScript and clones only a few specific sections (e.g. Research Experience, Publications, Books, Conferences) out of it. So each piece of text is written once, on the résumé page, and stays there.

## The "last updated" date

At the top of the résumé page, the date of the most recent commit touching that file is read live from the GitHub API — no build step required. For the Persian page, the Gregorian date is converted to the Jalali calendar with a small local function.

## Two PDF versions

`assets/files/Aria-CV-En.pdf` and `Aria-CV-Fa.pdf` are built separately from the website's design: black and white, compact, print- and ATS-friendly. They are not generated automatically from the site's HTML — whenever the résumé content changes meaningfully, these two files need to be regenerated by hand (or with a PDF-generation tool).

## One experimental touch

Every page has a small fossil icon at the top that differs by page (a trilobite on the home page, an ammonite on the résumé, a fern on publications). Using the CSS `@view-transition` rule, browsers that support Cross-Document View Transitions (currently mostly Chromium-based browsers) will morph this icon smoothly into its new shape when navigating between pages. Browsers without support just swap it instantly — nothing breaks.

## Deploying

```
Settings → Pages → Build and deployment → Source → "Deploy from a branch"
Branch: main   —   Folder: / (root)
```
That's it. No workflow, no build, no external dependency.
