"""Langkah 4: halaman index /latest/ dengan struktur Dribbble (jalankan dari root repo).

- index.html: <main> diganti dengan plan-index/files/index-main.html
  (notice bar, hero: teks + kartu post terbaru, tab dengan ikon, grid kartu + kartu status).
- assets/site.css: komponen baru ditambahkan di akhir (plan-index/files/index.css).
"""
import pathlib
import sys

ROOT = pathlib.Path(".")
CSS = ROOT / "assets/site.css"
INDEX = ROOT / "index.html"
FILES = ROOT / "plan-index/files"
if not CSS.is_file() or not FILES.is_dir():
    sys.exit("Jalankan dari root repo: python3 -I plan-index/tools/step4.py")

css = CSS.read_text()
if ".feature-card" in css:
    sys.exit("Langkah 4 sudah pernah dijalankan (.feature-card sudah ada di site.css).")
if ".site-header {" not in css:
    sys.exit("Jalankan Langkah 2 dan 3 dulu.")

text = INDEX.read_text()
start = text.find('    <main id="main">')
end = text.find("    </main>\n")
if start < 0 or end < start:
    sys.exit("index.html: blok <main> tidak ditemukan. Berhenti dan laporkan ke user.")
old_main = text[start:end]
if '<p class="eyebrow">[Radova Updates]</p>' not in old_main or '<ol class="post-grid">' not in old_main:
    sys.exit("index.html: isi <main> bukan versi yang diharapkan (header editorial + post-grid). "
             "Mungkin sudah diubah; berhenti dan laporkan ke user.")
end += len("    </main>\n")
INDEX.write_text(text[:start] + (FILES / "index-main.html").read_text() + text[end:])

CSS.write_text(css.rstrip("\n") + "\n" + (FILES / "index.css").read_text())
print("Langkah 4 selesai: index.html diganti, komponen index ditambahkan ke site.css.")
