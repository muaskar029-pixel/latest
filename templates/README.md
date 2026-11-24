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
   - Put the new post first in `ol.card-grid`. Keep at most 10 post cards in the grid: delete the last one if needed.
   - If the new post is the first in its category, delete that category's status card.
   - Copy the new card (without `data-tags`) to the top of "More updates" on the other detail pages that should list it; keep at most 4 cards there.
4. Agenda only: copy `templates/event.ics` to `agenda/<slug>/<slug>.ics` for the "Add to calendar (.ics)" link and fill it in. Times are UTC in `YYYYMMDDTHHMMSSZ` form (WIB minus 7 hours: 19:00 WIB on 5 Dec 2026 is `20261205T120000Z`); drop the `DTEND` line if there is no end time. Keep the CRLF line endings.
5. Agenda only: `agenda/index.html` has two lists. **Upcoming** is sorted by `start_time`, soonest first; **Past Events** is sorted by `start_time`, newest first. Move events from Upcoming to Past by hand once they end.

## Components (classes in `assets/site.css`)

| Class | Used for |
|---|---|
| `.editorial-header` | Listing page header: `<h1>`, then the description under it |
| `.tab-grid` | Category tabs, icon + text in one row; the current one (`aria-current="page"`) sits in a white pill |
| `.post-search`, `.post-filters` | `/latest/` only: search pill, "Popular" chips and sort above `#post-cards`. Only the search form is in the HTML: without JS it goes to DuckDuckGo on radova.org. With JS (`site.js`) it filters the cards on the page, and `site.js` adds `.post-filters`: up to 6 chips from the cards' most used `data-tags`, and the sort menu |
| `.single` | Detail page in one centred column, like a Dribbble shot: `<header>` (`<h1>`, then `.single__meta`: byline left, one button right), optional `img.single__media` (4:3 photo, `alt=""`), optional `.meta-dl`, `.editorial-prose`, optional `.tag-list` |
| `.tag-list` | The post's tags as pills under the text, one `<li>` per tag |
| `.more-posts` | "More updates" under a detail page: heading, "View all" link, and a `.card-grid` with up to 4 cards of other recent posts |
| `.editorial-prose--article` | Adds the drop cap; Article pages only |
| `.meta-dl` | Key/value `<dl>`; `.meta-dl__lead` enlarges one value, `.advisory-id` sets the ID |
| `.badge` + `--type`, `--severity-low/medium/high/critical`, `--scheduled`, `--cancelled` | Labels; the text always states the value |
| `.button` (+ `--navy`, `--outline`, `--small`, `--arrow`) | Pill button for one primary action (e.g. Register now); `--outline` is the navy outline button for a secondary link; `--arrow` adds the white arrow circle |
| `.pager` | Previous / Next bar for pagination and post navigation |
| `.empty-state` | Notice for a category or Agenda section with nothing published |
| `.sep` | ` · ` separator: read in Lynx, hidden on screen |
| `.site-header`, `.site-footer`, `.brand-lockup` | Header and footer on every page, the same markup everywhere. Header, in this order: logo, site menu (Latest, Resources, About, Contact), search, "Get Radova" (`.site-header__cta`). Footer: logo, Security policy, Source code |
| `.notice-bar` | One-line notice at the top of `/latest/` |
| `.hero-split`, `.chip`, `.check-list` | `/latest/` hero: chips, `<h1>` with one word in `.accent`, check list and button on the left, `.hero-media` on the right |
| `.cover` + `--article`, `--news`, `--agenda`, `--security` | Coloured title tile with the category icon; holds `.cover__kicker`, and the title (`h2`, or `p.cover__title` on a status card) |
| `.hero-media` | `/latest/` hero: the app clips in `assets/hero/` (one `<video preload="none">` each, with `data-app` and `data-word`; only the first has `poster`, the others `data-poster`, set by `site.js`), played in turn by `site.js`; the `<h1>` words in `.hero-words__track` follow the clips in the same order (`.is-current`); not a post |
| `.card-grid` > `.post-card` | Post grid on `/latest/`, the category pages and "More updates": `.cover` + `.byline`, or a status card with `.post-card__link` (`/latest/` only) |
| `.byline` (`.byline__author`) | Author with the Radova logo as avatar, or location / status; then the date |

## UI copy

Buttons and links use sentence case and say what they do. Use these exact labels:

| Where | Label |
|---|---|
| First link on every page | Skip to main content |
| Listing tabs | All Latest, Agenda, Article, News, Security |
| Pager without JS / with JS | ← Previous, Next → / Load more |
| Post navigation | ← Previous: {title}, Next: {title} → |
| Detail page | All articles, All news, All advisories (button in the byline row); More updates, View all |
| Agenda actions | Register now, Add to calendar (.ics) |
| Empty state and 404 link | See all latest updates, Go to the latest updates |
| Site header and footer | Latest, Resources, About, Contact, Get Radova / Security policy, Source code |
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

The page shows the 10 newest posts of all types in `ol.card-grid`, newest first. The hero holds the app clips (`.hero-media`), not a post.
After the post cards, the grid has one status card for each category that has no posts yet.

Grid card, one `<li>` per post (here an Article):

```html
<li data-tags="{{tags}}">
  <article class="post-card">
    <div class="cover cover--article">
      <p class="cover__kicker"><span class="badge badge--type">Article</span><span class="sep"> · </span><span>{{reading_time}} min read</span></p>
      <h2><a href="/latest/article/{{slug}}/">{{title}}</a></h2>
    </div>
    <p class="byline"><span class="byline__author">{{author}}</span><span class="sep"> · </span><time datetime="{{date}}">{{date_text}}</time></p>
  </article>
</li>
```

Thumbnail (optional): add `cover--image` to the cover and, as its first child, `<img class="cover__image" src="{{image}}" alt="" width="960" height="720" loading="lazy">`. Use a 4:3 photo, at least 960x720, under 100 KB. `alt` stays empty: the title already names the post.

`data-tags` copies the post's `radova:tags`; the search above the grid matches the card text and these tags, and the "Popular" chips are made from them.

Per type, change the cover class, the end of the kicker and the byline:

| Type | Cover class | Kicker after the type badge | Byline |
|---|---|---|---|
| Article | `cover--article` | `<span class="sep"> · </span><span>{{reading_time}} min read</span>` | `<span class="byline__author">{{author}}</span>`, then the date |
| News | `cover--news` | nothing | `<span class="byline__author">{{author}}</span>`, then the date |
| Agenda | `cover--agenda` | `<span class="sep"> · </span><span class="badge badge--{{status}}">Status: {{Status}}</span>` | `<span>{{location}}</span>`, then `<time datetime="{{start_time}}">{{start_text}} WIB</time>` |
| Security | `cover--security` | `<span class="sep"> · </span><span class="advisory-id">{{advisory_id}}</span><span class="sep"> · </span><span class="badge badge--severity-{{severity}}">Severity: {{Severity}}</span>` | `<span>Status: {{Status}}</span>`, then the date |

Status card, with a short line ("No events yet.", "No articles yet.", "No news yet.", "No advisories yet."); delete it when the category gets its first post:

```html
<li>
  <div class="post-card">
    <div class="cover cover--agenda">
      <p class="cover__kicker"><span class="badge badge--type">Agenda</span></p>
      <p class="cover__title">No events yet.</p>
    </div>
    <p class="post-card__link"><a href="/latest/agenda/">Go to Agenda</a></p>
  </div>
</li>
```
