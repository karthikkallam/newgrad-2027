# New Grad 2027 — Application Desk

A single-file tracker for the 2027 new grad SWE / ML recruiting cycle.
**386 companies** across big tech, AI labs, quant, fintech, infra, security,
robotics, aerospace, bio, gaming, crypto, and international.

**[Live site →](https://YOURUSERNAME.github.io/newgrad-2027/)**

## Why this exists

For a May 2027 graduate, the usual advice is wrong. Summer 2027 falls *after*
graduation, and most FAANG internships require you to return to school —
Meta's summer 2027 postings ask for a Dec 2027–Jun 2029 graduation date, and
Google's require active enrollment. The actual target is **full-time new grad
roles with 2027 start dates**, and that cycle opens in August, not spring.

This tracks that cycle.

## Features

- **Focus mode** — keyboard-driven queue. `O` open, `A` applied, `S` skip,
  `K` star, `←` back. Built for volume without context switching.
- **Answer vault** — fill your work authorization, graduation date, project
  blurbs and referral template once; copy any field with one click.
- **Follow-up detection** — anything sitting at "applied" for 7+ days gets
  flagged automatically.
- **Funnel metrics** — applied → OA → interview → offer, plus response rate.
  Under 3% after 200 applications means the résumé is the problem, not volume.
- **Notes per company** — req numbers, recruiter names, OA deadlines, referrals.
- **Import / export** — CSV for spreadsheets, JSON for full backup and restore.

## Timing flags

| Flag | Meaning |
|---|---|
| `open ✓` | Verified against a live posting on 31 Aug 2026 |
| `apply now` | Cycle open per the company's own stated window |
| `unverified` | Not checked this cycle — historical pattern only, confirm on the posting |
| `rolling` | No structured new grad program; portfolio-driven hiring |

Only 18 companies carry `open ✓`. The rest are best-effort and should be
confirmed before you rely on the timing.

## Your data

Everything is stored in your browser's `localStorage`. Nothing is uploaded,
nothing is transmitted, there is no backend. Clearing site data wipes it, so
export a JSON backup weekly.

**Do not commit your exported backup** — it contains your phone number,
address and notes. `.gitignore` already covers `*.json`.

## Links

Entries point to **careers pages, not individual requisitions**. Req URLs rot
within weeks as roles fill and get reposted; careers pages stay valid all
season. Land on one and filter for "2027" or "new grad".

For live requisition-level links, these update within hours:

- [vanshb03/New-Grad-2027](https://github.com/vanshb03/New-Grad-2027)
- [SimplifyJobs/New-Grad-Positions](https://github.com/SimplifyJobs/New-Grad-Positions)
- [speedyapply/2027-SWE-College-Jobs](https://github.com/speedyapply/2027-SWE-College-Jobs)
- [zapplyjobs/New-Grad-Jobs-2027](https://github.com/zapplyjobs/New-Grad-Jobs-2027)
- [northwesternfintech/2027QuantInternships](https://github.com/northwesternfintech/2027QuantInternships)

Subscribe to their `.atom` commit feeds and you'll see postings the day they go up.

## Run locally

No build step, no dependencies.

```bash
git clone https://github.com/YOURUSERNAME/newgrad-2027.git
cd newgrad-2027
open index.html      # or: python3 -m http.server 8000
```

## Contributing

Found a dead link or a company that should be here? Open an issue or a PR —
company data lives in the `const D=[...]` array at the top of the script in
`index.html`. Format: `["Name","Category","Role note","timing","url"]`.

## License

MIT
