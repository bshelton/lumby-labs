"""Collect public Hub counts and render an accessible, static history chart."""
import json
import math
from datetime import datetime, timezone, date
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / 'data/install-history.json'
SOURCE = 'https://api.runelite.net/pluginhub'
PLUGIN = 'farming-profit-tracker'


def validate(rows):
    previous = ''
    for row in rows:
        day = row['date']
        assert date.fromisoformat(day).isoformat() == day and day > previous, 'Dates must be unique and sorted'
        assert type(row['count']) is int and row['count'] >= 0, 'Invalid count'
        stamp = datetime.fromisoformat(row['observed_at'])
        assert stamp.utcoffset() is not None and stamp.astimezone(timezone.utc).date().isoformat() == day
        previous = day
    return rows


def record(rows, payload, now):
    validate(rows)
    if not isinstance(payload, dict) or type(payload.get(PLUGIN)) is not int or payload[PLUGIN] < 0:
        raise ValueError('Hub response has no valid plugin count; history was not changed')
    day = now.astimezone(timezone.utc).date().isoformat()
    if rows and day <= rows[-1]['date']:
        return rows  # Preserve the first successful observation each UTC day.
    return rows + [{'date': day, 'count': payload[PLUGIN], 'observed_at': now.astimezone(timezone.utc).isoformat(timespec='seconds')}]


def collect():
    rows = json.loads(HISTORY.read_text()) if HISTORY.exists() else []
    request = Request(SOURCE, headers={'User-Agent': 'LumbyLabs-install-trends/1.0'})
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    updated = record(rows, payload, datetime.now(timezone.utc))
    validate(updated)
    HISTORY.parent.mkdir(exist_ok=True)
    temp = HISTORY.with_suffix('.tmp')
    temp.write_text(json.dumps(updated, indent=2) + '\n')
    temp.replace(HISTORY)
    print(f"Recorded {updated[-1]['date']}: {updated[-1]['count']} active installs")


def render(rows):
    validate(rows)
    intro = '<h1>Install trends</h1><p class="lead">Farming Run Profit’s public Plugin Hub count, recorded once a day.</p>'
    if not rows:
        return intro + '<p>No snapshots collected yet.</p>'
    latest = rows[-1]
    change = latest['count'] - rows[0]['count']
    summary = f'<p><strong>{latest["count"]:,} active installs</strong> at the latest snapshot. '
    summary += (f'{change:+,} since {rows[0]["date"]}.' if len(rows)>1 else 'This is the first snapshot; a trend needs at least two days.') + '</p>'
    shown = rows[-90:]
    top = max(1, math.ceil(max(r['count'] for r in shown) / 4)) * 4
    start = date.fromisoformat(shown[0]['date']).toordinal()
    span = max(1, date.fromisoformat(shown[-1]['date']).toordinal() - start)
    def point(row):
        x = 48 + (date.fromisoformat(row['date']).toordinal()-start)/span*620 if len(shown)>1 else 358
        return x, 210-row['count']/top*170
    svg = '<svg class="trend-chart" viewBox="0 0 720 260" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Recorded active installs</title><desc id="chart-desc">Daily observations over the latest 90 recorded days. Exact values are in the snapshot table below. Gaps mean no observation.</desc>'
    for value in range(0,top+1,top//4):
        y=210-value/top*170
        svg += f'<path class="chart-grid" d="M48 {y} H668"/><text x="36" y="{y+5}" text-anchor="end">{value}</text>'
    for a,b in zip(shown,shown[1:]):
        if (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days == 1:
            x,y=point(a); xx,yy=point(b)
            svg+=f'<path class="chart-line" d="M{x} {y} L{xx} {yy}"/>'
    for row in shown:
        x,y=point(row)
        svg+=f'<circle class="chart-point" cx="{x}" cy="{y}" r="4"><title>{row["date"]}: {row["count"]} active installs</title></circle>'
    svg+=f'<text x="48" y="244">{shown[0]["date"]}</text>'
    if len(shown)>1: svg+=f'<text x="668" y="244" text-anchor="end">{latest["date"]}</text>'
    svg+='</svg>'
    table=''.join(f'<tr><td>{r["date"]}</td><td>{r["count"]:,}</td></tr>' for r in reversed(rows))
    return intro+summary+f'<p class="quiet">Last collected: {latest["observed_at"][:16].replace("T"," ")} UTC. Scheduled daily; updates may be delayed.</p>'+svg+'''<h2>What this tells us</h2><p>These are RuneLite’s reported active installs, not unique people, total downloads, or completed farming runs. Changes show net movement in the reported count, not exact new installs or uninstalls. Collection starts with our first snapshot; earlier history is unavailable.</p><p>Only the public count is collected. No player data or plugin telemetry is sent to Lumby Labs. Failed collections leave gaps rather than recording zero.</p><p><a href="https://api.runelite.net/pluginhub">Public data source</a> · <a href="{{root}}data/install-history.json">Download all snapshots (JSON)</a></p><h2>Daily snapshots</h2><div class="snapshot-table table-wrap"><table><caption>First successful observation per UTC day</caption><thead><tr><th scope="col">Date (UTC)</th><th scope="col">Active installs</th></tr></thead><tbody>'''+table+'</tbody></table></div>'

if __name__ == '__main__':
    collect()
