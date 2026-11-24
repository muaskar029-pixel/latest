# Plan: redesain halaman `/latest/` (struktur Dribbble, guideline Radova)

Untuk dieksekusi model lain di Claude Code, dari root repo `/home/.trash/Projects/yuros/radova/latest`.
Semua kode di folder ini **sudah diuji**: dibuat sebagai prototipe, lalu seluruh plan dijalankan ulang di clone bersih
(dry run) dan hasilnya dicek di browser. Hasil akhir harus sama dengan gambar di `plan-index/target/`.

## Isi folder

| Path | Isi |
|---|---|
| `PLAN.md` | File ini |
| `target/index-1280.png`, `index-768.png`, `index-375.png` | Tampilan akhir `/latest/` yang harus dicapai |
| `target/card-variants-1280.png` | Contoh kartu untuk post Agenda, Security, News di masa depan (hanya referensi) |
| `files/` | CSS, HTML, ikon, dan logo siap pakai (jangan diedit kecuali user minta) |
| `tools/step1.py` … `step5.py` | Script per langkah. Script hanya mengganti teks yang persis cocok; kalau tidak cocok, script berhenti tanpa mengubah apa pun |
| `tools/check.py` | Verifikasi statis. Jalankan setelah setiap langkah |

## Aturan untuk eksekutor (wajib)

1. Baca seluruh file ini dan lihat keempat gambar di `target/` sebelum mulai.
2. Kerjakan **satu langkah per giliran**, urut dari Langkah 0 sampai 5. Setiap selesai satu langkah:
   - jalankan ceknya;
   - laporkan hasilnya ke user dalam **Bahasa Indonesia**;
   - beri perintah commit;
   - **berhenti**.

   User yang commit, jadi jangan commit sendiri. Lanjut hanya kalau user bilang "lanjut".
3. Jangan mengubah desain, teks, atau kode di luar plan ini. Kalau script atau cek gagal, **jangan diakali**: laporkan pesan error-nya ke user dan tunggu.
4. Aturan repo:
   - HTML diindentasi 2 spasi.
   - Tidak boleh ada `style="..."`, `<style>`, script inline, maupun `hx-on`.
   - Pemisah ` · ` tetap ditulis di HTML (dibaca Lynx, disembunyikan CSS).
   - Badge selalu berisi teks.
5. Hook **GateGuard** di mesin ini menahan Bash pertama, edit pertama pada sebuah file, dan perintah yang menghapus (`git rm`, `rm -r`, `git checkout --`). Kalau ditahan, tulis dulu:
   - file yang terkena;
   - cara rollback dalam satu baris;
   - kutipan instruksi user.

   Lalu ulangi **perintah yang sama persis**. Biasanya lolos pada percobaan kedua.
6. Script dijalankan dari root repo: `python3 -I plan-index/tools/stepN.py`.
7. Folder `plan-index/` **jangan di-commit**. Perintah commit di bawah sudah mengecualikannya.

## Kenapa versi sebelumnya kurang bagus

- Grid hanya berisi 1 kartu, sehingga dua pertiga lebar halaman kosong. Cover kartunya pun kotak putih kosong tanpa visual.
- Tidak ada logo, ikon, atau tombol pill. Header dan footer polos. Hasilnya tidak mirip radova.org, Figma, maupun Dribbble.
- Struktur Dribbble tidak lengkap: tidak ada top nav dan tidak ada bar pengumuman.
- Ada masalah di luar desain yang membuat halaman rusak saat tayang. `check.py` di HEAD menemukan 49 masalah:
  - link post 404;
  - CSS mengambil file milik repo homepage;
  - penanda konflik merge ikut ter-commit di template.

  Lihat Langkah 1.

## Target: struktur Dribbble dipetakan ke Radova

| Dribbble | `/latest/` versi baru |
|---|---|
| Top nav: logo, menu, Sign up / Log in | `.site-header`: logo + RADOVA (ke radova.org), link **Latest**, tombol pill **About**. Sama dengan header radova.org |
| Promo bar | `.notice-bar`: "Found a security issue in Radova Linux? Report it privately." + **Read the policy** |
| Hero kiri: 2 chip, judul besar dengan kata berwarna, checklist, tombol | `.hero-split`: chip **Radova Updates** + **Soft launch**, h1 "Read Our Latest **Updates**" ("Updates" merah), 3 poin bercentang, tombol pill **Browse all updates** dengan lingkaran panah (ke `#updates`) |
| Hero kanan: media besar + chip atribusi | `.feature-card`: post terbaru di tile navy besar dengan ikon kategori yang terpotong, ditambah chip byline putih (logo, "Radova Team", tanggal) |
| Tab Shots / Designers / Services | `.tab-grid` yang sudah ada, ditambah ikon Phosphor per kategori |
| Kotak search + chip "Popular" + dropdown sort | `.post-search` + `.post-filters` di bawah tab (lihat keputusan 5) |
| Grid kartu bergambar + baris meta (avatar, nama, angka) | `.card-grid` > `.post-card`: tile berwarna per kategori (`.cover`), lalu baris byline (avatar logo + penulis, tanggal). Kategori yang masih kosong mendapat **kartu status** |
| CTA lengket di bawah | Tidak dibuat |
| Footer | `.site-footer`: logo, **Security policy**, **Source code**, © |

## Keputusan desain (sudah diambil; user mohon tinjau sebelum eksekusi)

| # | Keputusan | Alasan | Kalau user tidak setuju |
|---|---|---|---|
| 1 | Sudut membulat (12px, kartu besar 20px). Tombol, badge, dan chip berbentuk pill. **Tetap tanpa shadow**, border 1px hairline. | Figma ("Button Type", "Card Implementation") dan radova.org memakai pill dan radius 12px. Larangan shadow dari brief tetap dipatuhi. | Ubah ketiga token `--radova-radius`, `--radova-radius-lg`, `--radova-pill` menjadi `0` |
| 2 | Roboto untuk judul, Lato untuk isi. | Mengikuti Figma (`Frame 1-1.pdf`). Diubah 2026-11-20; brief lama menulis sebaliknya. | – |
| 3 | Post terbaru tampil besar di hero dan **tidak diulang** di grid. Grid berisi 9 post berikutnya. | Padanan langsung dari media besar di hero Dribbble. Totalnya tetap 10 post terbaru, sesuai Issue 2. | – |
| 4 | **Kartu status** untuk kategori yang masih kosong (sekarang Agenda dan Security). Teksnya memakai empty state dari Issue 9. | Grid tidak bolong. Pengunjung juga langsung tahu belum ada event atau advisory. | Hapus dua `<li>` terakhir di `files/index-main.html` sebelum Langkah 4 |
| 5 | **Ada** kotak search, chip "Popular", dan sort (Newest/Oldest), hanya di `/latest/`. | Hero kini berisi video, bukan post, jadi semua post ada di grid dan search bisa menyaring semuanya. Dengan JS, search menyaring kartu di halaman; tanpa JS, search dikirim ke DuckDuckGo (radova.org). | Hapus `.post-search`, `.post-filters`, `.post-filters__empty` di `index.html` |
| 6 | Tanpa foto. Visual kartu berasal dari warna kategori dan ikon Phosphor besar. | Belum ada foto resmi. Foto di repo `abouts` sebagian bertanda "TEST DATA" atau foto stok yang lisensinya tidak jelas. Phosphor adalah set ikon di Figma ("Icon Type"). | – |
| 7 | Header dan footer baru dipasang di **semua** halaman dan template, bukan hanya index. | Konsisten dengan radova.org. Lagi pula htmx hanya menukar `<main>`, jadi header harus sama di semua halaman. | – |
| 8 | Footer berisi link **Source code** ke `https://github.com/radova-linux/latest`. | Footer radova.org juga punya link "Repository". | Hapus baris `<li>` itu di `tools/step3.py` sebelum Langkah 3 |
| 9 | Ada chip **Soft launch**. | Sama dengan chip di hero radova.org, dan Issue 11 bernama "Soft Launch". | Ubah atau hapus teksnya di `files/index-main.html` |
| 10 | Langkah 1 merapikan struktur hasil merge `8d59d7d`. | Tanpa ini link post menjadi 404 dan halaman memuat CSS yang salah di radova.org/latest/. | – |

---

## Langkah 0: buang percobaan sebelumnya (tanpa commit)

Saat ini `git status --short` menampilkan `M assets/site.css`, `M index.html`, `M templates/README.md` (percobaan model sebelumnya yang belum di-commit) dan `?? plan-index/`.

```bash
git checkout -- index.html assets/site.css templates/README.md
git status --short
```

Harus tersisa **hanya** `?? plan-index/`. Berhenti dan lapor.

## Langkah 1: rapikan struktur setelah merge

Masalahnya, semua terbukti dengan `check.py` di HEAD:

- Penanda konflik `<<<<<<<` / `=======` / `>>>>>>>` ikut ter-commit di `templates/README.md` (baris 72–124) dan `templates/listing.html` (baris 6–9).
- Upstream memindahkan situs ke root repo, tapi 3 post masih ada di `latest/...`. Akibatnya `/latest/news/introducing-radova-latest/` jadi 404, karena filenya sekarang tayang di `/latest/latest/news/...`.
- Empat folder `sample-*` muncul lagi, padahal Issue 11 sudah menghapusnya.
- Semua halaman memuat `/assets/...`. Di radova.org/latest/ path itu mengarah ke aset repo homepage (radova.org/assets/), bukan aset repo ini. Path yang benar adalah `/latest/assets/...`.

```bash
git mv latest/article/what-radova-linux-is-for article/what-radova-linux-is-for
git mv latest/news/introducing-radova-latest news/introducing-radova-latest
git mv latest/security/policy security/policy
git rm -r -q agenda/sample-agenda article/sample-article news/sample-news security/sample-security
python3 -I plan-index/tools/step1.py
python3 -I plan-index/tools/check.py
```

Hasil yang diharapkan:
- `Langkah 1 selesai: ... path aset diganti di 13 file HTML.`
- `OK: ...`. Baris `Info: link ke repo homepage ... /` itu normal.

Cek manual di preview (Lampiran A): `/latest/news/introducing-radova-latest/` terbuka dengan gaya yang benar.

Commit (oleh user):

```bash
git add -A -- . ':(exclude)plan-index'
git commit -m "Fix paths and merge leftovers after moving the site to the repo root"
```

## Langkah 2: fondasi visual (ikon, logo, tombol dan badge pill)

```bash
python3 -I plan-index/tools/step2.py
python3 -I plan-index/tools/check.py
```

Yang berubah:
- `assets/icons/` (baru): 7 SVG Phosphor dan `LICENSE-phosphor.txt` (MIT). `check-red.svg` dan `arrow-right-red.svg` adalah salinan Phosphor dengan warna `#A10000`.
- `assets/logo.png` (baru): salinan logo dari repo `radova-linux.github.io`.
- `assets/site.css`:
  - token `--radova-radius: 12px`, `--radova-radius-lg: 20px`, `--radova-pill: 999px`;
  - blok `.button` diganti menjadi pill, dengan varian `--navy`, `--small`, `--arrow`;
  - `.badge` dibuat pill.

Cek visual di `/latest/security/`: tombol "Report a vulnerability" dan badge severity sekarang berbentuk pill.

```bash
git add -A -- . ':(exclude)plan-index'
git commit -m "Add Phosphor icons and logo, pill buttons and badges"
```

## Langkah 3: header dan footer gaya radova.org di semua halaman

Markup baru, dipasang oleh `tools/step3.py` di 13 file HTML (halaman, 404, dan template):

```html
    <header class="site-header">
      <a class="brand-lockup" href="/"><img src="/latest/assets/logo.png" alt="" width="28" height="28">RADOVA</a>
      <nav aria-label="Site">
        <ul>
          <li><a href="/latest/">Latest</a></li>
          <li><a class="button button--small button--navy" href="/about.html">About</a></li>
        </ul>
      </nav>
    </header>
```

```html
    <footer class="site-footer">
      <a class="brand-lockup" href="/"><img src="/latest/assets/logo.png" alt="" width="28" height="28">RADOVA</a>
      <ul>
        <li><a href="/latest/security/policy/">Security policy</a></li>
        <li><a href="https://github.com/radova-linux/latest">Source code</a></li>
      </ul>
      <p>&copy; 2026 Radova Linux</p>
    </footer>
```

Catatan:
- Logo memakai `alt=""` karena teks "RADOVA" sudah menjadi nama link.
- "Latest" sengaja tanpa `aria-current`. htmx tidak menukar header, jadi atribut itu akan basi setelah pindah tab.
- CSS-nya (`files/chrome.css`) ditambahkan di akhir `site.css`.

```bash
python3 -I plan-index/tools/step3.py
python3 -I plan-index/tools/check.py
```

Hasil yang diharapkan: `... header + footer baru di 13 file HTML ...`, lalu `OK`. Cek di preview: semua halaman (termasuk `/latest/404.html`) memakai header dan footer baru.

```bash
git add -A -- . ':(exclude)plan-index'
git commit -m "Add radova.org-style site header and footer"
```

## Langkah 4: halaman index `/latest/`

`tools/step4.py` mengganti seluruh `<main>` di `index.html` dengan `files/index-main.html`, lalu menambahkan `files/index.css` ke `site.css`. Isinya:
- `.notice-bar`;
- `.hero-split` + `.chip` + `.check-list`;
- `.feature-card`;
- tab dengan `id="updates"` (tujuan tombol "Browse all updates");
- `ol.card-grid` berisi 1 kartu Article dan 2 kartu status (Agenda, Security);
- komponen `.cover` dan `.byline`;
- ikon di tab. Karena CSS-nya global, ikon tab juga muncul di halaman kategori.

```bash
python3 -I plan-index/tools/step4.py
python3 -I plan-index/tools/check.py
python3 -I plan-index/tools/check.py --dump index.html
```

Output `--dump` (urutan baca Lynx) harus persis seperti ini. Tanda `*` kosong adalah item `<ol>`; Lynx asli menampilkannya sebagai nomor.

```text
[1]Skip to main content
[2]RADOVA
  * [3]Latest
  * [4]About
Found a security issue in Radova Linux? Report it privately. [5]Read the policy
Radova Updates · Soft launch
Read Our Latest Updates
Events, articles, news, and security advisories from Radova Linux, newest first.
  * Events and community sessions on the Agenda
  * Articles and news from the Radova team
  * Security advisories with severity and fixed versions
[6]Browse all updates
News · Newest
[7]Introducing Radova Latest
Radova Latest is the new home for Radova Linux events, articles, news, and
security advisories, newest first.
Radova Team · 14 Nov 2026
  * [8]All Latest
  * [9]Agenda
  * [10]Article
  * [11]News
  * [12]Security
  *
Article · 2 min read
[13]What Radova Linux Is For
An introduction to Radova Linux: an operating system for libraries, archives,
and digital assets, its four built-in applications, and the principles behind
them.
Radova Team · 14 Nov 2026
  *
Agenda
No events have been scheduled yet.
[14]Go to Agenda
  *
Security
No security advisories have been published yet.
[15]Go to Security
[16]RADOVA
  * [17]Security policy
  * [18]Source code
© 2026 Radova Linux
```

Lalu cek di browser (Lampiran B). Hasil harus sama dengan `target/index-1280.png`, `index-768.png`, dan `index-375.png`.

```bash
git add -A -- . ':(exclude)plan-index'
git commit -m "Redesign /latest/: notice bar, hero with the newest post, card grid"
```

## Langkah 5: dokumentasi

`tools/step5.py` memperbarui `templates/README.md`:
- langkah 3 di "Publishing a post" (cara memutar post di hero dan grid, serta menghapus kartu status);
- baris baru di tabel Components dan UI copy;
- bagian baru "`/latest/` page" berisi snippet kartu per tipe dan kartu status.

```bash
python3 -I plan-index/tools/step5.py
python3 -I plan-index/tools/check.py
```

Baca bagian baru README itu sekali, lalu pastikan snippet-nya sama dengan markup di `index.html`.

```bash
git add -A -- . ':(exclude)plan-index'
git commit -m "Document the /latest/ components and publishing steps"
```

## Setelah selesai

- Hapus `plan-index/` (`rm -r plan-index`; GateGuard akan meminta fakta), atau biarkan saja asal tidak di-commit.
- Sengaja **belum** dikerjakan; tawarkan ke user, jangan dikerjakan tanpa izin:
  - search atau chip topik;
  - `feed.xml`;
  - memasang `security.txt` di repo homepage dan mengganti `security@example.org` dengan email asli;
  - memperbarui `LAPORAN.md`.

---

## Lampiran A: preview lokal

Situs ini memakai path `/latest/...`, jadi folder repo harus disajikan sebagai `/latest/`:

```bash
mkdir -p ../.preview && ln -sfn "$PWD" ../.preview/latest
cd ../.preview && python3 -m http.server 8000
# buka http://localhost:8000/latest/
```

Link ke `/` dan `/about.html` mengarah ke repo homepage, jadi wajar kalau di preview keduanya 404.

## Lampiran B: cek di browser

Kalau tool chrome-devtools tersedia:

1. Pakai `emulate` dengan viewport `1280x900x1`, `768x1000x1`, dan `375x812x1`. `resize_page` gagal kalau jendela browser sedang maximized.
2. Di tiap lebar, ambil screenshot full page lalu bandingkan dengan `target/`.
3. Pastikan tidak ada scroll horizontal. Jalankan `document.documentElement.scrollWidth <= innerWidth`; hasilnya harus `true`.
4. Uji pindah tab via htmx: klik tab **Agenda**, lalu **All Latest**. Hero harus muncul lagi, ada 3 kartu, dan fokus keyboard berada di tab "All Latest".
5. Uji fokus keyboard: tekan Tab sampai ke kartu. Ring merah harus mengelilingi seluruh kartu.

Kalau tool itu tidak tersedia, minta user membuka preview dan membandingkannya dengan gambar target.

## Lampiran C: catatan teknis (sudah ditangani di file; untuk review)

- Pico mewarnai setiap `<p>` dengan `--pico-color`, sehingga teks di tile navy, biru, dan merah tidak terlihat. Karena itu `.cover` mengatur variabel `--pico-color`, bukan hanya `color`.
- Pico memberi margin negatif pada list dan link di dalam `nav`, sehingga tombol About keluar 10px dari container. Ini direset di `.site-header`.
- Di lebar 768–1023px, kelima tab terlalu sempit untuk ikon, jadi ikon disembunyikan di rentang itu. Selain itu, `<a>` tab dibuat mengisi penuh tinggi sel.
- Grid 2 kolom (768–1023px): kartu terakhir yang ganjil dibuat selebar 2 kolom supaya tidak ada lubang.
- Kontras: semua teks lolos WCAG AA. Yang terendah 4.99:1 (tanggal di byline, warna muted Pico di atas lavender), sama dengan nilai terendah sebelumnya.
- Jumlah link di index sekarang 18. Saat grid penuh (9 post + 2 kartu status) maksimalnya 26, masih di bawah batas 30 dari Issue 4.
- Tidak ada scroll horizontal di 9 halaman × 3 lebar (375, 768, 1280).
