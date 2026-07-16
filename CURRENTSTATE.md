# CURRENT STATE — SOJPE C2H Phase 1 (as of 2026-07-16, post design-rebuild)

Handoff doc for a new session. Read alongside `../CLAUDE.md` (business rules, metric formulas, 83-step spec) and `README.md` (architecture, API reference, deploy steps).

## One-paragraph summary

The dashboard frontend was **fully rebuilt to the new Metry360 design brief** (`../tech/docs/design/*.png` — Recruitment.png is the 100% target) on top of a new plain-CSS design system. The backend Lambda was extended the same day: renege-count bug fixed, plus recruiters / director HC / MTD joiners / RPR / per-client aggregation / `/api/trends`. Everything renders from the live API; anything the data can't support shows an honest "—" or empty state. Verified end-to-end in Chrome against the design PNGs.

## ⚠️ Deployment status

- **Lambda backend: CURRENT in AWS** (deployed 2026-07-16, includes renege fix + new aggregations + /api/trends).
- **Vercel frontend: STALE** — the rebuilt dashboard, design system, and real upload page are LOCAL/main only. Deploy = `vercel --prod --yes` from repo root, **only after the user gives the go**. Branch rule: everything merges to `main` only; GitHub pushes do NOT auto-deploy Vercel.
- Until deployed, do not ask Akash to upload in prod — the prod upload page silently discards files.

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
