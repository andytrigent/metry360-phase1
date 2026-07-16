# CURRENT STATE — SOJPE C2H Phase 1 (as of 2026-07-16)

Handoff doc for a new session. Read alongside `../CLAUDE.md` (business rules, metric formulas, 83-step spec) and `README.md` (architecture, API reference, deploy steps).

## One-paragraph summary

The app is **fully data-driven end-to-end**: upload 7 raw Excel files in the browser → stored in S3 + DynamoDB → data period auto-detected from file contents → `/api/dashboard-data` parses the files (pure-stdlib xlsx parser in Lambda) and aggregates AM-level metrics → all 5 dashboard views, alerts, KPI cards, donut chart, and CSV export render from that API. Week sidebar items are the Fridays of the data month; clicking one loads that week's report or an honest empty state. **Nothing user-visible is static anymore.**

## ⚠️ FIRST THING: NOT deployed to Vercel — everything recent is LOCAL only

- All recent work (data-driven views, real upload page, typo fix, static-content removal) is **NOT deployed to Vercel production**. It exists only in the local working copy / local commits. Production still serves: the "ScorecCard" typo, the FAKE simulation upload page, and static sample views.
- **Branch rule: everything must be merged and pushed to `main` ONLY** — no long-lived side branches. If work was done in a worktree or any other branch, merge it into `main` first, push `main` to GitHub (`git push origin main`), and deploy from there.
- Before deploying, check for unpushed/unmerged work: `git status`, `git log origin/main..HEAD`, and `git worktree list`. (As of 2026-07-16 there is a single worktree and only the `main` branch; all local commits have been pushed to `origin/main`. GitHub pushes do NOT auto-deploy Vercel.)
- Deploy = `vercel --prod --yes` from repo root, **only after the user gives the go** (they have been explicitly holding deploys to evaluate locally first).
- The backend Lambda IS current in AWS (deployed separately). Only the Vercel frontend is stale.
- Until deployed, do not ask Akash to upload in prod — the prod upload page silently discards files.

## Infrastructure (all live, region ap-south-1, account 302954730716)

- Frontend: Vercel `metry360-phase1` → https://metry360.arkos.studio ; `vercel.json` rewrites `/api/*` → API Gateway `2g852sgu1i` stage `prod` (`/api/health` + `/api/{proxy+}` catch-all)
- Lambda `sojpe-data-pipeline` (python3.11). Source `backend/lambda_handler.py`, handler is `index.lambda_handler` → **zip the file as `index.py`** to deploy
- S3 `trigent-c2h-files` (`reports/{report_id}/…`), DynamoDB `sojpe-reports` (key `report_id`)
- AWS CLI: user must run `aws login` (sessions expire mid-work; ask them to type `! aws login`)
- Local dev: `python <scratchpad>/local_server.py` → http://127.0.0.1:8123 — serves `public/` + proxies `/api/*` to the real AWS backend (also serves test raw files at `/rawfiles/`)

## Data currently in the system (real)

| Report | Data week | Contents |
|--------|-----------|----------|
| REPORT-718RPGZXPF3 | **Ending 10-Jul-2026** (06–10 Jul) | July week-2 files from `../Raw reports used for SOJPE/July Week 2/` — uploaded via the real browser flow |
| REPORT-3DDF59BC5F60 | Ending 29-May-2026 (25–29 May) | Repo's original raw files — Andy's verification upload |

July data facts: 5,166 positions, 45.3% coverage, avg sub 4.25, 32 selections, 32 joiners, 22 exits; **5 director groups**: Sanjib Saha, Sajja Jyosthna Devi (=Jyothsna), Manisha Jishtu, **Sivaranjani** (not in any old hardcoded org!), plus "Unassigned" (939 positions with no AM — real data-quality issue to raise with Rhoni/Akash).

## Key history (why things are the way they are)

- Before 2026-07-10 **no upload ever reached AWS** (no gateway route + upload page sent names only + Lambda was a mock). Then discovered `upload.html` — the page all buttons linked to — was a **pure simulation** (`simulateProcessing()`, fake success, zero network calls). That's why Akash's uploads kept "vanishing". `upload.html` is now the real base64 uploader (identical to `upload-new.html`).
- Reporting periods come from **inside the files** (`Period: dd/mm/yy To dd/mm/yy` in Selects/Renege; Joiners From/To fallback) — never the upload date. Weeks display as "Ending 10-Jul" (Friday), never week numbers. These are hard user requirements.
- File matching is keyword-based (`coverage`, `select`, `renege`, `joiner`, `exit`, `staffing`, `submission/avg sub`) because Akash's real files have names like `Coveragejuly.xlsx`, `Exit.xlsx`.

## What works (verified in Chrome, local)

Upload (7 files, browser) · Report History from API (data week + upload time + file list + Reprocess) · `/api/reporting-period` (source: data_period) · `/api/dashboard-data` (per-AM Coverage/Selects/Renege/Joiners/Exits, director grouping, RAG) · all 5 views + alerts + chart + export from data · week-scoped dashboard with empty states · landing page API status.

## Honest gaps / next work (priority order)

1. **Deploy to prod** (see above).
2. **Select % & Target Selects**: need monthly-target Config (per AM) + stateful weekly pacing snapshots (CLAUDE.md formula). Currently "—".
3. **Offers**: no Ceipal report exists; manual. Currently "—".
4. **Submissions file** (recruiter-level, multi-sheet) and **Staffing file** (Closing HC, YTJ-M/YTE-M, Avg Billing → RPR, revenue) not yet aggregated into dashboard-data.
5. AM→Director mapping comes only from Coverage's BU Head; AMs missing there land in "Unassigned". Canonical AM name master (Config) still needed — TRIM is applied but no alias mapping.
6. Approval workflow buttons "Mark for Review"/"Download Files" are visual only (`/approve` + `/reprocess` endpoints exist).
7. Multi-report month view: reporting-period uses latest upload's month; weeks from other months (e.g. the May report) aren't reachable from the sidebar.
8. Minor: `created_at` stored without timezone marker (frontend appends 'Z'); coverage can exceed 100% when a job has submissions but 0 open positions (raw-data artifact).

## Conventions (do not regress)

1. Week labels = week-ending Friday ("Ending 26-Jun"), from data.
2. Nothing static/hardcoded user-visible; missing data shows "—" or an explicit empty state — never fabricated numbers.
3. TRIM/whitespace-collapse all names before joining (`clean()` in Lambda).
4. Report History renders only from `/api/reports`.
5. Memory files exist at `~/.claude/projects/D--experiments-gcc-qmetry/memory/` with this same context.
