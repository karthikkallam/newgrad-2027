# Turning on auto-refresh and phone alerts

## 1. Upload these files

Your repo needs this structure:

```
newgrad-2027/
├── index.html
├── live_jobs.json                 (first snapshot, included)
├── scripts/
│   ├── fetch_jobs.py
│   └── targets.json
└── .github/
    └── workflows/
        └── refresh.yml
```

GitHub's web uploader can create folders: on the upload page, type
`scripts/fetch_jobs.py` into the filename box and it makes the folder for you.
Easier: drag the whole folder in — the uploader preserves structure.

## 2. Allow the Action to commit

Settings → Actions → General → Workflow permissions →
**Read and write permissions** → Save.

Without this the workflow runs but cannot push its results.

## 3. Phone notifications (2 minutes)

1. Install **ntfy** (free, no account) — iOS App Store or Google Play.
2. In the app, subscribe to a topic. Pick something unguessable, e.g.
   `karthik-newgrad-x7q2m`. Anyone who knows the topic name can read it,
   so don't use your name alone.
3. In your repo: Settings → Secrets and variables → Actions →
   **New repository secret**
   - Name `NTFY_TOPIC`, value: your topic string
   - Name `SITE_URL`, value: `https://karthikkallam.github.io/newgrad-2027/`

You'll now get a push notification whenever a new role appears at one of your
386 target companies. Nothing fires on the very first run (everything is new
then) — only on genuine changes after that.

## 4. Test it

Actions tab → **Refresh job listings** → Run workflow. Takes about 40 seconds.
Then reload your site and open the **Live feed** tab.

## Schedule

Runs at 08:00 and 18:00 US Central. Change the `cron` lines in
`refresh.yml` to adjust (they're in UTC).

GitHub disables scheduled workflows on repos with no activity for 60 days.
You'll be active, but if listings ever go stale, that's the first thing to check.

## What it actually does

Pulls the SimplifyJobs and vanshb03 tracker JSON — both bot-maintained with
real requisition URLs and posting dates — filters to Software / AI-ML-Data /
Quant, drops internships and senior roles, matches company names against your
target list, diffs against the previous run, and commits the result.

It does **not** scrape company careers pages. Those sit behind bot protection
and would break constantly.
