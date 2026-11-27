# RADOVA LATEST — EDITORIAL REDESIGN SPECIFICATION (`DESIGN.md`)

**Referensi Visual & Struktur:**
1. **Reuters Homepage (`https://www.reuters.com/`)** & screenshot referensi (`Screenshot 2026-11-26 at 00-02-25 Reuters Breaking International News & Views.png`).
2. **Global System & Guardrails:** [DESIGN.md](../DESIGN.md) (Single Source of Truth Radova Linux) dan [AGENTS.md](../AGENTS.md) (Pure Vanilla stack, Lighthouse 100/100/100/100, TBT = 0 ms, CLS = 0).

Dokumen ini menjadi cetak biru redesign seluruh halaman di repositori `latest` (`index.html`, `news/`, `article/`, `agenda/`, `security/`, `404.html`, serta varian `/id/` dan `/ar/`) agar mengadopsi **bahasa desain newsroom editorial ala Reuters**—padat informasi, tajam, *card-less* dengan garis pemisah *hairline* `1px`, dan hierarki tipografi yang mudah dipindai—tanpa melanggar identitas visual, token warna, atau standar performa Radova Linux.

---

## 1. Filosofi Desain: Reuters Wire-Service × Radova Linux

| Dimensi | Pendekatan Lama (`latest` saat ini) | Target Redesign (Reuters Editorial Pattern) |
|---|---|---|
| **Struktur Permukaan** | *Rounded hero split* + kartu besar ber-shadow (`post-card`) | **Flat Editorial Wire:** permukaan polos (`#FFFFFF` Light / `#0B0711` Dark), tanpa `box-shadow` berat, dipisahkan oleh **hairline rule `1px solid`** |
| **Radius Sudut** | `16px–20px` di semua kartu | **`2px–4px` (atau `0px`)** untuk thumbnail berita & kontainer editorial; pertahankan `16px–999px` hanya pada kontrol global (`.btn-navy`, `.btn-lang`, `.btn-theme`, pill filter) |
| **Kepadatan Konten** | 1 hero + 4 kartu simetris | **Hierarki Bertingkat:** Ticker strip → Lead Story asimetris → 4-kolom Sub-headlines → 4-kolom Thumbnail Grid → 65/35 Feature + Wire Rail → 4-kolom Category Matrix → Dark Showcase Band |
| **Keterbacaan Cepat** | Judul panjang dalam box tertutup | **Kicker + Headline + Deck + Timestamp** (`Kicker >` aksen merah, headline `Lato`, ringkasan singkat `Roboto Variable`, timestamp `ui-monospace`) |
| **Global Shell** | Header & footer Radova | **Wajib Dipertahankan 100% Identik** dengan Homepage (`.site-header` `px`-locked, `.site-footer` `#6D0000` Light / navy gradient Dark) |

> **Aturan Keras:** Jangan meniru iklan banner atas, widget saham eksternal, paywall, atau font berbayar Reuters (`Knowledge`/`Freight`). Seluruh komponen dibangun dengan HTML statis, Vanilla CSS, dan Vanilla JS murni.

---

## 2. Color System & Semantic Tokens (`latest`)

Mengikuti palet [DESIGN.md](../DESIGN.md) dengan penyesuaian kontras editorial Reuters (Light mode dominan putih bersih agar *hairline* dan foto menonjol; Dark mode `#0B0711` dengan surface `#150B52` untuk *showcase* / panel).

| Role Token | Light Mode | Dark Mode (`:root[data-theme="dark"]`) | Penggunaan di `latest` |
|---|---|---|---|
| `--surface-page` | `#FFFFFF` | `#0B0711` | Kanvas utama halaman berita |
| `--surface-subtle` | `#F7F6FF` | `#150B52` | Strip status/ticker, kotak search, panel ringkasan |
| `--surface-showcase` | `#0E0347` | `#150B52` | Band khusus **Top Briefs / Featured Media** (kontras tinggi ala *Top Video News* Reuters) |
| `--text-primary` | `#0E0347` | `#FFFFFF` | Headline utama, judul artikel, teks isi |
| `--text-body` | `#0E0347` (`--text-primary`) / `#5B5A78` (`--text-muted` untuk excerpt ringan) | `#FFFFFF` / `#C4C0D4` (`--text-muted`) | Ringkasan (*deck*) dan paragraf artikel |
| `--text-muted` | `#5B5A78` | `#C4C0D4` | Timestamp (`2 hr ago`), caption foto, metadata kategori (`>= 4.5:1`) |
| `--text-kicker` | `#A10000` | `#FF6B74` | Label kategori (`News >`, `Security >`), status breaking/advisory |
| `--hairline` | `rgba(14, 3, 71, 0.12)` (`--border-card`) | `rgba(196, 192, 212, 0.18)` (`--border-line`) | Garis pemisah horizontal & vertikal `1px solid` antar modul & kolom |
| `--hairline-strong` | `#0E0347` | `rgba(255, 255, 255, 0.35)` | Garis atas pemisah section utama (`border-top: 2px solid` atau `1px solid`) |

---

## 3. Tipografi & Skala Editorial

Tetap menggunakan font lokal `.woff2` (`assets/css/fonts.css` dimuat via `loader.js`, tanpa preload font):
- **Headline & Kicker (`--font-heading`):** `"Lato", system-ui, -apple-system, sans-serif` (`700`, `900`)
- **Deck, Link Navigasi Kategori & Isi (`--font-body`):** `"Roboto Variable", system-ui, -apple-system, sans-serif` (`400`, `500`, `700`)
- **Timestamp, Advisory ID & Ticker (`--font-mono`):** `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`

### Skala Tipe Khusus `latest` (Desktop → Mobile)
| Elemen | Font & Weight | Ukuran | Line-Height / Tracking | Catatan |
|---|---|---|---|---|
| **Lead Story `H1`** | `Lato` `900` | `clamp(1.75rem, 3.2vw, 2.5rem)` (`28px–40px`) | `1.12` / `-0.025em` | Lebih rapat & editorial daripada hero marketing Homepage (`56px`) |
| **Section Header (`H2`)** | `Lato` `900` | `1.125rem–1.25rem` (`18px–20px`) | `1.2` / `-0.01em` | Disertai chevron `›` atau panah SVG lokal |
| **Feature Headline (`H2`/`H3`)** | `Lato` `700` | `1.35rem–1.65rem` (`22px–26px`) | `1.18` / `-0.015em` | Untuk *Asymmetric Feature* (Section 4) |
| **Grid / Column Headline (`H3`)** | `Lato` `700` | `1rem–1.0625rem` (`16px–17px`) | `1.28` | Maksimal 3 baris agar ritme kolom rata |
| **Wire / Rail Headline** | `Lato` `700` | `0.9375rem` (`15px`) | `1.3` | Untuk daftar teks kanan & strip 4 kolom |
| **Deck / Excerpt** | `Roboto Variable` `400` | `0.9375rem` (`15px`) | `1.5` | Maksimal 2–3 baris di bawah `H1` / feature |
| **Category Kicker** | `Roboto Variable` `700` | `0.75rem` (`12px`) | `1.2` / `0.02em` | Warna `--text-kicker`, tanpa background pill berat |
| **Timestamp / Meta** | `ui-monospace` `400` | `0.75rem` (`12px`) | `1.3` | Format relatif/ISO (`2026-11-26` / `Updated 2h ago`) |

---

## 4. Arsitektur Layout Homepage `latest/index.html` (Section-by-Section)

Mengikuti alur visual dari screenshot referensi Reuters, seluruh `<main>` berada di dalam sistem container terpadu (`--container-max`: `510px` / `700px` / `950px` / `1200px` / `1450px`):

### Section 0: Status Ticker & Category Sub-Nav Strip
- **Inspirasi Reuters:** Baris kategori + strip ticker di bawah header utama.
- **Implementasi Radova:**
  1. **Category Filter Bar (`nav.tab-grid`):** Baris link horizontal bersih (`All`, `News`, `Articles`, `Agenda`, `Security`) + form pencarian ringkas (`.post-search`) sejajar di kanan pada desktop (`border-bottom: 1px solid var(--hairline)`).
  2. **Status Wire Strip (`.wire-ticker`):** Strip tipis (`padding-block: 8px`, `border-bottom: 1px solid var(--hairline)`) berisi 4–5 item status ringkas (mis. `Channel: Stable`, `Advisories: 0 Critical`, `Latest Release: ...`, `Archive Sync: OK`) dengan titik indikator status (`6px` bulat). *Zero JS marquee*, scroll horizontal halus di mobile.

### Section 1: Hero Lead Package + 4-Column Sub-Headline Strip
- **Inspirasi Reuters:** *Top Lead* (`Trump proposes raising tariffs...`) + strip 4 berita singkat di bawahnya.
- **Grid Desktop (`>= 1024px`):**
  - **Baris Atas (Asymmetric 12-Col Grid, `gap: 24px`):**
    - **Kolom Kiri (5 col / ~42%):** Kicker (`News ›`), `<h1>` Lead Story, deck 2–3 kalimat, timestamp + author/source tag.
    - **Kolom Kanan (7 col / ~58%):** Visual utama `16:9` (`.hero-media` deferred placeholder sesuai `AGENTS.md` §8.6, `border-radius: 4px`, `overflow: hidden`) + caption `12px` di bawah gambar.
  - **Baris Bawah (`border-top: 1px solid var(--hairline)`, `padding-top: 16px`):**
    - **4-Column Wire Strip (`repeat(4, 1fr)`):** 4 berita sekunder *text-only* (kicker + headline `15px` + timestamp), dipisahkan **garis vertikal `1px solid var(--hairline)`** di desktop (`gap: 20px`). Mobile: 1 kolom stack dengan garis horizontal.

### Section 2: "Top Stories" — 4-Column Visual Grid
- **Inspirasi Reuters:** *Other Top Stories* (4 thumbnail sejajar dengan gambar `16:9` di atas teks).
- **Struktur:**
  - Header section: `border-top: 2px solid var(--hairline-strong)`, judul `Top Stories ›` (`H2`).
  - Grid `4 kolom` (`>= 1024px`) → `2 kolom` (`>= 576px`) → `1 kolom` (`< 576px`), `gap: 20px`.
  - Tiap item (`<article class="wire-card">`): Gambar `16:9` (`width`/`height` eksplisit, `loading="lazy"`, `border-radius: 4px`), kicker kategori, headline `16px–17px` `Lato 700`, timestamp. **Tanpa background card, border, atau shadow.**

### Section 3: Asymmetric Feature + Right Wire Rail (65% / 35%)
- **Inspirasi Reuters:** Blok *World >* (foto besar di kiri + 3 berita teks di kanan + 1 kotak newsletter/briefing).
- **Grid Desktop (`>= 1024px`):** `grid-template-columns: minmax(0, 1.8fr) minmax(0, 1fr); gap: 28px;`.
  - **Kiri (Feature Story):** Header `Security & Advisories ›`, headline `24px`, deck singkat, gambar `16:9` lebar penuh kolom + caption.
  - **Kanan (Wire Rail):** 3–4 item daftar teks dipisah `border-bottom: 1px solid var(--hairline)`, diikuti 1 kotak **Notice / Policy Box** (`background: var(--surface-subtle)`, `border: 1px solid var(--hairline)`, `padding: 16px`, mis. tautan ke `security/policy/` atau feed).

### Section 4: 4-Column Category Matrix (`News › | Articles › | Agenda › | Security ›`)
- **Inspirasi Reuters:** Blok 4 kolom sejajar (*Technology | Gran World | Markets | Media*) dengan garis vertikal tipis di antara kolom.
- **Struktur per Kolom:**
  1. Header kolom (`Category ›`) dengan link ke subhalaman masing-masing.
  2. 1 **Lead Item** dengan thumbnail `16:9` + headline + timestamp.
  3. Garis pemisah `1px solid var(--hairline)`.
  4. 1–2 **Text-Only Items** (headline + timestamp).
  - Antar kolom dipisahkan `border-inline-start: 1px solid var(--hairline)` + `padding-inline-start: 20px` pada `>= 1024px`.

### Section 5: Dark Showcase Band ("Featured Briefs / Media")
- **Inspirasi Reuters:** Blok latar gelap (*Top Video News*) yang memecah ritme halaman putih sebelum bagian bawah.
- **Struktur:**
  - Background `var(--surface-showcase)` (`#0E0347` Light / `#150B52` Dark), teks `#FFFFFF`, border-radius `0` (full-bleed atau selebar container dengan padding `32px 24px`).
  - **Kiri (7 col):** Visual utama `16:9` + label kategori merah (`--red-600`) + headline putih `24px` + deck `rgba(255,255,255,0.85)`.
  - **Kanan (5 col):** Daftar `Up Next` berisi 4–5 item ringkas (judul + thumbnail kecil `80x45` di kanan, dipisah garis `rgba(255,255,255,0.16)`) + tombol outline `See all ›`.

### Section 6: "In Case You Missed It" (4-Col Archive Strip) & Editorial Notes
- **Inspirasi Reuters:** Baris 4 kartu arsip ringan di bagian bawah sebelum footer.
- **Struktur:** `4 kolom` thumbnail `16:9` untuk artikel/agenda pilihan lama agar halaman terasa kaya tanpa terasa berat.

---

## 5. Pola Subhalaman (`news/`, `article/`, `agenda/`, `security/`, `404.html`)

| Halaman | Struktur Editorial |
|---|---|
| **Category Index (`news/`, `article/`, `agenda/`, `security/`)** | Header kategori (`H1` + deskripsi 1 baris + `border-bottom: 2px solid var(--hairline-strong)`), 1 Lead Story asimetris di atas, lalu daftar artikel vertikal dengan thumbnail `16:9` di kiri (`220px`) dan judul + deck + timestamp di kanan, dipisah `1px solid var(--hairline)`. |
| **Detail Article (`news/*/`, `article/*/`)** | Layout baca fokus ala Reuters article: `max-width: 72ch` terpusat, kicker kategori di atas `H1`, sub-judul/deck, *byline* + `<time>` + tombol share/copy link minimal, gambar `16:9` dengan caption di bawahnya, lalu isi artikel `17px–18px` (`line-height: 1.68`) + sidebar kanan opsional `Related Stories` (`border-left: 1px solid var(--hairline)`). |
| **Security Policy (`security/policy/`)** | Pertahankan struktur dokumentasi/tabel yang jelas dengan *hairline table* (`1px solid var(--hairline)`), badge status monospace (`CVE`/`Advisory ID`), dan navigasi jangkar. |
| **404 Page (`404.html`)** | Tetap ringkas sesuai `AGENTS.md` §8.3 (tanpa CSS hero/grid yang tidak dipakai di halaman 404). |

---

## 6. Standar Performa, Atomic CSS & Interaktivitas

1. **CSS Architecture (`AGENTS.md` §3 & §8):**
   - Inline critical `<style>` hanya memuat token, reset minimal (~20 baris, **0% Pico CSS**), `.site-header` (`px`-locked), ticker strip, dan Section 1 (Lead Story + 4-col sub-headlines) agar *above-the-fold* langsung ter-render dengan `CLS = 0`.
   - Seluruh section di bawah lipatan (Section 2–6) dimuat via `assets/css/latest-below.css` non-blocking (`media="print" onload="this.media='all'"` + fallback `<noscript>`).
   - Tetap generate `assets/css/latest.bundle.css` dengan urutan: `tokens → base → layout → components → page → atomic` (1 class = 1 properti, nol unused CSS).
2. **Hero Image & Media:**
   - Gambar Lead Story memakai `<div class="hero-media" data-img="..." data-alt="...">` + `<noscript><img ...></noscript>` + `assets/js/hero-defer.js` (`defer`) dengan `aspect-ratio: 16 / 9`, `width`, dan `height` eksplisit.
   - Semua gambar Section 2–6 wajib memakai `loading="lazy" decoding="async"` serta `width` & `height` eksplisit.
3. **Motion & Aksesibilitas (WCAG AA):**
   - Hanya transisi `transform` dan `opacity` (mis. `img` subtle zoom `scale(1.02)` saat hover link, nonaktif saat `prefers-reduced-motion: reduce`).
   - Dilarang `opacity: 0` atau `filter: blur()` pada elemen LCP.
   - Satu `<h1>` per halaman, urutan heading rapi (`H1 → H2 → H3`), semua link kategori/kicker memiliki area klik nyaman (`min-height: 44px` di mobile untuk target interaktif).
   - Kompatibel penuh dengan `hx-boost` dan i18n (`[data-i18n]`, `data-en` tanpa `MutationObserver`) serta Dark Mode Vanilla JS (`#theme-toggle`, `#lang-toggle`, `#about-menu-btn`).
