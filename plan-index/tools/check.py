"""Verifikasi statis Radova Latest (jalankan dari root repo setelah tiap langkah).

  python3 -I plan-index/tools/check.py              # semua cek
  python3 -I plan-index/tools/check.py --dump FILE  # perkiraan `lynx -dump` untuk satu halaman

Cek: penanda konflik, kode inline, keseimbangan tag, link internal dan anchor, url() di site.css,
jumlah link per halaman listing (maks. 30, syarat Issue 4).
"""
import pathlib
import re
import sys
import textwrap
from html.parser import HTMLParser

ROOT = pathlib.Path(".")
if not (ROOT / "assets/site.css").is_file():
    sys.exit("Jalankan dari root repo.")
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "track", "wbr", "area", "base", "col", "embed", "param"}
BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "dt", "dd", "header", "footer", "nav", "section", "article", "div",
         "blockquote", "pre", "ol", "ul", "dl", "main", "tr"}


def site_files(pattern):
    return [f for f in sorted(ROOT.rglob(pattern)) if ".git" not in f.parts and "plan-index" not in f.parts]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors, self.ids, self.urls, self.links = [], [], set(), [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.urls.append(attrs[key])
        if tag == "a" and "href" in attrs:
            self.links += 1
        if tag == "script" and "src" not in attrs:
            self.errors.append("inline <script>")
        if tag == "style":
            self.errors.append("<style> element")
        for key in attrs:
            if key == "style" or key.startswith("on") or key.startswith("hx-on"):
                self.errors.append(f"inline attribute {key}=")
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append(f"tag tidak seimbang: </{tag}> di baris {self.getpos()[0]}")
            return
        self.stack.pop()


def dump(path):
    """Perkiraan `lynx -dump`: urutan sumber, tanpa CSS, link bernomor."""
    class Dump(HTMLParser):
        def __init__(self):
            super().__init__()
            self.lines, self.n, self.skip = [""], 0, 0

        def newline(self):
            if self.lines[-1].strip():
                self.lines.append("")

        def handle_starttag(self, tag, attrs):
            if tag in ("head", "script", "style"):
                self.skip += 1
            if tag in BLOCK:
                self.newline()
            if tag == "li":
                self.lines[-1] += "  * "
            if tag == "a":
                self.n += 1
                self.lines[-1] += f"[{self.n}]"

        def handle_endtag(self, tag):
            if tag in ("head", "script", "style"):
                self.skip -= 1
            if tag in BLOCK:
                self.newline()

        def handle_data(self, data):
            if self.skip:
                return
            data = re.sub(r"\s+", " ", data)
            if not self.lines[-1].strip():
                data = data.lstrip()
            self.lines[-1] += data

    d = Dump()
    d.feed(path.read_text())
    for line in d.lines:
        if line.strip():
            print(textwrap.fill(line, 80))


if len(sys.argv) == 3 and sys.argv[1] == "--dump":
    dump(pathlib.Path(sys.argv[2]))
    sys.exit(0)

problems, notes = [], set()

for f in site_files("*"):
    if f.is_file() and f.suffix in {".html", ".md", ".css", ".js", ".txt", ".ics"}:
        for n, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
            if line.startswith(("<<<<<<< ", ">>>>>>> ")) or line == "=======":
                problems.append(f"{f}:{n}: penanda konflik merge")

for f in site_files("*.html"):
    page = Page()
    page.feed(f.read_text())
    problems += [f"{f}: {e}" for e in page.errors]
    if page.stack:
        problems.append(f"{f}: tag tidak ditutup: {page.stack[-3:]}")
    if "templates" in f.parts:
        continue  # template berisi {{placeholder}}
    for url in page.urls:
        if url.startswith(("http://", "https://", "mailto:")):
            continue
        if url.startswith("#"):
            if url[1:] not in page.ids:
                problems.append(f"{f}: anchor {url} tidak ada")
            continue
        if url.startswith("/assets/"):
            problems.append(f"{f}: {url} harus /latest/assets/... (situs tayang di /latest/)")
            continue
        if not url.startswith("/latest/"):
            notes.add(url)  # milik repo homepage radova.org, bukan repo ini
            continue
        target = url[len("/latest/"):].split("#")[0].split("?")[0]
        if target == "" or target.endswith("/"):
            target += "index.html"
        if not (ROOT / target).is_file():
            problems.append(f"{f}: link {url} -> file {target} tidak ada")
    is_listing = f == ROOT / "index.html" or (len(f.parts) == 2 and f.name == "index.html")
    if is_listing and page.links > 30:
        problems.append(f"{f}: {page.links} link (maks. 30 untuk Lynx, Issue 4)")

css = (ROOT / "assets/site.css").read_text()
for url in sorted(set(re.findall(r'url\("([^"]+)"\)', css))):
    if not url.startswith("data:") and not (ROOT / "assets" / url).is_file():
        problems.append(f"assets/site.css: url(\"{url}\") tidak ada di assets/")

if problems:
    print("MASALAH:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("OK: tidak ada penanda konflik, kode inline, tag tak seimbang, link/anchor/url() rusak; "
      "halaman listing <= 30 link.")
if notes:
    print("Info: link ke repo homepage (tidak dicek di sini):", ", ".join(sorted(notes)))
