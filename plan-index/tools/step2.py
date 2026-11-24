"""Langkah 2: fondasi visual (jalankan dari root repo).

- Salin ikon Phosphor (MIT, sesuai Figma "Icon Type: Phosphor") ke assets/icons/ dan logo Radova ke assets/logo.png.
- assets/site.css: token radius, tombol pill (Figma "Button Type"), badge pill.
"""
import pathlib
import shutil
import sys

ROOT = pathlib.Path(".")
FILES = ROOT / "plan-index/files"
CSS = ROOT / "assets/site.css"
if not CSS.is_file() or not FILES.is_dir():
    sys.exit("Jalankan dari root repo: python3 -I plan-index/tools/step2.py")


def replace_once(text, old, new, where):
    count = text.count(old)
    if count != 1:
        sys.exit(f"{where}: teks yang dicari muncul {count} kali, harusnya 1. Berhenti dan laporkan ke user.")
    return text.replace(old, new)


css = CSS.read_text()
if "--radova-pill" in css:
    sys.exit("Langkah 2 sudah pernah dijalankan (token --radova-pill sudah ada).")

# Aset
(ROOT / "assets/icons").mkdir(exist_ok=True)
for icon in sorted((FILES / "icons").iterdir()):
    shutil.copy(icon, ROOT / "assets/icons" / icon.name)
shutil.copy(FILES / "logo.png", ROOT / "assets/logo.png")

# Token
css = replace_once(css, '  --radova-heading-font: "Lato", system-ui, sans-serif;\n',
                   '  --radova-heading-font: "Lato", system-ui, sans-serif;\n'
                   '  --radova-radius: 12px;\n'
                   '  --radova-radius-lg: 20px;\n'
                   '  --radova-pill: 999px;\n', "token")

# Tombol: blok lama diganti utuh
start = css.find("/* ---------- .button: primary call to action ---------- */")
end = css.find("/* ---------- .pager:")
if start < 0 or end < start:
    sys.exit("Blok .button lama tidak ditemukan. Berhenti dan laporkan ke user.")
css = css[:start] + '''/* ---------- .button: pill call to action (Figma "Button Type") ---------- */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  min-height: 48px;
  padding: 0.625rem 1.5rem;
  border: 1.5px solid var(--radova-red);
  border-radius: var(--radova-pill);
  font-weight: 700;
  line-height: 1.2;
  text-decoration: none;
  color: var(--radova-white);
  background: var(--radova-red);
}
.button:hover,
.button:focus-visible {
  color: var(--radova-white);
  border-color: var(--radova-red-2);
  background: var(--radova-red-2);
}
.button:focus-visible {
  outline: 3px solid var(--radova-red-3);
  outline-offset: 2px;
}
.button--navy {
  border-color: var(--radova-navy);
  background: var(--radova-navy);
}
.button--navy:hover,
.button--navy:focus-visible {
  border-color: var(--radova-blue);
  background: var(--radova-blue);
}
.button--small {
  min-height: 38px;
  padding: 0.375rem 1.125rem;
  font-size: 0.875rem;
}
/* A white circle with a red arrow at the end, like "Get Radova Linux" on radova.org. */
.button--arrow {
  padding-right: 0.5rem;
}
.button--arrow::after {
  content: "";
  flex: none;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--radova-white) url("icons/arrow-right-red.svg") center / 1.125rem no-repeat;
}

''' + css[end:]

# Badge pill
css = replace_once(css, ".badge {\n  display: inline-block;\n",
                   ".badge {\n  display: inline-block;\n  border-radius: var(--radova-pill);\n", "badge")

CSS.write_text(css)
print("Langkah 2 selesai: ikon + logo disalin, token radius, tombol pill, badge pill.")
