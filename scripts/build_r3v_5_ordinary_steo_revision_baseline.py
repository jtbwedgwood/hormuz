#!/usr/bin/env python3
"""Build an empirical STEO revision baseline and bounded Hormuz attribution.

The comparison convention exactly matches the project's 2026 counterfactual:
February STEO minus July STEO for the same March-July months, integrated over
calendar days.  A March-June version is also produced for the r3v.1 matched frame.

The non-Hormuz reference years are 2017-2019 and 2023-2025.  2020-2021 are
excluded for the pandemic and 2022 for the invasion-onset shock.  These are not
event-free years; they are an empirical "ordinary plus background news" baseline.
"""

from __future__ import annotations

import calendar
import csv
import io
import math
import re
import statistics
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_r3v_5_ordinary_steo_revision_baseline.csv"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

BASELINE_GROUPS = {
    "primary_non_hormuz": [2017, 2018, 2019, 2023, 2024, 2025],
    "pre_covid_2017_2019": [2017, 2018, 2019],
    "post_covid_2023_2025": [2023, 2024, 2025],
}
ALL_YEARS = [*BASELINE_GROUPS["primary_non_hormuz"], 2026]
HORIZONS = {
    "march_june": {"03": "BA", "04": "BB", "05": "BC", "06": "BD"},
    "march_july": {"03": "BA", "04": "BB", "05": "BC", "06": "BD", "07": "BE"},
}

DEMAND_REGIONS = {
    "patc_r01": "North America",
    "patc_r02": "Central and South America",
    "patc_r03": "Europe",
    "patc_r04": "Eurasia",
    "patc_r05": "Middle East",
    "patc_r06": "Africa",
    "patc_r07": "Asia and Oceania",
}
NONOPEC_SUPPLY_REGIONS = {
    "t3b_papr_r01": "North America non-OPEC supply",
    "t3b_papr_r02": "Central and South America non-OPEC supply",
    "t3b_papr_r03": "Europe non-OPEC supply",
    "t3b_papr_r04": "Eurasia non-OPEC supply",
    "t3b_papr_r05": "Middle East non-OPEC supply",
    "t3b_papr_r06": "Africa non-OPEC supply",
    "t3b_papr_r07": "Asia and Oceania non-OPEC supply",
}

FIELDS = [
    "row_id", "record_type", "baseline_group", "comparison_year", "horizon",
    "metric", "geography", "taxonomy", "revision_million_bbl",
    "baseline_n", "baseline_mean", "baseline_median", "baseline_p10",
    "baseline_p90", "baseline_min", "baseline_max", "baseline_median_absolute",
    "baseline_p90_absolute", "attribution_low", "attribution_high", "unit",
    "february_source_url", "july_source_url", "confidence", "method",
    "interpretation", "causal_warning", "double_counting_rule",
]


def url(slug: str) -> str:
    return f"https://www.eia.gov/outlooks/steo/archives/{slug}_base.xlsx"


def download(source_url: str) -> bytes:
    request = urllib.request.Request(source_url, headers={"User-Agent": "hormuz-research/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def workbook_rows(workbook: bytes, sheet_number: int) -> dict[str, dict[str, str]]:
    """Return XLSX sheet rows keyed by the EIA mnemonic in column A."""
    with zipfile.ZipFile(io.BytesIO(workbook)) as archive:
        strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = [
            "".join(node.text or "" for node in item.iter(f"{{{NS['m']}}}t"))
            for item in strings_root.findall("m:si", NS)
        ]
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet_number}.xml"))
        output: dict[str, dict[str, str]] = {}
        for row_node in root.findall(".//m:row", NS):
            cells: dict[str, str] = {}
            for cell in row_node.findall("m:c", NS):
                value = cell.find("m:v", NS)
                column = re.match(r"[A-Z]+", cell.attrib["r"])
                if value is None or column is None:
                    continue
                raw = value.text or ""
                cells[column.group()] = strings[int(raw)] if cell.attrib.get("t") == "s" else raw
            if cells.get("A"):
                output[cells["A"]] = cells
        return output


def find_table(workbook: bytes, sheet_numbers: list[int], mnemonic: str) -> dict[str, dict[str, str]]:
    for sheet_number in sheet_numbers:
        rows = workbook_rows(workbook, sheet_number)
        if mnemonic in rows:
            return rows
    raise ValueError(f"Could not find {mnemonic} in sheets {sheet_numbers}")


def cumulative_revision(february: dict[str, dict[str, str]], july: dict[str, dict[str, str]],
                        mnemonic: str, year: int, horizon: str) -> float:
    value = 0.0
    for month, column in HORIZONS[horizon].items():
        days = calendar.monthrange(year, int(month))[1]
        value += (float(february[mnemonic][column]) - float(july[mnemonic][column])) * days
    return value


def fmt(value: float | int | str | None) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.6f}".rstrip("0").rstrip(".")


def blank_row(**values: object) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    for key, value in values.items():
        row[key] = fmt(value)  # type: ignore[arg-type]
    return row


def percentile(values: list[float], probability: float) -> float:
    """Linear/Type-7 percentile; descriptive only for the six-year sample."""
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    fraction = position - lower
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def metrics_for_year(year: int) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    suffix = str(year)[2:]
    feb_slug, jul_slug = f"feb{suffix}", f"jul{suffix}"
    feb_book, jul_book = download(url(feb_slug)), download(url(jul_slug))

    feb_supply = find_table(feb_book, [7, 5], "papr_world")
    jul_supply = find_table(jul_book, [7, 5], "papr_world")
    feb_demand = find_table(feb_book, [9, 8], "patc_world")
    jul_demand = find_table(jul_book, [9, 8], "patc_world")
    feb_nonopec = workbook_rows(feb_book, 6)
    jul_nonopec = workbook_rows(jul_book, 6)

    output: dict[str, dict[str, str]] = {}
    for horizon in HORIZONS:
        supply = cumulative_revision(feb_supply, jul_supply, "papr_world", year, horizon)
        demand = cumulative_revision(feb_demand, jul_demand, "patc_world", year, horizon)
        russia_supply = cumulative_revision(feb_nonopec, jul_nonopec, "papr_RS", year, horizon)
        russia_demand = cumulative_revision(feb_demand, jul_demand, "patc_rs", year, horizon)
        values: dict[str, tuple[str, str, float]] = {
            "global_supply": ("World", "petroleum_and_other_liquid_fuels", supply),
            "global_demand": ("World", "petroleum_and_other_liquid_fuels", demand),
            "russia_supply": ("Russia", "petroleum_and_other_liquid_fuels", russia_supply),
            "russia_demand": ("Russia", "petroleum_and_other_liquid_fuels", russia_demand),
            "global_supply_ex_russia": ("World excluding Russia", "petroleum_and_other_liquid_fuels", supply - russia_supply),
            "global_demand_ex_russia": ("World excluding Russia", "petroleum_and_other_liquid_fuels", demand - russia_demand),
        }
        for mnemonic, geography in DEMAND_REGIONS.items():
            values[f"demand_{mnemonic}"] = (
                geography, "petroleum_and_other_liquid_fuels",
                cumulative_revision(feb_demand, jul_demand, mnemonic, year, horizon),
            )
        for mnemonic, geography in NONOPEC_SUPPLY_REGIONS.items():
            values[f"supply_{mnemonic}"] = (
                geography, "non_OPEC_petroleum_and_other_liquid_fuels",
                cumulative_revision(feb_nonopec, jul_nonopec, mnemonic, year, horizon),
            )
        for metric, (geography, taxonomy, value) in values.items():
            output[f"{horizon}|{metric}"] = {
                "geography": geography, "taxonomy": taxonomy, "value": fmt(value)
            }
    return output, {"feb": url(feb_slug), "jul": url(jul_slug)}


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    extracted: dict[int, dict[str, dict[str, str]]] = {}
    sources: dict[int, dict[str, str]] = {}
    for year in ALL_YEARS:
        extracted[year], sources[year] = metrics_for_year(year)
        for key, item in extracted[year].items():
            horizon, metric = key.split("|", 1)
            rows.append(blank_row(
                row_id=f"raw-{year}-{horizon}-{metric}", record_type="raw_vintage_pair",
                baseline_group="primary_non_hormuz" if year != 2026 else "target_2026",
                comparison_year=year, horizon=horizon, metric=metric,
                geography=item["geography"], taxonomy=item["taxonomy"],
                revision_million_bbl=float(item["value"]), unit="million_bbl",
                february_source_url=sources[year]["feb"], july_source_url=sources[year]["jul"],
                confidence="high_arithmetic_medium_measurement",
                method="February STEO minus July STEO for the same monthly values, multiplied by calendar days. Positive is lower supply/demand in July than February had forecast.",
                interpretation=("2026 target revision; not automatically causal." if year == 2026 else
                                "Reference-year revision used to estimate ordinary STEO vintage movement."),
                causal_warning="Vintage revision includes data updates, weather, macro changes, policy, outages and other contemporaneous events.",
                double_counting_rule="Regions and Russia are nested diagnostic rows; do not add them to the world total.",
            ))

    # Distribution summaries for every common metric and both horizons.
    metric_keys = sorted(extracted[2026])
    summary_lookup: dict[tuple[str, str], dict[str, float]] = {}
    for group, years in BASELINE_GROUPS.items():
        for key in metric_keys:
            horizon, metric = key.split("|", 1)
            sample = [float(extracted[year][key]["value"]) for year in years]
            stats = {
                "n": float(len(sample)), "mean": statistics.mean(sample),
                "median": statistics.median(sample), "p10": percentile(sample, 0.10),
                "p90": percentile(sample, 0.90), "min": min(sample), "max": max(sample),
                "median_abs": statistics.median(abs(value) for value in sample),
                "p90_abs": percentile([abs(value) for value in sample], 0.90),
            }
            if group == "primary_non_hormuz":
                summary_lookup[(horizon, metric)] = stats
            item = extracted[2026][key]
            rows.append(blank_row(
                row_id=f"summary-{group}-{horizon}-{metric}", record_type="baseline_distribution",
                baseline_group=group, horizon=horizon, metric=metric,
                geography=item["geography"], taxonomy=item["taxonomy"],
                baseline_n=int(stats["n"]), baseline_mean=stats["mean"],
                baseline_median=stats["median"], baseline_p10=stats["p10"],
                baseline_p90=stats["p90"], baseline_min=stats["min"],
                baseline_max=stats["max"], baseline_median_absolute=stats["median_abs"],
                baseline_p90_absolute=stats["p90_abs"], unit="million_bbl",
                february_source_url=" | ".join(sources[year]["feb"] for year in years),
                july_source_url=" | ".join(sources[year]["jul"] for year in years),
                confidence="medium_for_scale_low_for_probability",
                method="Descriptive distribution across the listed reference years; p10/p90 use linear Type-7 interpolation.",
                interpretation="Empirical ordinary-plus-background-news STEO revision baseline, not a confidence interval.",
                causal_warning="Only three or six observations; years contain OPEC decisions, sanctions, weather and other events even though they lack a new Hormuz-scale shock.",
                double_counting_rule="Use one baseline group at a time. Pre- and post-COVID subsets are sensitivities inside the six-year primary sample.",
            ))

    # Causal attribution after explicitly removing Russia, then applying the
    # empirical ex-Russia revision distribution.  Central = p10/p90; the full
    # observed envelope is retained as a conservative sensitivity.
    for horizon in HORIZONS:
        for kind in ("supply", "demand"):
            world_key = f"{horizon}|global_{kind}"
            russia_key = f"{horizon}|russia_{kind}"
            ex_key = f"{horizon}|global_{kind}_ex_russia"
            world = float(extracted[2026][world_key]["value"])
            russia = float(extracted[2026][russia_key]["value"])
            ex_russia = float(extracted[2026][ex_key]["value"])
            stats = summary_lookup[(horizon, f"global_{kind}_ex_russia")]
            central_low = ex_russia - stats["p90"]
            central_high = ex_russia - stats["p10"]
            conservative_low = ex_russia - stats["max"]
            conservative_high = ex_russia - stats["min"]
            common = dict(
                baseline_group="primary_non_hormuz", horizon=horizon,
                geography="World excluding Russia", taxonomy="petroleum_and_other_liquid_fuels",
                unit="million_bbl", february_source_url=sources[2026]["feb"],
                july_source_url=sources[2026]["jul"],
                confidence="medium_for_band_low_for_causal_precision",
                causal_warning="This is a bounded attribution, not an identified treatment effect. Ordinary revision may correlate with the Hormuz shock and the six reference years are a small sample.",
                double_counting_rule="Russia is removed before applying the ex-Russia baseline; do not subtract it again or add regional rows.",
            )
            rows.append(blank_row(
                row_id=f"attribution-{horizon}-{kind}-headline", record_type="target_decomposition",
                metric=f"2026_global_{kind}_revision", revision_million_bbl=world,
                method="Observed February-to-July 2026 world vintage revision.",
                interpretation="Revision-path headline; not a causal Hormuz estimate.", **common,
            ))
            rows.append(blank_row(
                row_id=f"attribution-{horizon}-{kind}-russia", record_type="named_non_hormuz_component",
                metric=f"russia_{kind}_revision_removed", geography="Russia",
                revision_million_bbl=russia,
                method="Russia row from the same EIA vintage pair. 2026 attacks on Russian energy infrastructure are separately documented by IEA and Reuters.",
                interpretation="Explicit non-Hormuz component removed before baseline adjustment; positive is a contribution to the world downward revision.", **{k: v for k, v in common.items() if k != "geography"},
            ))
            rows.append(blank_row(
                row_id=f"attribution-{horizon}-{kind}-central-band", record_type="causal_attribution_band",
                metric=f"hormuz_plausible_{kind}_effect_central_band",
                revision_million_bbl=ex_russia, baseline_p10=stats["p10"],
                baseline_p90=stats["p90"], attribution_low=central_low,
                attribution_high=central_high,
                method="2026 world revision less Russia, then subtract the p10-to-p90 signed ordinary ex-Russia revision distribution; endpoints reverse because a larger ordinary downward revision leaves less for Hormuz.",
                interpretation="Preferred causal-plausible band. It can exceed the net observed revision when ordinary revision would otherwise have raised supply/demand.", **common,
            ))
            rows.append(blank_row(
                row_id=f"attribution-{horizon}-{kind}-conservative-band", record_type="causal_attribution_band_sensitivity",
                metric=f"hormuz_plausible_{kind}_effect_full_observed_envelope",
                revision_million_bbl=ex_russia, baseline_min=stats["min"],
                baseline_max=stats["max"], attribution_low=conservative_low,
                attribution_high=conservative_high,
                method="2026 world revision less Russia, then subtract the full observed min/max ex-Russia baseline envelope.",
                interpretation="Conservative sensitivity; not preferred because one reference-year extreme sets each endpoint.", **common,
            ))

    # Audit allowance used to re-tier r3v.1: named Russia demand plus the p90
    # absolute ex-Russia ordinary revision. It is an uncertainty reserve, not a
    # claim that exactly this many barrels were unrelated to Hormuz.
    demand_key = "march_june|global_demand_ex_russia"
    russia_demand = float(extracted[2026]["march_june|russia_demand"]["value"])
    allowance = max(0.0, russia_demand) + summary_lookup[("march_june", "global_demand_ex_russia")]["p90_abs"]
    rows.append(blank_row(
        row_id="r3v1-march-june-demand-t4-revision-allowance",
        record_type="evidence_tier_propagation", baseline_group="primary_non_hormuz",
        horizon="march_june", metric="demand_non_hormuz_or_ordinary_revision_uncertainty_allowance",
        geography="World", taxonomy="petroleum_and_other_liquid_fuels",
        revision_million_bbl=allowance,
        baseline_p90_absolute=summary_lookup[("march_june", "global_demand_ex_russia")]["p90_abs"],
        unit="million_bbl", february_source_url=sources[2026]["feb"],
        july_source_url=sources[2026]["jul"], confidence="low_medium",
        method="Positive March-June Russia demand revision plus the empirical p90 absolute March-June world-ex-Russia revision. Used as a T4 uncertainty allowance in r3v.1.",
        interpretation="A conservative evidence-tier reserve, not a point estimate of barrels proven unrelated to Hormuz.",
        causal_warning="Absolute revision magnitudes lose sign and are used only to size uncertainty, not causal subtraction.",
        double_counting_rule="Replaces the earlier demand structural/ordinary-revision T4 slice in r3v.1; do not add both.",
    ))

    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate row IDs")
    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
