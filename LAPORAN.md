# Laporan Progres: Radova "Latest"

Diperbarui: 14 November 2026

Halaman **Latest** menampilkan pembaruan terbaru Radova dalam empat kategori: **Agenda, Article, News, Security**.

- **Acuan:**
  - Rencana issue: `Markdown Live Preview.pdf`
  - Style guide Figma: `Frame 1-1.pdf`
  - Brief desain: `claude_cli_design_brief.md`
- **Stack:** HTML statis, Pico CSS, htmx, dan vanilla JS. Tanpa Node.js/npm, dan harus tetap terbaca di Lynx.

## Ringkasan status

| Issue | Judul | Status |
|---|---|---|
| 1 | Struktur direktori dan standar metadata | Selesai, di-commit (`eb53072`) |
| 2 | Template HTML inti dan struktur listing | Selesai, di-commit (`1cb66ae`) |
| (–) | Perapian indentasi HTML | Selesai, di-commit (`bad2a71`) |
| 3 | Styling dasar, tema brand, master layout | Selesai, diperbarui sesuai brief; di-commit (`5ced1b8`) |
| 4 | Styling halaman listing dan komponen kartu | Selesai, diperbarui sesuai brief; di-commit (`5ced1b8`) |
| 5 | Styling halaman detail keempat tipe konten | Selesai, di-commit (`5ced1b8`) |
| 6 | Tab switching dan "Load More" (htmx) | Selesai, di-commit (`5ced1b8`) |
| 7, 8 | – | Tidak ada di PDF rencana |
| 9 | Microcopy UI, empty state, halaman 404 | Belum dikerjakan |
| 10 | Security Policy dan `security.txt` | Belum dikerjakan (perlu email kontak keamanan) |
| 11 | Konten awal untuk soft launch | Belum dikerjakan |

## Yang sudah dibuat

### Issue 1: Struktur direktori dan standar metadata
- Folder `latest/` (dengan `agenda/`, `article/`, `news/`, `security/`), `templates/`, dan `assets/`.
- Struktur URL: `/latest/`, `/latest/<type>/`, `/latest/<type>/<slug>/`, `/latest/<type>/page/<n>/`.
- Metadata disimpan di `<head>` sebagai `<meta name="radova:<field>">`, didokumentasikan di `templates/README.md`:
  - **Semua tipe:** `title`, `slug`, `date`, `summary`, `tags`.
  - **Article dan News:** `author`. Article juga punya `reading_time`.
  - **Agenda:** `start_time`, `end_time`, `location`, `register_url`, `status`.
  - **Security:** `advisory_id`, `severity`, `affected_versions`, `patched_versions`, `cve`, `status`.
- Satu entri contoh per kategori.

### Issue 2: Template halaman dan struktur listing
- **`/latest/`** menampilkan 10 item terbaru dari semua kategori.
- **Halaman kategori** menampilkan 10 item per halaman, terbaru dulu.
- **Agenda** dibagi dua bagian: **Upcoming Events** dan **Past Events**, dengan waktu dalam WIB (`+07:00`).
- **Template** untuk menyalin konten baru: `post.html`, `agenda.html`, `security.html`, `listing.html`. Cara publikasi ada di `templates/README.md`.
- HTML semantik, tanpa script atau style inline.

### Issue 3: Styling dasar, tema brand, master layout
- **Aset lokal** (versi dipatok): Pico CSS 2.1.1 (classless), htmx 2.0.11, font Lato dan Roboto (400 dan 700) beserta lisensi OFL-nya.
- **Master layout:** link "Skip to main content" → `<header>` berisi wordmark RADOVA → `<main id="main">` → `<footer>`.
- **Token brand di `assets/site.css`**, tanpa `!important`:
  - Latar lavender `#F7F6FF`, permukaan putih, teks navy `#0E0347`.
  - Aksen merah `#A10000` / `#BB080B` / `#DB000F`.
  - Garis struktur `rgba(14, 3, 71, 0.12)`.
  - Heading memakai Lato, body memakai Roboto.
- **Konfigurasi htmx yang aman** di `<head>`: `allowEval: false`, `allowScriptTags: false`, `selfRequestsOnly: true`.

### Issue 4: Halaman listing
- **`.editorial-header`:** eyebrow dan H1 di kiri, deskripsi di kanan.
- **`.tab-grid`:**
  - Tab berupa sel bergaris dengan tinggi 52 px; 5 kolom sama lebar di desktop, 2 kolom di mobile.
  - Tab aktif berlatar putih, tebal, dengan garis merah di bawah.
- **`.post-grid` / `.post-row`:**
  - Daftar bergaris tanpa bayangan, terbagi 1.2 : 0.8. Seluruh baris bisa diklik.
  - Kolom kiri berisi badge tipe (di `/latest/`), judul, ringkasan, dan tanggal (plus reading time untuk Article).
  - Panel kanan berisi data per tipe: Author dan Tags untuk Article/News; waktu mulai, lokasi, dan status untuk Agenda; ID advisory (monospace), severity, status, dan versi terdampak untuk Security.
- **Badge** selalu berisi teks, dengan warna sebagai penguat. Semua lolos kontras WCAG AA.
- **Pemisah ` · `** tetap ada sebagai teks, jadi terbaca di Lynx, dan disembunyikan CSS di browser.
- **`.pager`:** bar Previous/Next bergaris.

### Issue 5: Halaman detail
- **`.single-split`:**
  - Kolom kiri berisi link "← Back to …", eyebrow, H1, dan `<dl class="meta-dl">` metadata.
  - Kolom kanan berisi prosa putih (`.editorial-prose`) selebar maksimal 65 karakter.
- **Article:** drop cap pada paragraf pertama (CSS saja), blockquote bergaris merah, dan `<pre>` yang scroll di dalam kotaknya.
- **Agenda:** tombol "Register Now" dan link "Add to calendar (.ics)", dengan file contoh `sample-agenda.ics`.
- **Security:** isi terbagi dalam bagian Summary, Impact, Mitigation, Credits, dan Timeline.
- **Navigasi Previous/Next post** tersedia di template.

### Issue 6: htmx (tab dan Load more)
- **Tab kategori** memakai `hx-boost`, `hx-select="main"`, `hx-target="main"`, `hx-swap="outerHTML"`, dan `hx-push-url`, jadi ganti tab tidak perlu reload penuh.
- **Tombol Next jadi "Load more" saat JS aktif.** Isinya: menambahkan 10 item berikutnya ke daftar, mengganti pager, dan menghilang di halaman terakhir. Judul halaman tidak ikut berubah.
- **`assets/site.js`** memindahkan fokus keyboard setelah swap dan mengumumkan item baru lewat `aria-live="polite"`.
- **`hx-boost="false"`** dipasang di link eksternal dan unduhan.
- **Tanpa JS atau di Lynx,** tab dan pager tetap berfungsi sebagai link biasa.

## Struktur file saat ini

```
assets/
  fonts/              Lato & Roboto (woff2) + lisensi
  htmx.min.js
  pico.classless.min.css
  site.css            token brand dan komponen (editorial-header, tab-grid, post-row, single-split, ...)
  site.js             fokus dan pengumuman setelah swap htmx
latest/
  index.html          10 terbaru
  <type>/index.html   listing per kategori
  <type>/sample-*/    entri contoh (+ sample-agenda.ics)
templates/
  README.md           standar metadata, URL, cara publikasi, daftar komponen
  post.html, agenda.html, security.html, listing.html
```

## Verifikasi yang sudah dilakukan

- **Kode inline:** tidak ada `style=`, `<style>`, script inline, maupun `hx-on`, dan tag HTML seimbang.
- **Horizontal scroll:** tidak ada di lebar 375, 768, dan 1280 px pada kesembilan halaman.
- **Kontras warna:** semua pasangan teks/latar dan badge lolos WCAG AA (terendah 4.99:1).
- **Bayangan:** tidak ada sama sekali, dicek di browser.
- **Link:** semua link internal dan file `.ics` mengembalikan HTTP 200. Paling banyak 11 link per halaman listing (batas dari rencana 30).
- **htmx** (diuji di Chrome dengan salinan situs berisi 23 post uji):
  - Ganti tab: tanpa reload, URL dan judul ikut berubah, fokus pindah ke tab aktif.
  - Load more: 10 → 20 → 23 item, pengumuman benar, tombol hilang di halaman terakhir.
  - Back/Forward: URL, isi, dan tab aktif kembali dengan benar.

**Belum diverifikasi:** tampilan di **Lynx sungguhan**. Urutan baca hanya dicek dengan simulasi, karena Lynx tidak terpasang.

## Keputusan yang diambil

- **Font:** Lato untuk heading dan Roboto untuk body, sesuai rencana PDF dan brief. Figma memakai susunan sebaliknya.
- **Logo:** dipakai wordmark teks "RADOVA" karena belum ada file logo (SVG).
- **Listing diisi manual,** sesuai prinsip HTML statis tanpa build. Event Agenda harus dipindah dari "Upcoming" ke "Past Events" dengan tangan.
- **Bagian brief yang tidak diikuti persis:**
  - Link feed `/latest/feed.xml` belum dipasang, karena feed-nya belum ada.
  - Tab kategori dipindah dari header situs ke `.tab-grid`, jadi halaman detail memakai link kembali.
  - Badge di dalam `<dl>` hanya berisi nilainya, karena labelnya sudah diberikan `<dt>`.
  - Kolom kiri halaman detail tidak dibuat sticky.
- **Load more tidak mengubah URL.** Kalau halaman di-refresh, daftar kembali ke 10 item pertama.
- **Agenda belum punya Load more,** karena pagination untuk dua bagiannya belum ditentukan.

## Yang perlu ditindaklanjuti

1. **Siapkan file logo SVG** kalau ada.
2. **Konfirmasi nama footer** "Radova Linux".
3. **Cek path deploy.** Folder `latest/` ada di dalam repo bernama `latest`; kalau repo di-deploy di path `/latest/`, URL-nya jadi `/latest/latest/`.
4. **Konfirmasi Issue 7 dan 8** memang tidak ada. Feed XML yang dirujuk Issue 6 dan brief kemungkinan bagian dari issue itu.
5. **Siapkan email kontak keamanan** resmi untuk Issue 10.
6. **Uji di Lynx sungguhan** (`lynx -dump -width=80`) sebelum launch.
