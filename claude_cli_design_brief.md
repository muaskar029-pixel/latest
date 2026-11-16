# Claude CLI Brief: Radova "Latest" — Editorial UI & Reusable Styling Architecture

## 1. Context & Objective
You are working on the **Radova "Latest"** static site (`latest/`, `templates/`, `assets/site.css`). Issues 1–4 are partially complete in the working tree. Your task is to **refine Issues 3 & 4** and **complete Issue 5** by implementing a cohesive, reusable **Editorial Split-Grid Design System** inspired by our visual references, while strictly adhering to our technical constraints.

## 2. Strict Technical & Accessibility Constraints
* **Zero Node/npm:** Pure static HTML, Pico CSS (`assets/pico.classless.min.css`), HTMX (`assets/htmx.min.js`), and Vanilla JS.
* **Zero Inline Code:** No `style="..."`, `<style>`, or inline JS in any HTML file. All styles must live in `assets/site.css`.
* **Lynx Text-Browser Compatibility (`lynx -dump -width=80`):**
  * DOM reading order must remain strictly logical from top to bottom.
  * Keep text separators (` · `) inside the HTML for Lynx readability, and hide them visually in CSS where grid/flex spacing replaces them.
  * Badges/statuses must always include explicit text (e.g., `Severity: High`, `Status: Cancelled`), never color alone.
* **Brand Tokens (`:root` in `assets/site.css`):**
  * Background Primary: Lavender `#F7F6FF`
  * Surface / Card Background: Pure White `#FFFFFF`
  * Text & Structural Borders: Navy `#0E0347` (use `rgba(14, 3, 71, 0.12)` for hairline architectural grid borders)
  * Accent / Interactive: Reds `#A10000` (primary), `#BB080B` (hover), `#DB000F` (badges/alerts)
  * Typography: **Lato** for Headings, **Roboto** for Body & Metadata.
  * Visual Style: Flat architectural editorial layout, zero drop-shadows (`box-shadow: none`), sharp 1px structural borders, generous whitespace.

---

## 3. Reusable CSS Architecture (`assets/site.css`)
Refactor and organize `assets/site.css` into reusable layout primitives and components so `templates/*.html` and `latest/**/*.html` share the exact same classes without duplication:

1. **`.editorial-header`**: Split hero header at the top of index/category pages (Left: Eyebrow label + `<h1>` Title; Right: Category description + optional primary action/feed link).
2. **`.tab-grid`**: Full-width architectural tab bar (`All Latest`, `Agenda`, `Article`, `News`, `Security`). Equal-width cells on desktop (`display: grid; grid-template-columns: repeat(5, 1fr)`), bordered by 1px solid hairline borders, with the active tab (`[aria-current="page"]`) highlighted via a `#FFFFFF` surface background, bold text, and a bottom `#A10000` accent bar.
3. **`.post-row`**: Reusable 2-column asymmetric split card for listings (`grid-template-columns: 1.2fr 0.8fr` on desktop, stacked `1fr` on `<768px`). Separated by 1px horizontal/vertical grid lines.
4. **`.single-split`**: Reusable layout for Single Post detail pages (`post.html`, `agenda.html`, `security.html`). Uses a 2-column editorial layout on desktop (`grid-template-columns: 320px 1fr` or `40% 60%`) where the left column holds sticky/structured context (Title, Metadata `<dl>`, Back link, CTA) and the right column holds the readable prose body (`max-width: 65ch`).
5. **`.meta-dl`**: Reusable styled `<dl>` component for Agenda and Security metadata boxes (clean key-value grid with 1px dividers).
6. **`.badge` & Modifiers (`.badge--type`, `.badge--severity-high`, `.badge--cancelled`, etc.)**: Pill/rectangular editorial tags meeting WCAG AA contrast (>= 4.5:1).

---

## 4. Page-by-Page Design Specifications

### A. Index & Category Listing Pages (`/latest/index.html`, `/latest/<type>/index.html`, `templates/listing.html`)
*(Inspired by the "Blog & Articles" bordered grid reference)*

1. **Page Header (`.editorial-header`):**
   * **Left Side:** Small bracketed eyebrow text (e.g., `[Radova Updates]` or `[Category: Security]`) above a bold `<h1>` (`Read Our Latest Updates` or category title).
   * **Right Side (aligned bottom-right on desktop):** A concise 1–2 sentence description of the feed, plus a subtle pill link to the Atom RSS feed (`/latest/feed.xml`).
2. **Category Navigation Bar (`.tab-grid`):**
   * Directly below the header, enclosed in a 1px bordered grid container.
   * Each tab is a full-cell clickable `<a href="...">` with generous vertical padding (`min-height: 52px`).
3. **Index Post List (`.post-grid` & `.post-row`):**
   * Enclose the list in a clean 1px outer border where items share internal 1px hairline borders (no floating cards, no shadows).
   * **Left Column of `.post-row` (Core Narrative):**
     * Top: Category badge (`.badge--type`) on `/latest/`, or Advisory ID / Agenda status on category pages.
     * Middle: `<h2>` Post Title link (24px–28px, wraps cleanly) + 2-line summary paragraph (`max-width: 60ch`).
     * Bottom: Metadata footer (`<time datetime="...">`, reading time for Articles) separated by ` · ` for Lynx.
   * **Right Column of `.post-row` (Structured Context Panel):**
     * Since Radova is text-first and avoids heavy stock photos, use the right column as a high-contrast architectural panel (`background: #FFFFFF` or subtle tint) displaying category-specific structured data:
       * **Article / News:** Large typographic tag list, author, and a clean `"Read Article →"` visual indicator.
       * **Agenda:** Prominent date/time block (`WIB / +07:00`), Location, and Status badge (`Scheduled` / `Cancelled`).
       * **Security:** Large monospace Advisory ID (`RSA-YYYY-NNN`), explicit Severity badge (`Severity: Critical/High/etc.`), Status, and Affected Versions summary.
4. **Agenda Index Specifics (`/latest/agenda/index.html`):**
   * Maintain two distinct semantic sections (`<h2>Upcoming Events</h2>` and `<h2>Past Events</h2>`), each utilizing the `.post-grid` layout.
5. **Pagination Bar:**
   * Full-width bordered bar at the bottom of the grid with `Previous` and `Next` links (`min-height: 52px`).

---

### B. Single Post Detail Pages (`templates/post.html`, `agenda.html`, `security.html` & `latest/<type>/sample-*/index.html`)
*(Inspired by the 2-column split editorial journal reference)*

1. **Split Editorial Layout (`.single-split`):**
   * **Left Column (Editorial Header & Metadata Panel):**
     * Breadcrumb / Back link (`← Back to Latest` or category).
     * Category eyebrow label + `<h1>` Post Title.
     * Standard `<head>` & visible metadata: `<meta name="radova:author">` (add `author` to metadata standard in `templates/README.md` and `post.html`), Publication Date (`<time>`), Reading Time, and Tags.
     * **For Agenda (`agenda.html`):** Render the `<dl class="meta-dl">` here (Start/End time in WIB, Location/Online link, Status badge) + prominent `"Register Now"` CTA button and `"Add to Calendar (.ics)"` link.
     * **For Security (`security.html`):** Render the `<dl class="meta-dl">` here (`Advisory ID`, `Severity`, `Status`, `Affected Versions`, `Patched Versions`, `CVE` links).
   * **Right Column (Prose & Content Body — `.editorial-prose`):**
     * Clean white surface (`#FFFFFF`) with generous internal padding and `max-width: 65ch` for optimal reading comfort.
     * **Drop-cap styling (Optional/CSS-only):** Apply a subtle editorial `::first-letter` style to the first paragraph of **Article** posts (like the reference image) using CSS only so Lynx stays unaffected.
     * **Typography & Elements:** Clear vertical rhythm for `<h2>`/`<h3>`, styled `<blockquote>` with a `#A10000` left border, and horizontally scrollable `<pre><code>` blocks (`overflow-x: auto; max-width: 100%`) so mobile viewports (375px) never scroll horizontally.
     * **For Security (`security.html`):** Strictly structure the right-column body into semantic sections: `Summary`, `Impact`, `Mitigation`, `Credits`, and `Timeline`.
2. **Post Footer Navigation:**
   * A 2-column bordered bar at the bottom of `<main>` linking to the **Previous Post** and **Next Post**.

---

## 5. Step-by-Step Execution Plan for Claude CLI

1. **Standardize Metadata (`templates/README.md`):**
   * Add `<meta name="radova:author" content="...">` to the metadata specification for Articles/News to resolve the open question from `LAPORAN.md`.
2. **Update `assets/site.css`:**
   * Implement the reusable classes (`.editorial-header`, `.tab-grid`, `.post-grid`, `.post-row`, `.single-split`, `.meta-dl`, `.editorial-prose`, `.badge`).
   * Ensure responsive breakpoints (`@media (max-width: 768px)`) collapse all 2-column splits into a single vertical column with zero horizontal overflow at `375px`.
3. **Update Templates (`templates/listing.html`, `post.html`, `agenda.html`, `security.html`):**
   * Apply the new semantic, reusable HTML structure across all 4 templates.
4. **Propagate to Existing Pages (`latest/index.html`, `latest/<type>/index.html`, `latest/<type>/sample-*/index.html`):**
   * Update the main index, all 4 category indexes, and all 4 sample detail pages to match the updated templates.
5. **Verification Checks (Must Run Before Finishing):**
   * Verify zero inline `style=` or `<script>` tags across all `.html` files.
   * Verify no horizontal overflow at `375px`, `768px`, and `1280px`.
   * Verify WCAG AA contrast on all badges and text.
   * Test text-only reading order (simulate `lynx -dump` structure check) to confirm ` · ` separators and `<dl>` key-values read sequentially.