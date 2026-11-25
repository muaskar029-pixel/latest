#!/usr/bin/env python3
"""Generate the Indonesian (id/) and Arabic (ar/) copy of every English page in this repo.

    python3 translate.py           write id/ and ar/, refresh the language menu of the English pages
    python3 translate.py --check   list English texts that have no translation yet (exit 1 if any)
    python3 translate.py --check --dump   the same, as JSON {english: first page}, to start a translation

The English pages are the source; edit only them. Every text run (a heading, a paragraph with its inline
tags, a label, alt/title/aria-label/placeholder and the meta descriptions) is looked up by its English text
in i18n/id.json and i18n/ar.json. A value of null keeps the English (brand names, codes).
Links to pages get the language folder, links to assets go one folder up. Arabic pages get dir="rtl".
Keep this file identical in about, latest, learns and events. Standard library only.
"""
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOS = ("about", "latest", "learns", "events")
REPO = ROOT.name if ROOT.name in REPOS else sys.exit("run from a Radova repo")
LANGS = ("id", "ar")
SITE = "https://radova.org"
SKIP_DIRS = {"id", "ar", "templates", "plan-index", "node_modules", ".git"}
MENU_LABEL = {"en": ("EN", "EN: choose language"), "id": ("ID", "ID: pilih bahasa"), "ar": ("AR", "AR: اختر اللغة")}
MENU_NAMES = (("id", "Bahasa Indonesia"), ("ar", "العربية"), ("en", "English"))

OPAQUE = r"script|style|svg|pre|textarea"
TOKEN = re.compile(
    r"<!--.*?-->"
    r"|<(%s)\b(?:\"[^\"]*\"|'[^']*'|[^'\">])*>.*?</\1\s*>"
    r"|</?[a-zA-Z][^\s/>]*(?:\"[^\"]*\"|'[^']*'|[^'\">])*>"
    r"|<![^>]*>"
    r"|[^<]+" % OPAQUE,
    re.S | re.I,
)
INLINE = {"a", "abbr", "b", "br", "cite", "code", "em", "i", "kbd", "mark", "q", "s", "small", "span", "strong", "sub", "sup", "time", "u", "wbr"}
VOID = {"br", "wbr", "img", "input", "meta", "link", "hr", "source", "area", "base", "col", "embed", "track"}
TEXT_ATTRS = ("alt", "title", "aria-label", "placeholder", "data-word", "data-role", "data-tags", "data-label")  # shown by JS or CSS attr()
META_TEXT = {"description", "og:title", "og:description", "twitter:title", "twitter:description"}
URL_ATTRS = ("href", "src", "poster", "action", "data-full")
ATTR = re.compile(r"""(\s)([a-zA-Z_:][-a-zA-Z0-9_:.]*)(\s*=\s*)("[^"]*"|'[^']*')""")
LETTER = re.compile(r"[^\W\d_]")
CODE = re.compile(r"^(?:[\w.+-]*@[\w.:-]+|[\w-]+(?:\.[\w-]+)+(?:/\S*)?)$")  # e-mail, handle, domain: never translated


def tag_name(tok):
    m = re.match(r"</?([a-zA-Z][^\s/>]*)", tok)
    return m.group(1).lower() if m and tok.startswith("<") else None


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- URLs
def page_url(rel):
    """repo-relative page file -> its path inside the repo ('' for index.html, 'history' for history.html)."""
    return rel[: -len("index.html")] if rel.endswith("index.html") else rel[: -len(".html")]


def is_page(path):
    last = path.rsplit("/", 1)[-1]
    return last == "" or last.endswith(".html") or "." not in last


def lang_path(path, lang):
    """'/about/history' -> '/about/ar/history' for the four Radova repos; any other path is returned as is."""
    m = re.match(r"^/(%s)(/.*)?$" % "|".join(REPOS), path)
    if not m or lang == "en":
        return path
    return "/%s/%s/%s" % (m.group(1), lang, (m.group(2) or "/").lstrip("/"))


def rewrite_url(url, lang, page_dir):
    """A URL in a page that moves from <page_dir> to <lang>/<page_dir>."""
    if not url or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "{{")):
        return url
    m = re.match(r"^(https?://(?:www\.)?radova\.org)(/[^?#]*)?(.*)$", url)
    if m:
        path = m.group(2) or "/"
        return m.group(1) + (lang_path(path, lang) if is_page(path) else path) + m.group(3)
    if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("//"):
        return url
    path = re.match(r"^[^?#]*", url).group(0)
    tail = url[len(path):]
    if path.startswith("/"):
        return (lang_path(path, lang) if is_page(path) else path) + tail
    target = os.path.normpath(os.path.join(page_dir, path or "."))
    if target.startswith(".."):  # leaves this repo, e.g. ../learns/
        abs_path = "/" + os.path.normpath(os.path.join(REPO, page_dir, path)).replace(os.sep, "/")
        abs_path += "/" if path.endswith("/") else ""
        return (lang_path(abs_path, lang) if is_page(path) else abs_path) + tail
    return url if is_page(path) else "../" + url  # pages keep the same layout inside <lang>/; assets are one up


def rewrite_srcset(val, lang, page_dir):
    parts = [p.split() for p in val.split(",") if p.strip()]
    return ", ".join(" ".join([rewrite_url(p[0], lang, page_dir)] + p[1:]) for p in parts)


def rewrite_css_urls(css, lang, page_dir):
    return re.sub(r"""url\((["']?)([^"')]+)\1\)""",
                  lambda m: "url(%s%s%s)" % (m.group(1), rewrite_url(m.group(2), lang, page_dir), m.group(1)), css)


# ---------------------------------------------------------------- text runs
def is_inline(tok):
    n = tag_name(tok)
    return n is None and not tok.startswith("<") or n in INLINE


def units(tokens):
    """(first, last) token indices of each text run: text plus balanced inline tags, holding a letter."""
    def edge(i):
        t = tokens[i]
        return not t.strip() or tag_name(t) in VOID

    def segments(run):
        stack, sep = [], set()
        for i in run:
            t = tokens[i]
            if not t.startswith("<"):
                continue
            if t.startswith("</"):
                if stack and tag_name(tokens[stack[-1]]) == tag_name(t):
                    stack.pop()
                else:
                    sep.add(i)
            elif tag_name(t) not in VOID and not t.endswith("/>"):
                stack.append(i)
        sep |= set(stack)
        seg = []
        for i in run + [None]:
            if i is not None and i not in sep:
                seg.append(i)
                continue
            yield from refine(seg)
            seg = []

    def refine(seg):
        while seg and edge(seg[0]):
            seg = seg[1:]
        while seg and edge(seg[-1]):
            seg = seg[:-1]
        if not seg:
            return
        items, depth, start = [], 0, None  # top-level text tokens and elements of the run
        for i in seg:
            t = tokens[i]
            if not t.startswith("<"):
                if depth == 0:
                    items.append((i, i))
            elif t.startswith("</"):
                depth -= 1
                if depth == 0:
                    items.append((start, i))
            elif tag_name(t) in VOID or t.endswith("/>"):
                if depth == 0:
                    items.append((i, i))
            else:
                if depth == 0:
                    start = i
                depth += 1
        elements = [(a, b) for a, b in items if a != b]
        loose_text = [a for a, b in items if a == b and not tokens[a].startswith("<") and tokens[a].strip()]
        if len(items) == 1 and elements:  # <a ...>Text</a>: translate only the inside
            yield from refine([i for i in seg if elements[0][0] < i < elements[0][1]])
        elif len(elements) > 1 and not loose_text and all(tag_name(tokens[a]) == "a" for a, b in elements):  # sibling links
            for a, b in elements:
                yield from refine([i for i in seg if a <= i <= b])
        else:
            text = norm(html.unescape(re.sub(r"<[^>]*>", "", "".join(tokens[seg[0]: seg[-1] + 1]))))
            if LETTER.search(text) and not CODE.match(text):
                yield seg[0], seg[-1]

    run = []
    for i, tok in enumerate(tokens):
        if is_inline(tok) and not tok.startswith("<!"):
            run.append(i)
        else:
            yield from segments(run)
            run = []
    yield from segments(run)


def document_text(tokens):
    """Indices of tokens inside <title> or <body>: the page's own text (not other head metadata)."""
    keep, inside = set(), False
    for i, tok in enumerate(tokens):
        n = tag_name(tok)
        if n in ("title", "body"):
            inside = not tok.startswith("</")
        elif inside:
            keep.add(i)
    return keep


class Catalog:
    def __init__(self, lang):
        self.path = ROOT / "i18n" / (lang + ".json")
        self.data = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        self.missing, self.used = {}, set()

    def get(self, en, where):
        key = norm(en)
        text = html.unescape(re.sub(r"<[^>]*>", "", key))
        if not LETTER.search(text) or CODE.match(text):
            return None
        if key in self.data:
            self.used.add(key)
            return key if self.data[key] is None else self.data[key]
        self.missing.setdefault(key, where)
        return None


# ---------------------------------------------------------------- pages
MENU_RE = re.compile(r'([ \t]*)<div class="lang-menu">.*?</ul>\s*</div>', re.S)
ALT_RE = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n')


def menu(lang, rel, indent, btn_class="btn-lang"):
    code, label = MENU_LABEL[lang]
    here = "/%s/%s" % (REPO, page_url(rel))
    items = "".join(
        '\n%s    <li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>'
        % (indent, lang_path(here, l), l, l, ' aria-current="true"' if l == lang else "", name)
        for l, name in MENU_NAMES
    )
    return (
        '%s<div class="lang-menu">\n'
        '%s  <button type="button" id="lang-toggle" class="%s" aria-label="%s" aria-expanded="false" aria-controls="lang-list">'
        '<span>%s</span><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3.5 5 6.5 8 3.5"/></svg></button>\n'
        '%s  <ul id="lang-list" class="lang-list" hidden>%s\n'
        "%s  </ul>\n"
        "%s</div>" % (indent, indent, btn_class, label, code, indent, items, indent, indent)
    )


def with_menu(src, lang, rel):
    assert MENU_RE.search(src), rel + ": no language menu"
    def keep_class(m):  # the page may style the button with its own utility classes
        c = re.search(r'id="lang-toggle" class="([^"]*)"', m.group(0))
        return menu(lang, rel, m.group(1), c.group(1) if c else "btn-lang")
    return MENU_RE.sub(keep_class, src, count=1)


def with_alternates(src, rel):
    src = ALT_RE.sub("", src)
    if rel.endswith("404.html"):
        return src
    here = "/%s/%s" % (REPO, page_url(rel))
    links = "".join('  <link rel="alternate" hreflang="%s" href="%s%s">\n' % (h, SITE, lang_path(here, l))
                    for h, l in (("en", "en"), ("id", "id"), ("ar", "ar"), ("x-default", "en")))
    return src.replace("</head>", links + "</head>", 1)


def translate_page(src, lang, rel, cat):
    page_dir = os.path.dirname(rel)
    menu_block = MENU_RE.search(src).group(0)  # rebuilt by with_menu() afterwards, not translated here
    src = ALT_RE.sub("", src).replace(menu_block, "<!--lang-menu-->", 1)
    tokens = [m.group(0) for m in TOKEN.finditer(src)]
    assert "".join(tokens) == src, rel + ": tokenizer lost text"
    doc = document_text(tokens)
    out, done = list(tokens), set()

    # 1. text runs
    for first, last in units(tokens):
        if first in doc:
            chunk = "".join(tokens[first: last + 1])
            t = cat.get(chunk, rel)
            if t is not None:  # keep the whitespace around the run, it separates it from icons and tags
                lead, trail = re.match(r"^\s*", chunk).group(0), re.search(r"\s*$", chunk).group(0)
                out[first: last + 1] = [lead + t + trail] + [""] * (last - first)
                done.update(range(first, last + 1))

    # 2. text in attributes of the tags left (a translated run brings its own)
    for i, tok in enumerate(out):
        name = tag_name(tok)
        if i in done or name is None or tok.startswith("</") or name in ("script", "style", "svg", "pre"):
            continue
        open_tag = re.match(r"<(?:\"[^\"]*\"|'[^']*'|[^'\">])*>", tok).group(0)
        attrs = {m.group(2).lower(): m.group(4)[1:-1] for m in ATTR.finditer(open_tag)}
        meta_text = name == "meta" and (attrs.get("name") in META_TEXT or attrs.get("property") in META_TEXT)

        def text_attr(m):
            a, q = m.group(2).lower(), m.group(4)
            if (a in TEXT_ATTRS and i in doc) or (a == "content" and meta_text):
                t = cat.get(q[1:-1], rel + " @" + a)
                if t is not None:
                    assert q[0] not in t, "quote inside a translated attribute: " + t
                    return m.group(1) + m.group(2) + m.group(3) + q[0] + t + q[0]
            return m.group(0)

        out[i] = ATTR.sub(text_attr, open_tag) + tok[len(open_tag):]

    # 3. URLs, on the translated page: translations carry links too
    tokens = [m.group(0) for m in TOKEN.finditer("".join(out))]
    for i, tok in enumerate(tokens):
        name = tag_name(tok)
        if name is None or tok.startswith("</") or name in ("svg", "pre", "textarea"):
            continue
        open_tag = re.match(r"<(?:\"[^\"]*\"|'[^']*'|[^'\">])*>", tok).group(0)
        if name == "style":
            tokens[i] = rewrite_css_urls(tok, lang, page_dir)
            continue
        if name == "script" and "src=" not in open_tag:
            tokens[i] = re.sub(r"""(["'])assets/""", r"\1../assets/", tok)  # inline loaders name assets/ paths
            continue
        og_url = re.search(r"""property=["']og:url["']""", open_tag)

        def url_attr(m):
            a, q = m.group(2).lower(), m.group(4)
            v = q[1:-1]
            if a in URL_ATTRS or (a == "content" and og_url):
                v = rewrite_url(v, lang, page_dir)
            elif a == "srcset":
                v = rewrite_srcset(v, lang, page_dir)
            elif a == "style":
                v = rewrite_css_urls(v, lang, page_dir)
            return m.group(1) + m.group(2) + m.group(3) + q[0] + v + q[0]

        tokens[i] = ATTR.sub(url_attr, open_tag) + tok[len(open_tag):]

    page = "".join(tokens).replace("<!--lang-menu-->", menu_block, 1)
    return re.sub(r"<html\b[^>]*>", '<html lang="%s"%s>' % (lang, ' dir="rtl"' if lang == "ar" else ""), page, count=1)


def pages():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
        for f in sorted(fn):
            if f.endswith(".html"):
                yield os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")


def selftest():
    assert lang_path("/about/history", "ar") == "/about/ar/history"
    assert lang_path("/learns", "id") == "/learns/id/"
    assert lang_path("/", "ar") == "/"
    assert rewrite_url("assets/site.css", "ar", "") == "../assets/site.css"
    assert rewrite_url("history", "ar", "") == "history"
    assert rewrite_url("../agenda/", "id", "news") == "../agenda/"
    assert rewrite_url("https://radova.org/events", "id", "") == "https://radova.org/events/id/"
    assert rewrite_url("https://radova.org/", "id", "") == "https://radova.org/"
    assert rewrite_url("/latest/assets/logo.png", "id", "") == "/latest/assets/logo.png"
    assert rewrite_url("#main", "ar", "") == "#main"
    toks = [m.group(0) for m in TOKEN.finditer('<p>Use <code>x</code> now.</p><a href="/"><svg><path/></svg> Home</a>')]
    assert [norm("".join(toks[a: b + 1])) for a, b in units(toks)] == ["Use <code>x</code> now.", "Home"]
    toks = [m.group(0) for m in TOKEN.finditer('<li><a href="a">One</a> <a href="b">Two</a></li><p>Mail <a href="m">me@x.org</a></p><b>me@x.org</b>')]
    assert [norm("".join(toks[a: b + 1])) for a, b in units(toks)] == ["One", "Two", 'Mail <a href="m">me@x.org</a>']


def main():
    selftest()
    check = "--check" in sys.argv
    cats = {l: Catalog(l) for l in LANGS}
    written = 0
    for rel in pages():
        src = (ROOT / rel).read_text(encoding="utf-8")
        en = with_alternates(with_menu(src, "en", rel), rel)
        for lang in LANGS:
            page = with_alternates(with_menu(translate_page(en, lang, rel, cats[lang]), lang, rel), rel)
            if not check:
                (ROOT / lang / rel).parent.mkdir(parents=True, exist_ok=True)
                (ROOT / lang / rel).write_text(page, encoding="utf-8")
                written += 1
        if not check and en != src:
            (ROOT / rel).write_text(en, encoding="utf-8")
    missing = 0
    for lang, cat in cats.items():
        for key, where in cat.missing.items():
            if "--dump" not in sys.argv:
                print("missing %s  %-30s %s" % (lang, where[:30], key[:150]))
            missing += 1
        for key in sorted(set(cat.data) - cat.used):
            if "--dump" not in sys.argv:
                print("unused  %s  %s" % (lang, key[:150]))
    if "--dump" in sys.argv:  # the missing texts as JSON, a skeleton to translate
        todo = {}
        for cat in cats.values():
            for key, where in cat.missing.items():
                todo.setdefault(key, where)
        print(json.dumps(todo, ensure_ascii=False, indent=0))
    print("%d pages written, %d texts missing" % (written, missing), file=sys.stderr)
    sys.exit(1 if check and missing else 0)


if __name__ == "__main__":
    main()
