# Content metadata standard

Every post is a static HTML file at `<type>/<slug>/index.html`.
`<type>` is one of `agenda`, `article`, `news`, `security`.

## URL structure

| URL | File |
|---|---|
| `/latest/` | `index.html` |
| `/latest/<type>/` | `<type>/index.html` |
| `/latest/<type>/page/<number>/` | `<type>/page/<number>/index.html` |
| `/latest/<type>/<slug>/` | `<type>/<slug>/index.html` |

## How metadata is stored

Metadata goes in `<head>` as `<meta name="radova:<field>" content="...">`, one tag per field.
Leave out optional fields that have no value; never leave `content` empty.
Dates use ISO 8601 with the WIB offset: `2026-11-14T09:00:00+07:00`.
Lists (`tags`, `affected_versions`, `patched_versions`, `cve`) are comma-separated.

## Standard fields (all types)

| Field | Required | Example |
|---|---|---|
| `title` | yes | `Radova Latest is live` (also used for `<title>` and `<h1>`) |
| `slug` | yes | `radova-latest-is-live` (lowercase, `a-z0-9-`, same as folder name) |
| `date` | yes | `2026-11-14T09:00:00+07:00` (publication date) |
| `summary` | yes | One or two sentences |
| `tags` | yes | `release, community` |

## Agenda fields

| Field | Required | Values |
|---|---|---|
| `start_time` | yes | ISO 8601, `+07:00` |
| `end_time` | no | ISO 8601, `+07:00` |
| `location` | yes | Place name or `Online` |
| `register_url` | no | Absolute URL |
| `status` | yes | `scheduled` or `cancelled` |

## Security fields

| Field | Required | Values |
|---|---|---|
| `advisory_id` | yes | `RSA-YYYY-NNN`, e.g. `RSA-2026-001` |
| `severity` | yes | `low`, `medium`, `high`, `critical` |
| `affected_versions` | yes | e.g. `1.0, 1.1` |
| `patched_versions` | yes | e.g. `1.2`, or `none` while unpatched |
| `cve` | no | e.g. `CVE-2026-12345` |
| `status` | yes | `investigating`, `mitigated`, `resolved`, `informational` |

## Article and News fields

| Field | Required | Values |
|---|---|---|
| `author` | yes (Article, News) | Person or team name, e.g. `Radova Team` |
| `reading_time` | yes (Article only) | Whole minutes: word count / 200, rounded up, minimum 1 |

## Templates

| File | Use for |
|---|---|
| `post.html` | Article and News detail pages |
| `agenda.html` | Agenda detail pages |
| `event.ics` | Calendar file for an Agenda post |
| `security.html` | Security advisory detail pages |
| `listing.html` | Category pages and their `/page/<n>/` pages |

## Publishing a post

1. Copy the matching template to `<type>/<slug>/index.html` and replace every `{{...}}`. `{{Type}}`/`{{Status}}`/`{{Severity}}` are the capitalised display forms; `*_text` is the human date, e.g. `5 Dec 2026, 19:00`.
2. Add the post to the top of `<type>/index.html`. When that list passes 10 items, move the oldest into `<type>/page/2/` (and so on) and add the pagination nav.
3. Update `index.html` (see "`/latest/` page" below):
   - Turn the post that is in `.feature-card` into a grid card and put it first in `ol.card-grid`.
   - Put the new post in `.feature-card`.
   - Keep at most 9 post cards in the grid: delete the last one if needed.
   - If the new post is the first in its category, delete that category's status card.
4. Agenda only: copy `templates/event.ics` to `agenda/<slug>/<slug>.ics` for the "Add to calendar (.ics)" link and fill it in. Times are UTC in `YYYYMMDDTHHMMSSZ` form (WIB minus 7 hours: 19:00 WIB on 5 Dec 2026 is `20261205T120000Z`); drop the `DTEND` line if there is no end time. Keep the CRLF line endings.
5. Agenda only: `agenda/index.html` has two lists. **Upcoming** is sorted by `start_time`, soonest first; **Past Events** is sorted by `start_time`, newest first. Move events from Upcoming to Past by hand once they end.

## Components (classes in `assets/site.css`)

| Class | Used for |
|---|---|
| `.editorial-header` | Listing page header: eyebrow + `<h1>` left, description right |
| `.tab-grid` | Category tabs; mark the current one with `aria-current="page"` |
| `.post-grid` > `.post-row` (`--agenda`, `--article`, `--news`, `--security`) | Listing; `.post-row__main` left, `dl.post-row__panel` right |
| `.single-split` | Detail page: `<header>` with context left, `.editorial-prose` right |
| `.editorial-prose--article` | Adds the drop cap; Article pages only |
| `.meta-dl` | Key/value `<dl>`; `.meta-dl__lead` enlarges one value, `.advisory-id` sets the ID |
| `.badge` + `--type`, `--severity-low/medium/high/critical`, `--scheduled`, `--cancelled` | Labels; the text always states the value |
| `.button` (+ `--navy`, `--small`, `--arrow`) | Pill button for one primary action (e.g. Register now); `--arrow` adds the white arrow circle |
| `.pager` | Previous / Next bar for pagination and post navigation |
| `.empty-state` | Notice for a category or Agenda section with nothing published |
| `.sep` | ` · ` separator: read in Lynx, hidden on screen |
| `.site-header`, `.site-footer`, `.brand-lockup` | Header and footer on every page: logo + RADOVA, Latest, About / Security policy, Source code |
| `.notice-bar` | One-line notice at the top of `/latest/` |
| `.hero-split`, `.chip`, `.check-list` | `/latest/` hero: chips, `<h1>` with one word in `.accent`, check list and button on the left, `.feature-card` on the right |
| `.cover` + `--article`, `--news`, `--agenda`, `--security` | Coloured title tile with the category icon; holds `.cover__kicker`, the title (`h2`, or `p.cover__title` on a status card) and `.cover__summary` |
| `.feature-card` | The newest post, large, in the `/latest/` hero |
| `.card-grid` > `.post-card` | `/latest/` grid: `.cover` + `.byline`, or a status card with `.post-card__link` |
| `.byline` (`.byline__author`) | Author with the Radova logo as avatar, or location / status; then the date |

## UI copy

Buttons and links use sentence case and say what they do. Use these exact labels:

| Where | Label |
|---|---|
| First link on every page | Skip to main content |
| Listing tabs | All Latest, Agenda, Article, News, Security |
| Pager without JS / with JS | ← Previous, Next → / Load more |
| Post navigation | ← Previous: {title}, Next: {title} → |
| Detail page back link | ← Back to Agenda / Articles / News / Security |
| Agenda actions | Register now, Add to calendar (.ics) |
| Empty state and 404 link | See all latest updates, Go to the latest updates |
| Site header and footer | Latest, About / Security policy, Source code |
| `/latest/` notice and hero | Read the policy, Browse all updates |
| `/latest/` status card link | Go to Agenda, Go to Article, Go to News, Go to Security |

Empty states (category with no posts, followed by the "See all latest updates" link):

| Category | Copy |
|---|---|
| Agenda | No events have been scheduled yet. |
| Article | No articles have been published yet. |
| News | No news has been published yet. |
| Security | No security advisories have been published yet. |

An empty Agenda section uses "No upcoming events yet." or "No past events yet." without a link.

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
