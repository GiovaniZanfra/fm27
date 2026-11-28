"""Which raw export a team's interim data was parsed from (data/<team>/interim/source.json)."""
import json
import re
from datetime import datetime
from pathlib import Path

LABEL_RE = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}")


def latest_raw(team_raw_dir):
    """Newest export in `team_raw_dir`: the max file named YYYY-MM-DD_HH-MM-SS.html (by name),
    else the most recently modified HTML (legacy names). None if there is no HTML file."""
    team_raw_dir = Path(team_raw_dir)
    stamped = sorted(p for p in team_raw_dir.glob("*.html") if LABEL_RE.fullmatch(p.stem))
    if stamped:
        return stamped[-1]
    legacy = sorted(team_raw_dir.glob("*.html"), key=lambda p: p.stat().st_mtime)
    return legacy[-1] if legacy else None


def source_path(team, data_dir="data"):
    return Path(data_dir) / team / "interim" / "source.json"


def write_source(team, html_file, data_dir="data"):
    html_file = Path(html_file)
    path = source_path(team, data_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    info = {"label": html_file.stem, "file": str(html_file),
            "parsed_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    path.write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return info


def read_source(team, data_dir="data"):
    """The source.json dict, or None if missing/unreadable."""
    try:
        return json.loads(source_path(team, data_dir).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def export_label(team, data_dir="data"):
    info = read_source(team, data_dir)
    return info.get("label", "unknown") if info else "unknown"
