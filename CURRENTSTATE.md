# CURRENT STATE — SOJPE C2H Phase 1 (as of 2026-07-17, post targets-master)

## 2026-07-17: Targets master + Monthly Rollup (ALL LIVE, commit 722599b)

- **Targets master** (from `../Targets.xlsx`): S3 `config/targets.json`, GET/PUT `/api/config/targets` (history-archived like the other masters), 16 per-AM rows with FY Apr 2026–Mar 2027 monthly Entry/Exit targets + C FWD + HC End; editable "Targets" grid in Master Tables. Floor totals validate (Jul 193 / Jun 154 / May 152 entries).
- **Target-name aliasing is code-side only** (org master untouched): "Sathish - IT" + "Sathish - Non IT" SUM to Sathish Kumar B (Jul 21/21); "Praveen" → Praveen Kumar M. Director rollup follows the canonical org chart (Praveen/Vivek/Rumman/Sachin/Sankeerth targets under Sanjib Saha = Jul 108), NOT the targets file's director column (display-only).
- **New metrics on every AM/director/grand row** (when a target exists): `monthly_target`, `monthly_exit_target`, `weekly_target` = monthly ÷ 21 × week's working days (uses config `working_days_per_month`), `target_achievement_pct` = MTD joiners ÷ monthly target, `rpr` = MTD joiners ÷ recruiter count (product-owner spec; null when recruiter count unknown — June has no Avg Subs file). Top-level `targets_available`.
- **`GET /api/monthly?month=YYYY-MM`** (default latest report's month): sums weekly actuals across the month's reports, point-in-time MTD/recruiters from the latest report, contributing-week list; months with no uploads still show targets with null actuals. Frontend "Monthly Rollup" view (month selector, KPI cards, director→AM table, week chips).
- **Weekly tables** gained Target / Ach % / RPR columns + ⓘ formula popovers, gated on `targets_available` (layout unchanged for pre-targets payloads). Intelligence-report efficiency alert now uses recruiter-based RPR (silent when null).
- **Recruiter-level coverage FLAGGED IMPOSSIBLE**: Ceipal Coverage export has no assign-to column. Parser is ready — an "Assigned To"/"Assigned Recruiter" column will auto-emit per-AM `recruiter_coverage`; until then recruiter coverage cells show "—" + ⓘ.
- Divya Lakshmi confirmed already correct in org master (DivyaLakshmi → Manisha Jishtu + aliases); org chart NOT modified.

# Previous state (2026-07-16, post design-rebuild)

Handoff doc for a new session. Read alongside `../CLAUDE.md` (business rules, metric formulas, 83-step spec) and `README.md` (architecture, API reference, deploy steps).

## One-paragraph summary

The dashboard frontend was **fully rebuilt to the new Metry360 design brief** (`../tech/docs/design/*.png` — Recruitment.png is the 100% target) on top of a new plain-CSS design system. The backend Lambda was extended the same day: renege-count bug fixed, plus recruiters / director HC / MTD joiners / RPR / per-client aggregation / `/api/trends`. Everything renders from the live API; anything the data can't support shows an honest "—" or empty state. Verified end-to-end in Chrome against the design PNGs.

## Deployment status — ALL LIVE as of 2026-07-16 ~17:15 IST

- **Lambda backend: CURRENT in AWS** (renege fix, aggregations, trends, configs, categories).
- **Vercel frontend: DEPLOYED and verified** at https://metry360.arkos.studio (design rebuild, recruiter hierarchy, calendar weeks, June W4, Select Category, Master Tables). Prod upload page is now the real uploader — Akash can upload in prod.
- ⚠️ Vercel BLOCKS deployments whose commit author email isn't linked to a GitHub account. Fixed via repo-local `git config user.email "103489765+andytrigent@users.noreply.github.com"` (andytrigent's noreply address). Do NOT commit in this repo with anand.padia@gmail.com — deployments will silently BLOCK again (state BLOCKED, no build logs).

## New frontend architecture (2026-07-16 rebuild)

- `public/assets/metry-ds.css` — design system: tokens (`:root`) + `m-` prefixed components (sidebar, chips, KPI cards, RAG rail/popover, tables, alert cards, charts, empty states).
- `public/assets/metry-charts.js` — `window.MetryCharts.{donut, sparkline, lineChart}`, inline SVG, zero deps, honest 0/1/2-point handling.
- `public/design-system.html` — living component reference (serve at /design-system.html). Use it for any new UI.
- `public/dashboard.html` — single-page app, all views: Recruitment (pixel-faithful to Recruitment.png), Management View (expandable director→AM rows), Director Drilldown, AM Productivity, Renege Watch, Coverage Gap, Amazon Ops, ITS (client-scoped), Report History (restyled), plus quarter cycle + month/W1–W4 week chips driven by real report data. Export PDF = window.print() with print stylesheet; CSV export kept.
- Design decisions: "RENGE" typo in the PNG corrected to "RENEGE"; W1–W4 chips per design but subtitle/trend labels use real dates; a small `DIRECTOR_ALIASES` map merges verified name variants (Sivaranjani/Sivaranjani Pandian; Jyosthna/Jyothsna) — real fix is the canonical name Config (CLAUDE.md open item #4).

## Later same-day additions (all deployed + verified)

- **Canonical org chart**: Lambda embeds CANONICAL_ORG from `../Hirearchy Tracker.xlsx` — org chart wins over per-file BU Head; verified aliases only (Jyosthna/Jyothsna, Sivaranjani/Sivaranjani Pandian, Roshan D, etc.). Unassigned now = truly blank AMs only (July 939 pos). ~8 AMs in live data are missing from the org tracker (stale org, grouped by real BU Head). Open question for business: Vivek Singh Sengar / Praveen Kumar M are both AMs under Sanjib AND their own Staffing director blocks (shown both ways). "Sarvasiddi Venkata Divya Lakshmi" probably = DivyaLakshmi — unconfirmed, kept separate.
- **Recruiter-level hierarchy**: each AM carries `recruiter_details:[{name,submissions,target,leave_count,comments}]` + top-level `unattached_recruiters` (July 38/102, May 25/90 — managers not in org config; adding names to CANONICAL_ORG/AM_ALIASES auto-attaches them). Recruitment view renders recruiter → AM → director with real per-recruiter ACHIEVE % (submissions/target — the Avg Subs file has per-recruiter targets).
- **Calendar-anchored weeks** (user requirement): W1 starts the 1st of month, weeks end Friday, W5 exists. July: W1=01–03 (3 working days), report=W2. May: W1=May 1 alone, report=**W5** (25–29). API emits corrected `week` + `weeks:[{n,start,end,label,working_days,has_report,report_id}]`; chips render from it, no client-side week math.
- **No design-placeholder data**: sidebar client views + Select Client dropdown driven by real `clients[]` (top-3 by positions). Frontend alias stopgap removed (names canonical server-side).
- **Targets discovery**: `../C2H_SOJPE_May_Week_2_17 May 2026_f.xlsx` has a real `Targets` sheet (per-AM monthly Entry/Exit, FY Apr–Mar) — could unlock Monthly Target/MTD/Achieve KPIs; NOT wired in (confirm currency with Rhoni first). `SOJPE_Config.xlsx` is an empty stub. More backend changes expected from product owner.

## Evening additions 2026-07-16 (all deployed + verified)

- **June W4 uploaded via the real browser flow** → REPORT-UVX56ZGH3JL (22–26 Jun, W4). June's real file mix ≠ canonical 7 (no Submissions/Avg Subs, no standalone Exits; YTE/YTJ pivot extras) → upload flow now requires only the 5 core files (coverage/selects/renege/joiners/staffing) with optional files + explicit metric-impact warnings; Lambda classifies YTE/YTJ (stored, never used as numbers) and derives weekly exits from the Staffing workbook's 'Exit Report' sheet when no exits file (new `exits_source` field: weekly_exits_file | staffing_exit_report | null). June headline: 4,487 positions, 48.2% cov, 4.68 avg sub, 71 selections, 11 reneges, 26 joiners, 25 exits; recruiters/Achieve "—" (no submissions file). All 3 reports reprocessed via UI buttons. NOTE: Reprocess uses a native alert() — replace with in-page toast (blocks automation).
- **Editable master tables (Rhoni)**: S3 config store (config/customer_master.json 708 rows from customer_List_categorized_16_07_2026_v6.xlsx; config/org_chart.json) with GET/PUT /api/config/customer-master + /api/config/org-chart, append-only history under config/history/ before every overwrite; Lambda loads configs per request → edits apply without redeploy. **NO AUTH on config PUTs (Phase 1 risk — needs Phase 2 JWT or at least API key).**
- **Categories**: Coverage's Client column = master's Sub Unit. /api/dashboard-data now emits categories[] (IT Services, Product/Captive, BPO, Non Tech Non BPO, EDC, GCC + honest "Uncategorized") and category_match {matched,total}. Match ~80%/week; Uncategorized (~20%, mostly FT_-prefixed + new sub-units) is fixed by Rhoni adding master rows. Frontend: "Select Client"→"Select Category" dropdown, top-3 category sidebar shortcuts, category-scoped view, and a "Master Tables" workspace view (editable grids, filter, add/delete row, honest save states; verified full PUT round-trip).
- Local dev server (scratchpad local_server.py): now serves /rawfiles/<subpath> for the whole raw-reports tree and proxies PUT.

## Backend API (Lambda `sojpe-data-pipeline`, deployed)

- Renege bug FIXED: column matcher `cg()` now matches exact → whole-word → substring ('Count' no longer binds to 'Account Manager'). July reneges = 5 (was 0).
- `/api/dashboard-data` (+`?report_id=`): totals.recruiters; per-director recruiters|null, hc{opening,closing,joiners_week,exits_week}|null, mtd_joiners, rpr|null; per-AM recruiters|null, mtd_joiners; top-level `clients:[{name,positions,submissions,jobs_with_subs,coverage_pct,avg_sub}]` (July: 158 clients). Missing data (targets/offers/billing) = absent keys, never fabricated.
- `/api/trends`: `{weeks:[{report_id, week_ending, month, totals}]}` chronological.

## Data currently in the system (real)

| Report | Data week | Notes |
|--------|-----------|-------|
| REPORT-718RPGZXPF3 | Ending 10-Jul-2026 (06–10 Jul) | July W2; default view |
| REPORT-3DDF59BC5F60 | Ending 29-May-2026 (25–29 May) | Repo's original raw files |

**NO JUNE DATA EXISTS** (S3 + local verified). Any June upload hit the prod fake uploader and vanished — Akash must re-upload June's 7 files (after Vercel deploy, or locally). June chip shows an honest empty state.

## Honest gaps / flagged as impossible with current data

1. **Monthly targets** — not in any of the 7 files → Monthly Target KPI "—/—", Select %, Target Selects, Achieve %, MTD denominators all blocked. Needs Config (per-AM monthly target + working days). CLAUDE.md open items #1/#4/#5.
2. **Offers** — no Ceipal report → official Renege % (Reneges/Offers) impossible; UI shows renege counts.
3. **Avg Billing / Revenue** — NO billing column in the real Staffing file (CLAUDE.md is wrong about this) → revenue metrics impossible from current exports.
4. **Trends** — only 2 uploaded weeks (May, July) → velocity charts plot 2 honest points; per-AM sparklines are 2-point/1-dot.
5. **Org Health donut** — partial composite (Coverage + Avg Sub only), captioned as such; other 3 factors need targets/offers.
6. Name mismatches across the 7 files depress recruiter-match (~7/20 AMs) → canonical AM name master (Rhoni) still the durable fix.
7. Client dropdown is populated but doesn't yet re-scope the main tables (Amazon Ops/ITS sidebar views are the client-scoping path).
8. Approval workflow buttons still visual-only; `created_at` timezone quirk remains.

## Conventions (do not regress)

1. Week labels from data; nothing user-visible hardcoded; missing data = "—" or explicit empty state — never fabricated numbers.
2. TRIM/whitespace-collapse names before joining; alias map is a stopgap, not the fix.
3. Report History renders only from `/api/reports`.
4. New UI must be built from `metry-ds.css` components + `MetryCharts` (see design-system.html).
5. Local dev: `python <scratchpad>/local_server.py` → http://127.0.0.1:8123 (serves `public/` + proxies `/api/*` to real AWS). AWS CLI: user runs `! aws login` when sessions expire.
6. Memory files exist at `~/.claude/projects/D--experiments-gcc-qmetry/memory/` with this same context.
