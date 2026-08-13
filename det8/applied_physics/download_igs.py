"""
DET v8.0 — Applied Physics: Automated IGS Clock-Product Downloader

Downloads IGS combined clock products from CDDIS (NASA) using Earthdata auth.

The modern CDDIS products use RINEX 3 long filenames, gzip, year+day-of-year:

    gnss/products/<GPSweek>/IGS0<PRODUCT>_<YYYY><DOY>0000_01D_30S_CLK.CLK.gz

  PRODUCT: OPSFIN (operational final, default) · DEMFIN (Repro3 final) ·
           OPSRAP (operational rapid)
  SAMPLING: 30S (default) · 05M

PREREQUISITE (one-time, done by YOU — the assistant never sees your password):

    cat > ~/.netrc <<'EOF'
    machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD
    EOF
    chmod 600 ~/.netrc

Then:

    python3 -m det8.applied_physics.download_igs --start-date 2023-01-01 --end-date 2023-12-31 --dry-run
    python3 -m det8.applied_physics.download_igs --start-date 2023-01-01 --end-date 2023-12-31
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


def day_of_year(year: int, month: int, day: int) -> int:
    """Day of year (1-366) for a calendar date."""
    d = datetime.date(year, month, day)
    return d.timetuple().tm_yday


def clock_url(year: int, month: int, day: int,
              product: str = "OPSFIN", sampling: str = "30S") -> str:
    """CDDIS URL for the IGS combined clock product of a given day.

    Directory is keyed by GPS week; the filename is keyed by year + day-of-year.
    """
    week = gps_week(year, month, day)
    doy = day_of_year(year, month, day)
    return (f"{CDDIS_PRODUCTS}/{week}/IGS0{product}_"
            f"{year}{doy:03d}0000_01D_{sampling}_CLK.CLK.gz")


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


def download_day(year: int, month: int, day: int,
                 product: str = "OPSFIN", sampling: str = "30S",
                 dest: str = DEFAULT_DEST, dry_run: bool = False) -> dict:
    """Download the combined clock file for one calendar day."""
    url = clock_url(year, month, day, product, sampling)
    if dry_run:
        return {"url": url, "ok": None, "error": "dry-run"}
    return _download_one(url, dest)


def download_range(start_date: datetime.date, end_date: datetime.date,
                   product: str = "OPSFIN", sampling: str = "30S",
                   dest: str = DEFAULT_DEST, dry_run: bool = False) -> list[dict]:
    """Download combined clock products for an inclusive date range."""
    results = []
    d = start_date
    while d <= end_date:
        results.append(download_day(d.year, d.month, d.day, product, sampling, dest, dry_run))
        d += datetime.timedelta(days=1)
    return results


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Download IGS combined clock products from CDDIS.")
    p.add_argument("--start-date", help="YYYY-MM-DD (inclusive)")
    p.add_argument("--end-date", help="YYYY-MM-DD (inclusive; defaults to start-date)")
    p.add_argument("--product", default="OPSFIN",
                   choices=["OPSFIN", "DEMFIN", "OPSRAP"],
                   help="combined product type (default OPSFIN)")
    p.add_argument("--sampling", default="30S", choices=["30S", "05M"],
                   help="sampling rate (default 30S)")
    p.add_argument("--dest", default=DEFAULT_DEST, help="output directory")
    p.add_argument("--dry-run", action="store_true", help="print URLs, do not download")
    args = p.parse_args(argv)

    if not args.start_date:
        p.error("provide --start-date (and optional --end-date)")

    start = datetime.date.fromisoformat(args.start_date)
    end = datetime.date.fromisoformat(args.end_date) if args.end_date else start

    if not os.path.exists(NETRC):
        print("ERROR: ~/.netrc not found. Create it first (see module docstring).")
        return 1

    print(f"Dates {start} → {end}, product {args.product}, sampling {args.sampling}, "
          f"dest {args.dest} {'(dry-run)' if args.dry_run else ''}")
    results = download_range(start, end, args.product, args.sampling, args.dest, args.dry_run)
    if args.dry_run:
        for r in results:
            print(f"  {r['url']}")
        print(f"dry-run: {len(results)} URLs listed (nothing downloaded).")
        return 0
    ok = sum(1 for r in results if r["ok"])
    print(f"{ok}/{len(results)} files OK.")
    for r in results:
        if r["ok"] is False:
            print(f"  FAILED {r['url']}\n    {r['error']}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
