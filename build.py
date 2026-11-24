#!/usr/bin/env python3
"""Build the minified bundle from the readable sources in assets/.

    python3 build.py

assets/base.css + assets/site.css  ->  assets/css/latest.bundle.css

Run it after every edit to a source file and commit both. Standard library only.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")


def _string_end(s, i):
    quote = s[i]
    i += 1
    while s[i] != quote:
        i += 2 if s[i] == "\\" else 1
    return i + 1


def _segments(css):
    """Split CSS into (is_string, text) parts; comments are dropped except /*! licences */."""
    out, buf, i = [], [], 0
    while i < len(css):
        if css[i] in "\"'":
            j = _string_end(css, i)
            out += [(False, "".join(buf)), (True, css[i:j])]
            buf, i = [], j
        elif css.startswith("/*", i):
            j = css.index("*/", i) + 2
            if css.startswith("/*!", i):
                out += [(False, "".join(buf)), (True, css[i:j] + "\n")]
                buf = []
            i = j
        else:
            buf.append(css[i])
            i += 1
    out.append((False, "".join(buf)))
    return out


def minify_css(css):
    """Whitespace and comments only: strings, calc() spaces and selector spaces are kept."""
    out = []
    for is_string, text in _segments(css):
        if not is_string:
            text = re.sub(r"\s+", " ", text)
            text = re.sub(r" ?([{};,>]) ?", r"\1", text)
            text = re.sub(r": ", ":", text)
        out.append(text)
    css = "".join(out).replace(";}", "}")
    return css.strip() + "\n"


def rebase_urls(css, prefix):
    """Relative url()s in assets/*.css point one folder up once bundled into assets/css/."""
    def fix(m):
        quote, path = m.group(1), m.group(2)
        if re.match(r"(data:|/|#|[a-z]+://)", path):
            return m.group(0)
        return "url(%s%s%s%s)" % (quote, prefix, path, quote)
    return re.sub(r"url\(\s*([\"']?)([^\"')]+)\1\s*\)", fix, css)


def _shape(css):
    """Everything that matters to a browser: no comments, no whitespace outside strings."""
    parts = [t if s else re.sub(r"\s+", "", t) for s, t in _segments(css) if not t.startswith("/*!")]
    return "".join(parts).replace(";}", "}")


def build_css(sources, target):
    src = "\n".join(open(os.path.join(ASSETS, f), encoding="utf-8").read() for f in sources)
    src = rebase_urls(src, "../")
    out = minify_css(src)
    # The minifier may only drop whitespace, comments and a final ';' before '}'.
    assert _shape(out) == _shape(src), "minify_css changed the CSS"
    assert out.count("{") == out.count("}"), "unbalanced braces"
    assert out.isascii(), "non-ASCII in bundle: escape it in the source"
    path = os.path.join(ASSETS, target)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("%s  %d -> %d bytes" % (target, len(src), len(out)))


if __name__ == "__main__":
    build_css(["base.css", "site.css"], "css/latest.bundle.css")
