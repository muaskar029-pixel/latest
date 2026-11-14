# Content metadata standard

Every post is a static HTML file at `latest/<type>/<slug>/index.html`.
`<type>` is one of `agenda`, `article`, `news`, `security`.

## URL structure

| URL | File |
|---|---|
| `/latest/` | `latest/index.html` |
| `/latest/<type>/` | `latest/<type>/index.html` |
| `/latest/<type>/page/<number>/` | `latest/<type>/page/<number>/index.html` |
| `/latest/<type>/<slug>/` | `latest/<type>/<slug>/index.html` |

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

1. Copy the matching template to `latest/<type>/<slug>/index.html` and replace every `{{...}}`. `{{Type}}`/`{{Status}}`/`{{Severity}}` are the capitalised display forms; `*_text` is the human date, e.g. `5 Dec 2026, 19:00`.
2. Add the post to the top of `latest/<type>/index.html`. When that list passes 10 items, move the oldest into `latest/<type>/page/2/` (and so on) and add the pagination nav.
3. Add it to the top of `latest/index.html` and drop the 11th item there.
4. Agenda only: copy `templates/event.ics` to `latest/agenda/<slug>/<slug>.ics` for the "Add to calendar (.ics)" link and fill it in. Times are UTC in `YYYYMMDDTHHMMSSZ` form (WIB minus 7 hours: 19:00 WIB on 5 Dec 2026 is `20261205T120000Z`); drop the `DTEND` line if there is no end time. Keep the CRLF line endings.
5. Agenda only: `latest/agenda/index.html` has two lists. **Upcoming** is sorted by `start_time`, soonest first; **Past Events** is sorted by `start_time`, newest first. Move events from Upcoming to Past by hand once they end.

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
| `.button` | One primary action (e.g. Register now) |
| `.pager` | Previous / Next bar for pagination and post navigation |
| `.empty-state` | Notice for a category or Agenda section with nothing published |
| `.sep` | ` · ` separator: read in Lynx, hidden on screen |

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

Empty states (category with no posts, followed by the "See all latest updates" link):

| Category | Copy |
|---|---|
| Agenda | No events have been scheduled yet. |
| Article | No articles have been published yet. |
| News | No news has been published yet. |
| Security | No security advisories have been published yet. |

An empty Agenda section uses "No upcoming events yet." or "No past events yet." without a link.
