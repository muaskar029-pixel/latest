"""Langkah 3: header dan footer gaya radova.org di SEMUA halaman dan template (jalankan dari root repo).

Header: logo + RADOVA (ke radova.org) | Latest | tombol pill About (sama seperti header radova.org).
Footer: logo + RADOVA | Security policy | Source code | copyright.
"Latest" di header sengaja TANPA aria-current: htmx hanya menukar <main>, jadi header tidak ikut
berganti saat pindah tab dan aria-current akan basi.
"""
import pathlib
import sys

ROOT = pathlib.Path(".")
CSS = ROOT / "assets/site.css"
if not CSS.is_file() or not (ROOT / "plan-index").is_dir():
    sys.exit("Jalankan dari root repo: python3 -I plan-index/tools/step3.py")

OLD_HEADER = '''    <header>
      <a class="brand" href="/">RADOVA</a>
    </header>
'''
OLD_FOOTER = '''    <footer>
      <p>&copy; 2026 Radova Linux</p>
    </footer>
'''
LOCKUP = '<a class="brand-lockup" href="/"><img src="/latest/assets/logo.png" alt="" width="28" height="28">RADOVA</a>'
NEW_HEADER = f'''    <header class="site-header">
      {LOCKUP}
      <nav aria-label="Site">
        <ul>
          <li><a href="/latest/">Latest</a></li>
          <li><a class="button button--small button--navy" href="/about.html">About</a></li>
        </ul>
      </nav>
    </header>
'''
NEW_FOOTER = f'''    <footer class="site-footer">
      {LOCKUP}
      <ul>
        <li><a href="/latest/security/policy/">Security policy</a></li>
        <li><a href="https://github.com/radova-linux/latest">Source code</a></li>
      </ul>
      <p>&copy; 2026 Radova Linux</p>
    </footer>
'''

css = CSS.read_text()
if ".site-header {" in css:
    sys.exit("Langkah 3 sudah pernah dijalankan (.site-header sudah ada di site.css).")
if "--radova-pill" not in css:
    sys.exit("Jalankan Langkah 2 dulu.")

pages = [f for f in sorted(ROOT.rglob("*.html")) if ".git" not in f.parts and "plan-index" not in f.parts]
for f in pages:
    text = f.read_text()
    if text.count(OLD_HEADER) != 1 or text.count(OLD_FOOTER) != 1:
        sys.exit(f"{f}: header/footer lama tidak ditemukan tepat satu kali. Berhenti dan laporkan ke user.")
for f in pages:
    text = f.read_text()
    f.write_text(text.replace(OLD_HEADER, NEW_HEADER).replace(OLD_FOOTER, NEW_FOOTER))

CSS.write_text(css.rstrip("\n") + "\n" + (ROOT / "plan-index/files/chrome.css").read_text())
print(f"Langkah 3 selesai: header + footer baru di {len(pages)} file HTML, CSS ditambahkan.")
