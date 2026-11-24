# Laporan Progres: Radova "Latest"

Diperbarui: 20 November 2026

Halaman **Latest** menampilkan pembaruan terbaru Radova dalam empat kategori: **Agenda, Article, News, Security**.

- **Acuan:**
  - Rencana issue: `Markdown Live Preview.pdf`
  - Style guide Figma: `Frame 1-1.pdf` (warna, font, tombol, kartu, ikon)
  - Struktur halaman: dribbble.com (beranda dan halaman shot)
  - Brief desain: `claude_cli_design_brief.md`
- **Stack:** HTML statis, Pico CSS, htmx, dan vanilla JS. Tanpa Node.js/npm, dan tetap terbaca di Lynx.

## Ringkasan status

| Issue | Judul | Status |
|---|---|---|
| 1 | Struktur direktori dan standar metadata | Selesai |
| 2 | Template HTML inti dan struktur listing | Selesai |
| 3 | Styling dasar, tema brand, master layout | Selesai |
| 4 | Styling halaman listing dan komponen kartu | Selesai |
| 5 | Styling halaman detail keempat tipe konten | Selesai |
| 6 | Tab switching dan "Load More" (htmx) | Selesai |
| 7, 8 | – | Tidak ada di PDF rencana |
| 9 | Microcopy UI, empty state, halaman 404 | Selesai |
| 10 | Security Policy dan `security.txt` | Selesai, kecuali email kontak resmi (masih `security@example.org`) |
| 11 | Konten awal untuk soft launch | Selesai: 1 News, 1 Article; Agenda dan Security tampil kosong |

## Tampilan saat ini

- **Semua halaman:**
  - Font dasar 16px (Figma "Normal Text"), tepi halaman 72px di layar lebar.
  - Header berisi logo, menu, search, dan tombol "Get Radova".
  - Tidak ada bayangan. Kartu dan panel memakai radius 12px.
- **`/latest/`:**
  - Notice keamanan.
  - Hero: judul "One system for every …" dengan kata yang berganti mengikuti video aplikasi.
  - Tab kategori, kotak search, chip "Popular" (dari tag post), dan menu sort.
  - Grid kartu 4 kolom. Kartu post memakai foto; kartu status untuk kategori yang masih kosong.
- **Halaman kategori:**
  - Judul dan deskripsi singkat, tab, dan grid kartu yang sama dengan `/latest/`.
  - Halaman kategori kosong menampilkan empty state. Agenda punya dua bagian: Upcoming dan Past Events.
- **Halaman detail (seperti halaman shot Dribbble):**
  - Satu kolom di tengah: judul; byline (avatar, penulis, tanggal, waktu baca) dengan tombol kategori di kanan; foto besar; isi 20px; tag; lalu "More updates".
  - Agenda dan Security tetap memakai `<dl>` untuk waktu, lokasi, status, severity, dan versi.

## Verifikasi (20 November 2026)

- **`python3 -I plan-index/tools/check.py`:** OK. Tidak ada kode inline atau tag yang tidak seimbang, dan semua link, anchor, serta `url()` valid.
- **Horizontal scroll:** tidak ada di lebar 375, 768, dan 1280px pada kesembilan halaman, dengan dropdown header tertutup maupun terbuka.
- **Batas 30 link per halaman listing (Issue 4):** terpenuhi sekarang, juga saat halaman penuh (10 post, Previous dan Next). Pada halaman Security ke-2 dan seterusnya, tombol "Report a vulnerability" tidak dipasang (lihat `templates/listing.html`).
- **Kontras:** teks dan badge lolos WCAG AA; nilai terendah 4.99:1 (tanggal di byline).
- **Fitur JS di Chrome:**
  - ganti tab htmx;
  - search, chip, dan sort di `/latest/`;
  - kata hero mengikuti video.
- **Lynx:** hanya dicek dengan simulasi (`check.py --dump`), karena Lynx tidak terpasang. Kontrol yang butuh JS (chip, sort) dibuat oleh `site.js`, jadi tidak muncul di Lynx.

## Keputusan yang diambil

- **Font mengikuti Figma:** Roboto untuk heading, Lato untuk teks. Rencana PDF dan brief menyebut susunan sebaliknya.
- **Kartu tanpa ringkasan,** atas permintaan: hanya badge, judul, penulis, dan tanggal. Ringkasan tetap ada di `<meta name="description">`.
- **"Latest" di header berupa satu link,** bukan dropdown. Isinya sama dengan tab kategori, dan ini menjaga halaman listing di bawah 30 link.
- **Foto kartu dan halaman detail** memakai poster video hero (`assets/hero/*.jpg`, lisensi Mixkit).
- **Feed `/latest/feed.xml` tidak dibuat,** karena Issue 7 dan 8 tidak ada di rencana.

## Yang perlu ditindaklanjuti

1. **Email kontak keamanan resmi.** Ganti `security@example.org` di `SECURITY.md`, `security/policy/index.html` (2 tempat), dan `.well-known/security.txt`.
2. **Pasang `security.txt` di root domain.** RFC 9116 mewajibkan `https://radova.org/.well-known/security.txt`, jadi file ini perlu disalin ke repo homepage. Di repo ini file tersebut tayang di `/latest/.well-known/`.
3. **Uji di Lynx sungguhan** (`lynx -dump -width=80`) sebelum launch.
