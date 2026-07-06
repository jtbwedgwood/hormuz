# Foundation Research Standards

These standards govern source quality, citation, uncertainty, and publication figures for the Hormuz project.

## Source-Quality Rubric

Use the highest available tier for every claim. Lower-tier sources can motivate leads, but do not let them carry a central quantitative claim without corroboration.

| Tier | Use for | Examples | Rules |
|---|---|---|---|
| A1 - primary official data | Core quantitative claims, baselines, country totals, historical comparisons | EIA, IEA, JODI, UN Comtrade, IMF, World Bank, national customs/statistical agencies, port authorities, official emergency/stockpile agencies | Preferred source for final numbers. Record version, release date, access date, unit, geography, and transformation. |
| A2 - primary operational data | Ship movements, port calls, observed rerouting, geofenced transit counts | Raw AIS feeds, port authority notices, marine safety bulletins, satellite imagery with reproducible method | Accept only with documented collection window, geofence or imagery footprint, vessel inclusion rules, and known blind spots. |
| B - transparent institutional analysis | Cross-checks, model assumptions, contextual estimates | IEA/OPEC/EIA commentary, peer-reviewed papers, central-bank or government research, reputable think-tank work with methods | Use when the method is visible and inputs are traceable. Cite the underlying data when possible. |
| C - commercial/analyst estimates | Fast-moving flows, freight, insurance, private AIS-derived indicators | Kpler, Vortexa, Lloyd's List Intelligence, S&P Global, Argus, Platts, Rystad, broker notes | Usable if date, provider, metric definition, and quoted value are explicit. Treat as estimate unless independently validated. |
| D - reputable news | Event chronology, quotes, sanctions/actions, market reaction | Reuters, AP, FT, WSJ, Bloomberg, trade press | Use for reported events and attributed claims. Do not use as sole source for derived flow volumes unless no better source exists. |
| E - unverified/social/advocacy | Leads only | Social media, anonymous screenshots, political statements, unsourced aggregators | Do not use in final claims unless corroborated and clearly labeled as allegation or official statement. |

Recency rules:

- For live disruption claims, prefer sources published or updated within 72 hours; if older, label the observation window explicitly.
- For monthly/annual official data, use the latest release available at analysis time and record the release date.
- For structural facts such as route capacity or historical chokepoint shares, refresh if the source is more than two years old or if infrastructure, sanctions, or conflict conditions changed materially.
- Never mix baseline and disruption-period data without stating both date ranges.

Required citation fields for every cited dataset, article, or report:

- `claim_id` or figure/table identifier.
- Source organization and author if available.
- Title or dataset name.
- Publication/release date and, for live pages, access date.
- URL or DOI; archive URL when available.
- Dataset version, table name, query parameters, geography, time period, units, and transformation notes.
- Confidence label: `high`, `medium`, `low`, or `speculative`.
- Paywall/access status: `public`, `free_registration`, `paywalled`, `licensed`, or `private_note`.

Confidence labels:

- `high`: primary data or multiple independent sources agree; definitions are clear; uncertainty is bounded.
- `medium`: credible source and plausible method, but incomplete definitions, lagged data, or only one independent source.
- `low`: credible but indirect proxy, weak comparability, or material missing data.
- `speculative`: scenario, model sensitivity, allegation, or analyst judgment not yet validated.

Paywall and archive handling:

- Public sources should be archived with Internet Archive Save Page Now when they support a final claim.
- For paywalled sources, cite the public landing page plus publication, date, author, and exact metric; keep short paraphrased notes in the issue file, not copied article text.
- For licensed data, cite the provider and dataset/module name, but do not commit restricted raw data or screenshots unless the license permits it.
- If an archive capture fails because of dynamic content, record the failure and keep the live URL plus access date.

Claim rules:

- Every chart subtitle, table value, or confident prose claim must trace to a source row or issue note.
- Central quantitative claims need either Tier A support or two independent lower-tier sources.
- Distinguish observed data from modeled estimates and scenarios in both prose and figures.
- Preserve contradictory estimates when they matter; report a range or explain why one source is preferred.

## Chart And Map Standards

Publication figures should be reproducible, source-auditable, and readable as standalone assets.

Figure metadata required:

- Figure ID, short title, author/script path, data source files, upstream URLs, generation date, and output path.
- Exact time period, geography, units, baseline period, deflator/currency basis if relevant, and whether values are observed, estimated, modeled, or interpolated.
- Source footnote in the graphic or caption: `Source: ...; calculations by author.` Add `Accessed YYYY-MM-DD` for live or changing pages.

Uncertainty display:

- Use bands for model intervals, ranges, and source disagreement; use points/lines only for central estimates.
- Label intervals by meaning, not just style: `source range`, `95% CI`, `scenario range`, `low/high estimate`.
- For confidence categories, use direct labels or symbols in addition to color.
- Do not smooth volatile daily series unless the raw series remains available in the figure, appendix, or data file. If using rolling averages, state the window.

Missing and partial data:

- Leave gaps for missing observations unless interpolation is analytically necessary.
- Use dashed lines for interpolated or provisional segments and label them.
- Do not convert missing values to zero unless the data source explicitly defines absence as zero.
- Footnote known blind spots: AIS dark activity, sanctions/shadow-fleet behavior, country reporting lags, re-exports, and cargo classification ambiguity.

Chart design:

- Start quantitative axes at zero for bars/areas; line charts may use non-zero axes only when clearly labeled.
- Use direct labels where feasible; legends are acceptable for dense multi-series charts.
- Avoid color-only encoding; combine color with line style, marker, label, or pattern for key distinctions.
- Use consistent units: `mb/d`, `mt`, `bcm`, `$2026`, `% of baseline`, or `% of global supply`; avoid mixed units in one axis.
- Put the takeaway in the title only when the underlying claim is high or medium confidence.

Map standards:

- Use Natural Earth public-domain basemaps for global/regional context unless a more precise official maritime boundary dataset is required.
- For the Gulf/Hormuz inset, prefer a local projection that preserves shape and distance well enough for the displayed scale; for world flow maps, use a compromise projection and avoid Mercator for area comparisons.
- Label disputed boundaries conservatively and avoid implying sovereignty when the map only needs trade routes or ports.
- Show routes as schematic flows unless vessel-level tracks are actually observed. Do not imply exact paths from aggregate cargo statistics.
- Include scale, north arrow only when useful, projection/basemap note, and geofence definition when counting transits.

Export formats:

- Archive editable source: script/notebook plus data inputs and environment notes.
- Export publication raster at 2x target blog width as PNG; use SVG/PDF for vector charts and maps when labels render reliably.
- Keep machine-readable figure data as CSV/Parquet next to generated figures.
- File names should include figure ID, slug, and date or version, for example `fig-02-hormuz-daily-transits-2026-07-06.png`.

Visual audit before publication:

- Verify every plotted number against the source data after transformations.
- Check mobile width legibility, colorblind accessibility, and grayscale interpretability.
- Confirm source notes and uncertainty labels survive export.
- Inspect maps for misleading route precision, clipped labels, and projection artifacts.

## Public Reference URLs

- EIA, World Oil Transit Chokepoints: https://www.eia.gov/international/analysis/special-topics/world_oil_transit_Chokepoints
- EIA, Strait of Hormuz remains critical oil chokepoint: https://www.eia.gov/todayinenergy/detail.php?id=65504
- DataCite Metadata Schema: https://schema.datacite.org/
- NOAA Data Citation Procedural Directive: https://repository.library.noaa.gov/view/noaa/65786
- Internet Archive Save Page Now help: https://help.archive.org/help/using-the-wayback-machine/
- Reuters Trust Principles: https://www.thomsonreuters.com/en/about-us/trust-principles
- Reuters Journalistic Standards: https://reutersagency.com/about/standards-values/
- IPCC uncertainty guidance note: https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf
- Datawrapper accessibility guidance: https://www.datawrapper.de/academy/how-we-make-sure-our-charts-maps-and-tables-are-accessible
- Datawrapper colorblind visualization guidance: https://www.datawrapper.de/blog/colorblindness-part2
- Natural Earth: https://www.naturalearthdata.com/
- Natural Earth terms of use: https://www.naturalearthdata.com/about/terms-of-use/
