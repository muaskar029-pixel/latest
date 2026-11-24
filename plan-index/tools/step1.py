"""Langkah 1: rapikan sisa merge 8d59d7d (jalankan dari root repo, SETELAH git mv / git rm di PLAN.md).

1. Hapus penanda konflik yang ikut ter-commit di templates/listing.html dan templates/README.md.
2. Perbaiki path file lama `latest/...` di dokumentasi (situs sekarang ada di root repo).
3. Ganti "/assets/ menjadi "/latest/assets/ di semua HTML: repo ini tayang di radova.org/latest/,
   jadi /assets/ akan mengambil file milik repo homepage, bukan milik repo ini.
"""
import pathlib
import sys

ROOT = pathlib.Path(".")
if not (ROOT / "assets/site.css").is_file() or not (ROOT / "plan-index").is_dir():
    sys.exit("Jalankan dari root repo: python3 -I plan-index/tools/step1.py")
if (ROOT / "article/sample-article").exists():
    sys.exit("Jalankan dulu perintah git rm di PLAN.md Langkah 1.")
# git mv meninggalkan folder latest/ yang kosong; hapus hanya kalau benar-benar kosong.
leftover = ROOT / "latest"
if leftover.exists():
    if any(p.is_file() for p in leftover.rglob("*")):
        sys.exit("Masih ada file di latest/: jalankan dulu perintah git mv di PLAN.md Langkah 1.")
    for folder in sorted(leftover.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        folder.rmdir()
    leftover.rmdir()


def replace_once(text, old, new, where):
    count = text.count(old)
    if count != 1:
        sys.exit(f"{where}: teks yang dicari muncul {count} kali, harusnya 1. Berhenti, jangan diakali; laporkan ke user.")
    return text.replace(old, new)


# 1a. templates/listing.html: ambil sisi upstream (komentar dengan path baru).
path = ROOT / "templates/listing.html"
text = path.read_text()
text = replace_once(text, '''<<<<<<< HEAD
=======
    <!-- Page 1 is {{type}}/index.html; page N>1 adds " - Page N" and lives in {{type}}/page/N/index.html. -->
>>>>>>> upstream/main
''', '''    <!-- Page 1 is {{type}}/index.html; page N>1 adds " - Page N" and lives in {{type}}/page/N/index.html. -->
''', path)
text = replace_once(text, "Page 1 is latest/{{type}}/index.html; page N>1 is latest/{{type}}/page/N/index.html",
                    "Page 1 is {{type}}/index.html; page N>1 is {{type}}/page/N/index.html", path)
path.write_text(text)

# 1b. templates/README.md: ambil sisi HEAD (lebih lengkap) dengan path file versi upstream.
path = ROOT / "templates/README.md"
text = path.read_text()
start = text.index("<<<<<<< HEAD\n")
middle = text.index("=======\n", start)
end = text.index(">>>>>>> upstream/main\n", middle) + len(">>>>>>> upstream/main\n")
ours = text[start + len("<<<<<<< HEAD\n"):middle]
for old, new in [
    ("`latest/<type>/<slug>/index.html`", "`<type>/<slug>/index.html`"),
    ("`latest/<type>/index.html`", "`<type>/index.html`"),
    ("`latest/<type>/page/2/`", "`<type>/page/2/`"),
    ("`latest/index.html`", "`index.html`"),
    ("`latest/agenda/<slug>/<slug>.ics`", "`agenda/<slug>/<slug>.ics`"),
    ("`latest/agenda/index.html`", "`agenda/index.html`"),
]:
    ours = replace_once(ours, old, new, f"{path} ({old})")
path.write_text(text[:start] + ours + text[end:])

# 2. Tidak boleh ada penanda konflik tersisa di file teks mana pun.
for f in ROOT.rglob("*"):
    if ".git" in f.parts or "plan-index" in f.parts or not f.is_file():
        continue
    if f.suffix not in {".html", ".md", ".css", ".js", ".txt", ".ics"}:
        continue
    for line in f.read_text(errors="replace").splitlines():
        if line.startswith(("<<<<<<< ", ">>>>>>> ")) or line == "=======":
            sys.exit(f"Masih ada penanda konflik di {f}: {line!r}")

# 3. Path aset.
changed = 0
for f in sorted(ROOT.rglob("*.html")):
    if ".git" in f.parts or "plan-index" in f.parts:
        continue
    text = f.read_text()
    if '"/assets/' in text:
        f.write_text(text.replace('"/assets/', '"/latest/assets/'))
        changed += 1
print(f"Langkah 1 selesai: konflik dirapikan, path dokumentasi diperbaiki, path aset diganti di {changed} file HTML.")
