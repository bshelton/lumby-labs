# Lumby Labs

Static plugin directory, documentation, and support site for Lumby Labs.

## Preview locally

Requires Python 3.10 or later. No package installation is needed.

```sh
python3 build.py
python3 check.py
python3 -m http.server 8080 --directory _site
```

Open http://localhost:8080. Rebuild after editing content, styles, or templates.

## Structure

- `content/`: documentation page fragments.
- `assets/`: stylesheet, wordmark favicon, plugin icon, and an illustrative ledger screenshot.
- `build.py`: shared page layout and directory entries. Add new plugins and guides here.
- `check.py`: generated page and link checks.
- `.github/workflows/pages.yml`: builds, checks, and deploys to GitHub Pages on pushes to main.

The default public URL is https://bshelton.github.io/lumby-labs/. The 404 page uses this project prefix; update it if the hosting path changes. Pages use relative links elsewhere. There is no client-side application framework, analytics, or external font request.

Bug reports for the plugin belong in https://github.com/bshelton/farming-profit/issues. Website feedback belongs in this repository's Issues.

## Artwork

The farming icon and illustrative ledger screenshot come from the Farming Run Profit repository. The screenshot contains synthetic data. The LL favicon is an original geometric lettermark. Lumby Labs is independent of RuneLite and Jagex.

## Public install trends

`trends.py` records the first successful observation each UTC day from
`https://api.runelite.net/pluginhub` in `data/install-history.json`. Missing or
invalid counts fail collection; no zeros or historical values are invented.
The site renders the latest 90 observations as a chart and all observations in a table/JSON download.

The Pages workflow collects at 12:23 UTC daily (GitHub may delay scheduled runs).
Run **Publish site → Run workflow** in Actions to collect manually and deploy.
The same job commits the snapshot and deploys, so it does not depend on a bot
commit triggering another workflow. A failed collection leaves the published
site unchanged; check the last-collected timestamp and workflow failures.

Local checks: `python3 -m unittest discover -s tests`, `python3 build.py`,
`python3 check.py`. Use `python3 trends.py` to collect a real observation.
This collects public aggregate counts only, not player telemetry.
