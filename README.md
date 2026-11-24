# latest
new and article repository

## content
- agenda
- article
- news
- security

Post metadata and URL structure: [templates/README.md](templates/README.md)

## local preview
In VS Code, open this folder and click **Go Live** (Live Server extension by Ritwick Dey); `.vscode/settings.json` mounts the repo at `/latest/`. Or run `./serve.sh`, then open http://localhost:8000/latest/. Pages use `/latest/` paths, so serving the repo root directly or opening files with `file://` leaves the CSS unloaded.

## css
Pages load one file, `assets/css/latest.bundle.css`. Edit the sources instead: `assets/site.css` (the Radova theme) or `assets/base.css` (the Pico rules in use), then run `python3 build.py` and commit the sources and the bundle together.

## check before publishing
Run `python3 -I plan-index/tools/check.py` from the repo root: it finds inline code, unbalanced tags, broken internal links and listing pages over 30 links. `python3 -I plan-index/tools/check.py --dump <file>` prints roughly what `lynx -dump` shows.
