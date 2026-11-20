"""Langkah 5: dokumentasikan komponen dan cara mengisi halaman index di templates/README.md (jalankan dari root repo)."""
import pathlib
import sys

ROOT = pathlib.Path(".")
README = ROOT / "templates/README.md"
if not README.is_file() or not (ROOT / "plan-index").is_dir():
    sys.exit("Jalankan dari root repo: python3 -I plan-index/tools/step5.py")


def replace_once(text, old, new, where):
    count = text.count(old)
    if count != 1:
        sys.exit(f"README ({where}): teks yang dicari muncul {count} kali, harusnya 1. Berhenti dan laporkan ke user.")
    return text.replace(old, new)


text = README.read_text()
if "## `/latest/` page" in text:
    sys.exit("Langkah 5 sudah pernah dijalankan.")
if "<<<<<<<" in text:
    sys.exit("README masih berisi penanda konflik: jalankan Langkah 1 dulu.")

text = replace_once(text, "3. Add it to the top of `index.html` and drop the 11th item there.\n", """3. Update `index.html` (see "`/latest/` page" below):
   - Turn the post that is in `.feature-card` into a grid card and put it first in `ol.card-grid`.
   - Put the new post in `.feature-card`.
   - Keep at most 9 post cards in the grid: delete the last one if needed.
   - If the new post is the first in its category, delete that category's status card.
""", "publishing step 3")

text = replace_once(text, "| `.button` | One primary action (e.g. Register now) |\n",
                    "| `.button` (+ `--navy`, `--small`, `--arrow`) | Pill button for one primary action (e.g. Register now); `--arrow` adds the white arrow circle |\n",
                    "button row")

text = replace_once(text, "| `.sep` | ` · ` separator: read in Lynx, hidden on screen |\n", """| `.sep` | ` · ` separator: read in Lynx, hidden on screen |
| `.site-header`, `.site-footer`, `.brand-lockup` | Header and footer on every page: logo + RADOVA, Latest, About / Security policy, Source code |
| `.notice-bar` | One-line notice at the top of `/latest/` |
| `.hero-split`, `.chip`, `.check-list` | `/latest/` hero: chips, `<h1>` with one word in `.accent`, check list and button on the left, `.feature-card` on the right |
| `.cover` + `--article`, `--news`, `--agenda`, `--security` | Coloured title tile with the category icon; holds `.cover__kicker`, the title (`h2`, or `p.cover__title` on a status card) and `.cover__summary` |
| `.feature-card` | The newest post, large, in the `/latest/` hero |
| `.card-grid` > `.post-card` | `/latest/` grid: `.cover` + `.byline`, or a status card with `.post-card__link` |
| `.byline` (`.byline__author`) | Author with the Radova logo as avatar, or location / status; then the date |
""", "components rows")

text = replace_once(text, "| Empty state and 404 link | See all latest updates, Go to the latest updates |\n", """| Empty state and 404 link | See all latest updates, Go to the latest updates |
| Site header and footer | Latest, About / Security policy, Source code |
| `/latest/` notice and hero | Read the policy, Browse all updates |
| `/latest/` status card link | Go to Agenda, Go to Article, Go to News, Go to Security |
""", "UI copy rows")

text = text.rstrip("\n") + "\n" + '''
## `/latest/` page (`index.html`)

The page shows the 10 newest posts of all types: the newest in the hero (`.feature-card`), the next 9 in `ol.card-grid`.
After the post cards, the grid has one status card for each category that has no posts yet.

Grid card, one `<li>` per post (here an Article):

```html
<li>
  <article class="post-card">
    <div class="cover cover--article">
      <p class="cover__kicker"><span class="badge badge--type">Article</span><span class="sep"> · </span><span>{{reading_time}} min read</span></p>
      <h2><a href="/latest/article/{{slug}}/">{{title}}</a></h2>
      <p class="cover__summary">{{summary}}</p>
    </div>
    <p class="byline"><span class="byline__author">{{author}}</span><span class="sep"> · </span><time datetime="{{date}}">{{date_text}}</time></p>
  </article>
</li>
```

Per type, change the cover class, the end of the kicker and the byline:

| Type | Cover class | Kicker after the type badge | Byline |
|---|---|---|---|
| Article | `cover--article` | `<span class="sep"> · </span><span>{{reading_time}} min read</span>` | `<span class="byline__author">{{author}}</span>`, then the date |
| News | `cover--news` | nothing | `<span class="byline__author">{{author}}</span>`, then the date |
| Agenda | `cover--agenda` | `<span class="sep"> · </span><span class="badge badge--{{status}}">Status: {{Status}}</span>` | `<span>{{location}}</span>`, then `<time datetime="{{start_time}}">{{start_text}} WIB</time>` |
| Security | `cover--security` | `<span class="sep"> · </span><span class="advisory-id">{{advisory_id}}</span><span class="sep"> · </span><span class="badge badge--severity-{{severity}}">Severity: {{Severity}}</span>` | `<span>Status: {{Status}}</span>`, then the date |

Feature card: the same cover, kicker and byline as the grid card, inside `<article class="feature-card">` (no `<li>`),
with `<span class="sep"> · </span><span>Newest</span>` at the end of the kicker.

Status card, using the line from the empty-state table above; delete it when the category gets its first post:

```html
<li>
  <div class="post-card">
    <div class="cover cover--agenda">
      <p class="cover__kicker"><span class="badge badge--type">Agenda</span></p>
      <p class="cover__title">No events have been scheduled yet.</p>
    </div>
    <p class="post-card__link"><a href="/latest/agenda/">Go to Agenda</a></p>
  </div>
</li>
```
'''
README.write_text(text)
print("Langkah 5 selesai: templates/README.md diperbarui.")
