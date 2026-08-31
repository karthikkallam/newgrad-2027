#!/usr/bin/env python3
"""
Pull live new-grad listings from the community trackers, filter to SWE/ML/Quant,
tag anything at a target company, diff against the previous run, and (optionally)
push a phone notification for genuinely new roles.

Runs in GitHub Actions twice a day. No dependencies beyond the stdlib.

Sources (both bot-maintained, both publish date_posted and real requisition URLs):
  - SimplifyJobs/New-Grad-Positions
  - vanshb03/New-Grad-2027
"""

import json, os, re, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

SOURCES = {
    "simplify": "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/.github/scripts/listings.json",
    "vansh":    "https://raw.githubusercontent.com/vanshb03/New-Grad-2027/dev/.github/scripts/listings.json",
}
KEEP_CATEGORIES = {"Software", "Software Engineering", "AI/ML/Data",
                   "Quant", "Data Science, AI & Machine Learning"}

# Titles that are new-grad SWE/ML/quant. Applied only when category is missing.
TITLE_OK = re.compile(
    r"software|engineer|developer|machine learning|\bml\b|\bai\b|research|"
    r"quant|data scien|infrastructure|backend|frontend|full.?stack|systems|platform",
    re.I)
# Roles that are not what we want even if the title matches.
TITLE_NO = re.compile(
    r"\bintern\b|internship|co-?op|technician|installer|field service|sales|"
    r"account executive|recruit|marketing|\bphd\b required|principal|staff engineer|"
    r"senior|sr\.|lead engineer|manager|director|vp\b",
    re.I)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "live_jobs.json")
TARGETS_FILE = os.path.join(ROOT, "targets.json")


def norm(s):
    """Normalize a company name for fuzzy matching."""
    s = (s or "").lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"\b(inc|llc|ltd|corp|corporation|company|co|group|labs?|"
               r"technologies|technology|systems|holdings|the|ai|securities|capital|"
               r"trading|partners|management)\b", " ", s)
    return re.sub(r"[^a-z0-9]", "", s)


def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "newgrad-2027-tracker"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"  attempt {i+1} failed: {e}", file=sys.stderr)
            time.sleep(3 * (i + 1))
    return []


def relevant(job):
    if not job.get("active"):
        return False
    if job.get("is_visible") is False:
        return False
    title = job.get("title") or ""
    if TITLE_NO.search(title):
        return False
    cat = job.get("category")
    if cat:
        return cat in KEEP_CATEGORIES
    return bool(TITLE_OK.search(title))


def main():
    targets = json.load(open(TARGETS_FILE))
    tmap = {norm(n): n for n in targets}

    seen, out = set(), []
    for src, url in SOURCES.items():
        print(f"fetching {src}...")
        data = fetch(url)
        print(f"  {len(data)} rows")
        for j in data:
            if not relevant(j):
                continue
            u = j.get("url") or ""
            if not u or u in seen:
                continue
            seen.add(u)
            cn = j.get("company_name") or ""
            key = norm(cn)
            match = tmap.get(key)
            if not match:  # substring fallback for "Google" vs "Google DeepMind"
                for k, v in tmap.items():
                    if k and len(k) > 4 and (k in key or key in k):
                        match = v
                        break
            locs = j.get("locations") or []
            if isinstance(locs, str):
                locs = [locs]
            out.append({
                "company": cn,
                "target": match,
                "title": j.get("title"),
                "url": u,
                "category": j.get("category") or "Software",
                "locations": locs[:3],
                "sponsorship": j.get("sponsorship"),
                "posted": j.get("date_posted"),
                "updated": j.get("date_updated"),
                "source": src,
            })

    out.sort(key=lambda x: -(x.get("posted") or 0))
    print(f"\n{len(out)} relevant active roles ({sum(1 for x in out if x['target'])} at target companies)")

    # diff against last run
    prev_urls = set()
    if os.path.exists(OUT):
        try:
            prev_urls = {j["url"] for j in json.load(open(OUT))["jobs"]}
        except Exception:
            pass
    new = [j for j in out if j["url"] not in prev_urls]
    new_targets = [j for j in new if j["target"]]
    print(f"{len(new)} new since last run ({len(new_targets)} at target companies)")

    payload = {
        "generated": int(time.time()),
        "generated_iso": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "count": len(out),
        "target_count": sum(1 for x in out if x["target"]),
        "new_urls": [j["url"] for j in new],
        "jobs": out,
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, separators=(",", ":"))
    print(f"wrote {OUT}")

    # notify (only for target companies, only if configured)
    topic = os.environ.get("NTFY_TOPIC")
    if topic and new_targets and prev_urls:
        lines = [f"{j['target']} - {j['title'][:60]}" for j in new_targets[:12]]
        body = "\n".join(lines)
        if len(new_targets) > 12:
            body += f"\n...and {len(new_targets)-12} more"
        try:
            req = urllib.request.Request(
                f"https://ntfy.sh/{topic}",
                data=body.encode("utf-8"),
                headers={
                    "Title": f"{len(new_targets)} new role(s) at your target companies",
                    "Priority": "high" if len(new_targets) > 2 else "default",
                    "Tags": "briefcase",
                    "Click": os.environ.get("SITE_URL", "https://github.com"),
                })
            urllib.request.urlopen(req, timeout=20)
            print(f"notified ntfy.sh/{topic}")
        except Exception as e:
            print(f"notify failed: {e}", file=sys.stderr)

    for j in new_targets[:15]:
        d = datetime.fromtimestamp(j["posted"], timezone.utc).strftime("%Y-%m-%d") if j.get("posted") else "?"
        print(f"  NEW {d}  {j['target'][:22]:<22} {j['title'][:50]}")


if __name__ == "__main__":
    main()
