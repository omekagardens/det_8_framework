"""
DET v8.0 — Applied Physics: Automated IGS Clock-Product Downloader

Downloads IGS clock products (`.clk.Z`) from CDDIS (NASA) for a range of GPS
weeks, using Earthdata authentication.

PREREQUISITE (one-time, done by YOU — the assistant never sees your password):

    cat > ~/.netrc <<'EOF'
    machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD
    EOF
    chmod 600 ~/.netrc

Then run (dry-run first to see the URLs):

    python3 -m det8.applied_physics.download_igs --start 2279 --end 2280 --dry-run
    python3 -m det8.applied_physics.download_igs --start 2279 --end 2280

The script calls `curl` with `--netrc-file` and a session-cookie jar; credentials
come ONLY from `~/.netrc` (never hardcoded, never on the command line).

Products: `igc` = combined clock (default), `igs` = final, `igr` = rapid,
`igu` = ultra-rapid.
"""

from __future__ import annotations

import argparse
import datetime
import os
import subprocess


CDDIS_PRODUCTS = "https://cddis.nasa.gov/archive/gnss/products"
DEFAULT_DEST = "det8/data/igs"
NETRC = os.path.expanduser("~/.netrc")
COOKIE_JAR = os.path.expanduser("~/.urs_cookies")


def gps_week(year: int, month: int, day: int) -> int:
    """GPS week number for a calendar date (GPS epoch = 1980-01-06, Sunday)."""
    gps_epoch = datetime.date(1980, 1, 6)
    d = datetime.date(year, month, day)
    return (d - gps_epoch).days // 7


def current_gps_week() -> int:
    """GPS week for today."""
    today = datetime.date.today()
    return gps_week(today.year, today.month, today.day)


def clock_url(week: int, day: int, prefix: str = "igc") -> str:
    """CDDIS URL for a daily clock product.

    day is the day-of-week (0 = Sunday … 6 = Saturday).
    """
    return f"{CDDIS_PRODUCTS}/{week}/{prefix}{week}{day}.clk.Z"


def _download_one(url: str, dest_dir: str) -> dict:
    os.makedirs(dest_dir, exist_ok=True)
    out = os.path.join(dest_dir, os.path.basename(url))
    cmd = [
        "curl", "-L", "--fail", "--silent", "--show-error",
        "--netrc-file", NETRC,
        "--cookie-jar", COOKIE_JAR,
        "--cookie", COOKIE_JAR,
        "-o", out,
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 0
    return {"url": url, "ok": ok,
            "error": "" if ok else r.stderr.strip()[:200]}


def download_week(week: int, prefix: str = "igc",
                  dest: str = DEFAULT_DEST, dry_run: bool = False) -> list[dict]:
    """Download the 7 daily clock files for one GPS week."""
    results = []
    for day in range(7):
        url = clock_url(week, day, prefix)
        if dry_run:
            results.append({"url": url, "ok": None, "error": "dry-run"})
        else:
            results.append(_download_one(url, dest))
    return results


def download_range(start_week: int, end_week: int, prefix: str = "igc",
                   dest: str = DEFAULT_DEST, dry_run: bool = False) -> list[dict]:
    """Download clock products for a range of GPS weeks (inclusive)."""
    results = []
    for week in range(start_week, end_week + 1):
        results.extend(download_week(week, prefix, dest, dry_run))
    return results


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Download IGS clock products from CDDIS.")
    p.add_argument("--start", type=int, help="start GPS week")
    p.add_argument("--end", type=int, help="end GPS week (inclusive)")
    p.add_argument("--date", type=str, help="download the week containing YYYY-MM-DD")
    p.add_argument("--prefix", default="igc",
                   choices=["igc", "igs", "igr", "igu"],
                   help="product type (default igc = combined)")
    p.add_argument("--dest", default=DEFAULT_DEST, help="output directory")
    p.add_argument("--dry-run", action="store_true", help="print URLs, do not download")
    args = p.parse_args(argv)

    if args.date:
        y, m, d = map(int, args.date.split("-"))
        week = gps_week(y, m, d)
        start = end = week
    elif args.start is not None:
        start = args.start
        end = args.end if args.end is not None else args.start
    else:
        p.error("provide --start/--end or --date")

    if not os.path.exists(NETRC):
        print("ERROR: ~/.netrc not found. Create it first (see module docstring).")
        return 1

    print(f"Weeks {start}–{end}, prefix {args.prefix}, dest {args.dest} "
          f"{'(dry-run)' if args.dry_run else ''}")
    results = download_range(start, end, args.prefix, args.dest, args.dry_run)
    ok = sum(1 for r in results if r["ok"])
    print(f"{ok}/{len(results)} files OK.")
    for r in results:
        if r["ok"] is False:
            print(f"  FAILED {r['url']}\n    {r['error']}")
    return 0 if (args.dry_run or ok == len(results)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
