---
id: "hormuz-f6r.7"
title: "Reconcile replacement supply origins by importer"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "importers"
  - "tradeflows"
  - "substitution"
blocked_by: []
blocks:
  - "hormuz-ccx.5"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T00:00:00Z"
updated_at: "2026-07-07T00:00:00Z"
---

# Reconcile replacement supply origins by importer

## Description

Tighten the country-by-country replacement-supply story for China, India, Japan, and South Korea. Distinguish named replacement origins, cargo rerouting, stock draw, demand destruction, and unresolved/other.

## Acceptance Criteria

- Country rows identify replacement origins where public evidence supports them.
- China section separates Russia, sanctioned/relabeled Iranian barrels, Saudi/UAE bypass barrels, commercial stocks, lower refinery runs, and unresolved/other.
- India section separates crude replacement from gas/LPG rationing and named LPG suppliers.
- Japan and South Korea get one-sentence replacement-origin/inventory-draw summaries suitable for the blog.
- Any cargo-level claim is flagged if it requires Kpler/Vortexa/licensed AIS rather than public data.

## Work Notes

- 2026-07-06: Filed from follow-up synthesis. Existing F6R tables provide adjustment buckets but not a fully reconciled origin-by-origin replacement matrix.
- 2026-07-07: Claimed for a narrow public-evidence reconciliation pass. Target outputs: `data/derived/hormuz_f6r_7_replacement_supply_origins.csv` and, if useful, `docs/hormuz-importer-replacement-origins.md`.
- 2026-07-07: Completed `data/derived/hormuz_f6r_7_replacement_supply_origins.csv` with 18 rows covering China, India, Japan, South Korea, and a cross-cutting licensed-data caveat row. Added concise user-facing addendum at `docs/hormuz-importer-replacement-origins.md`. Added a minimal manifest row for the derived matrix.
- 2026-07-07: Acceptance notes:
  - China rows separately identify Russia, sanctioned/relabeled Iranian barrels, Saudi/UAE bypass barrels, commercial/operational stocks, lower refinery runs, LNG demand response, and unresolved/other. Confidence is highest for observed lower refinery runs and weakest for exact named-origin volume splits.
  - India rows separate crude-route diversification from gas/LNG rationing and LPG. Public sources name LPG suppliers as the United States, Norway, Canada, Algeria, Russia, plus available Gulf sources; public crisis releases do not name crude replacement countries.
  - Japan gets a blog-ready sentence and rows for Yanbu, Fujairah, U.S. procurement, possible Central Asia/South America supply, and stock releases. METI support is strong for route categories and aggregate replacement coverage, not cargo-by-cargo supplier volumes.
  - South Korea gets a blog-ready sentence and rows for unresolved crude replacement plus Qatar LNG/condensate priority assurance. Replacement-volume confidence remains medium-low because public sources do not show actual cargo replacement or drawdown series.
  - Any exact claim like "China replaced X mb/d with Russia" or "Korea replaced Y cargoes from supplier Z" is flagged as requiring Kpler/Vortexa/licensed AIS or customs reconciliation.
- 2026-07-07: Key sources accessed and used:
  - EIA/Vortexa oil route/destination and bypass capacity: `https://www.eia.gov/todayinenergy/detail.php?id=65504`.
  - EIA/Vortexa LNG route/destination: `https://www.eia.gov/todayinenergy/detail.php?id=65584`.
  - CGEP China energy-security Q&A: `https://www.energypolicy.columbia.edu/implications-of-the-conflict-in-the-middle-east-for-chinas-energy-security/`.
  - EIA China country brief PDF: `https://www.eia.gov/international/content/analysis/countries_long/China/pdf/China-2025.pdf`.
  - EIA strategic oil inventory note: `https://www.eia.gov/todayinenergy/detail.php?id=67504`.
  - China NBS April and May 2026 energy production: `https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html`, `https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html`.
  - India PIB March 11 and March 12 statements: `https://www.pib.gov.in/PressReleasePage.aspx?PRID=2238525&lang=1&reg=3`, `https://www.pib.gov.in/PressReleasePage.aspx?PRID=2239021&lang=2&reg=3`.
  - Japan METI March 3, March 13, March 24, and May 15 statements: `https://www.meti.go.jp/english/speeches/press_conferences/2026/0303001.html`, `https://www.meti.go.jp/english/speeches/press_conferences/2026/0313001.html`, `https://www.meti.go.jp/english/speeches/press_conferences/2026/0324001.html`, `https://www.meti.go.jp/english/press/2026/0515_003.html`.
  - Korea MOTIR Qatar LNG/condensate statement: `https://english.motir.go.kr/eng/article/EATCLdfa319ada/2661/view`.
- 2026-07-07: Validation: ran `.venv/bin/python` CSV check over `data/derived/hormuz_f6r_7_replacement_supply_origins.csv` and `data/manifest.csv`; result was 18 matrix rows, 13 columns, no malformed CSV rows, no missing required IDs/sources/confidence fields, required China buckets present, India LPG supplier row present, and 15 rows flagged as needing cargo-level data for exact volume claims.
