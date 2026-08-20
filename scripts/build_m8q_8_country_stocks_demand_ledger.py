#!/usr/bin/env python3
"""Build the March-July 2026 country stock-and-demand accounting ledger."""

from __future__ import annotations

import calendar
import csv
import io
import re
import tempfile
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/hormuz_m8q_8_country_stocks_demand_ledger.csv"
FEB_URL = "https://www.eia.gov/outlooks/steo/archives/feb26_base.xlsx"
JUL_URL = "https://www.eia.gov/outlooks/steo/archives/jul26_base.xlsx"
SPR_URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCSSTUS1"
COMMERCIAL_CRUDE_URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCESTUS1"
COMMERCIAL_TOTAL_URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WTESTUS1"
IEA_ACTION_URL = "https://www.iea.org/news/iea-member-countries-to-carry-out-largest-ever-oil-stock-release-amid-market-disruptions-from-middle-east-conflict"
IEA_SPLIT_URL = "https://www.iea.org/news/iea-confirms-member-country-contributions-to-collective-action-to-release-oil-stocks-in-response-to-middle-east-disruptions"
IEA_JUL21_URL = "https://www.iea.org/news/iea-executive-director-statement-on-oil-markets"
IEA_JUL_OMR_URL = "https://www.iea.org/reports/oil-market-report-july-2026"
EIA_CHINA_URL = "https://www.eia.gov/international/content/analysis/countries_long/China/"
EIA_CHINA_STOCK_URL = "https://www.eia.gov/todayinenergy/detail.php?id=67504"
NBS_APR_URL = "https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963756.html"
NBS_MAY_URL = "https://www.stats.gov.cn/english/PressRelease/202606/t20260617_1963970.html"
NBS_JUN_URL = "https://www.stats.gov.cn/english/PressRelease/202607/t20260717_1964155.html"
IEA_POLICY_URL = "https://www.iea.org/data-and-statistics/data-tools/2026-energy-crisis-policy-response-tracker"
METI_MAR13_URL = "https://www.meti.go.jp/english/speeches/press_conferences/2026/0313001.html"
METI_MAR24_URL = "https://www.meti.go.jp/english/speeches/press_conferences/2026/0324001.html"
METI_MAY15_URL = "https://www.meti.go.jp/english/press/2026/0515_003.html"
KOREA_URL = "https://english.motir.go.kr/eng/article/EATCLdfa319ada/2661/view"

FIELDS = [
    "row_id", "ledger_group", "accounting_level", "geography", "period_start", "period_end",
    "observation_month", "metric", "value_low", "value_base", "value_high", "unit", "status",
    "data_cutoff", "source_publication_date", "confidence", "source_url", "method", "interpretation",
    "causal_assessment", "double_counting_rule",
]
MONTHS = ["2026-03", "2026-04", "2026-05", "2026-06", "2026-07"]
MONTH_COLS = {"2026-03": "BA", "2026-04": "BB", "2026-05": "BC", "2026-06": "BD", "2026-07": "BE"}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def fmt(value: float | str | None) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.6f}".rstrip("0").rstrip(".")


def make_row(row_id: str, ledger_group: str, accounting_level: str, geography: str,
             period_start: str, period_end: str, observation_month: str, metric: str,
             low: float | str | None, base: float | str | None, high: float | str | None,
             unit: str, status: str, data_cutoff: str, source_publication_date: str,
             confidence: str, source_url: str, method: str, interpretation: str,
             causal_assessment: str, double_counting_rule: str) -> dict[str, str]:
    values = [fmt(low), fmt(base), fmt(high)]
    return dict(zip(FIELDS, [row_id, ledger_group, accounting_level, geography, period_start, period_end,
        observation_month, metric, *values, unit, status, data_cutoff, source_publication_date, confidence,
        source_url, method, interpretation, causal_assessment, double_counting_rule], strict=True))


def xlsx_rows(workbook: bytes, sheet_number: int) -> dict[str, dict[str, float]]:
    """Read numeric rows keyed by STEO mnemonic using only the Python stdlib."""
    with zipfile.ZipFile(io.BytesIO(workbook)) as archive:
        strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = ["".join(t.text or "" for t in si.iterfind(".//m:t", NS))
                   for si in strings_root.findall("m:si", NS)]
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{sheet_number}.xml"))
        output: dict[str, dict[str, float]] = {}
        for xml_row in root.findall(".//m:row", NS):
            cells: dict[str, str] = {}
            for cell in xml_row.findall("m:c", NS):
                match = re.match(r"[A-Z]+", cell.attrib["r"])
                value = cell.find("m:v", NS)
                if not match or value is None:
                    continue
                cells[match.group()] = strings[int(value.text)] if cell.attrib.get("t") == "s" else value.text or ""
            if "A" not in cells:
                continue
            numeric = {}
            for column in {"AZ", *MONTH_COLS.values()}:
                try:
                    numeric[column] = float(cells[column])
                except (KeyError, ValueError):
                    pass
            if numeric:
                output[cells["A"]] = numeric
        return output


class CellParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.cells: list[str] = []
        self.current: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"td", "th"}:
            self.current = ""

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.current += data

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self.current is not None:
            self.cells.append(" ".join(self.current.split()))
            self.current = None


def weekly_month_endpoints(html: str) -> dict[str, tuple[str, float]]:
    parser = CellParser()
    parser.feed(html)
    output: dict[str, tuple[str, float]] = {}
    for month in ["2026-Feb", "2026-Mar", "2026-Apr", "2026-May", "2026-Jun", "2026-Jul"]:
        index = parser.cells.index(month)
        pairs = []
        for offset in range(1, 11, 2):
            if index + offset + 1 >= len(parser.cells):
                continue
            date_text, value_text = parser.cells[index + offset:index + offset + 2]
            if date_text and value_text and re.fullmatch(r"\d{2}/\d{2}", date_text):
                pairs.append((date_text, float(value_text.replace(",", "")) / 1000.0))
        if not pairs:
            raise ValueError(f"No weekly observations found for {month}")
        output[month] = pairs[-1]
    return output


def build_demand_rows(feb: bytes, july: bytes) -> list[dict[str, str]]:
    feb_rows = xlsx_rows(feb, 9)
    jul_rows = xlsx_rows(july, 9)
    specs = {
        "patc_world": ("World", "headline", "Global forecast-vintage consumption gap; do not call the entire revision a causal Hormuz response."),
        "patc_r01": ("North America", "component", "Regional revision; United States, Canada, and Mexico are suballocations."),
        "patc_r02": ("Central and South America", "component", "Regional revision; Brazil is a suballocation."),
        "patc_r03": ("Europe", "component", "Regional revision, not an EU-only series."),
        "patc_r04": ("Eurasia", "component", "Regional revision; Russia is a suballocation."),
        "patc_r05": ("Middle East", "component", "Regional revision; likely strongly affected by local feedstock, refinery, and mobility constraints."),
        "patc_r06": ("Africa", "component", "Regional revision; country detail is not published in this STEO table."),
        "patc_r07": ("Asia and Oceania", "component", "Regional revision; China, India, and Japan are suballocations."),
        "patc_us": ("United States", "suballocation", "Actual/postshock vintage is slightly above the February path cumulatively, so this is a negative demand-reduction contribution."),
        "patc_ca": ("Canada", "suballocation", "Actual/postshock vintage is above the February path cumulatively."),
        "patc_mx": ("Mexico", "suballocation", "Country suballocation of North America."),
        "patc_br": ("Brazil", "suballocation", "Country suballocation of Central and South America."),
        "patc_rs": ("Russia", "suballocation", "Country suballocation of Eurasia."),
        "patc_ch": ("China", "suballocation", "Lower runs and imports support a real adjustment, but macro revisions and structural transport trends also contribute."),
        "patc_in": ("India", "suballocation", "Official alternative sourcing improved; evidence for end-use crude-demand destruction is weaker than the forecast revision alone."),
        "patc_ja": ("Japan", "suballocation", "Reserve use and alternative procurement were prominent; broad end-use demand destruction is not independently established."),
    }
    rows: list[dict[str, str]] = []
    cumulative: dict[str, float] = {}
    for mnemonic, (geography, level, causal) in specs.items():
        if mnemonic not in feb_rows or mnemonic not in jul_rows:
            continue
        total = 0.0
        for month in MONTHS:
            days = calendar.monthrange(2026, int(month[-2:]))[1]
            delta = (feb_rows[mnemonic][MONTH_COLS[month]] - jul_rows[mnemonic][MONTH_COLS[month]]) * days
            total += delta
            rows.append(make_row(
                f"demand-{mnemonic}-{month.replace('-', '')}", "demand_counterfactual", level, geography,
                f"{month}-01", f"{month}-{days:02d}", month, "consumption_below_frozen_february_forecast",
                delta, delta, delta, "million_bbl", "forecast_revision_preliminary" if month != "2026-07" else "forecast_revision_july_forecast",
                "2026-07-31", "2026-07-07", "medium_high", f"{FEB_URL} | {JUL_URL}",
                "(February STEO mb/d minus July STEO mb/d) times calendar days. March-June are preliminary in the July vintage; July is forecast.",
                f"Positive means consumption is lower than the frozen February path. {causal}",
                "The revision is not a controlled causal estimate: it includes the Hormuz shock, ordinary data revisions, weather, macro changes, prices, and structural trends.",
                "World equals the seven region components. Countries are nested within regions and must not be added to their parent region."))
        cumulative[mnemonic] = total
        rows.append(make_row(
            f"demand-{mnemonic}-cumulative", "demand_counterfactual", level, geography, "2026-03-01", "2026-07-31", "",
            "cumulative_consumption_below_frozen_february_forecast", total, total, total, "million_bbl",
            "march_june_preliminary_july_forecast", "2026-07-31", "2026-07-07", "medium_high",
            f"{FEB_URL} | {JUL_URL}", "Sum of the five monthly forecast-vintage gaps.",
            f"Cumulative March-July gap. {causal}",
            "Use as the best reproducible demand counterfactual, not as proof that every barrel was destroyed by the closure.",
            "World equals the seven region components. Countries are nested within regions and must not be added to their parent region."))

    residual_specs = [
        ("North America excluding United States Canada and Mexico", "patc_r01", ["patc_us", "patc_ca", "patc_mx"]),
        ("Central and South America excluding Brazil", "patc_r02", ["patc_br"]),
        ("Eurasia excluding Russia", "patc_r04", ["patc_rs"]),
        ("Asia and Oceania excluding China India and Japan", "patc_r07", ["patc_ch", "patc_in", "patc_ja"]),
    ]
    for name, parent, children in residual_specs:
        value = cumulative[parent] - sum(cumulative[x] for x in children)
        rows.append(make_row(
            "demand-residual-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"), "demand_counterfactual",
            "residual_suballocation", name, "2026-03-01", "2026-07-31", "",
            "cumulative_consumption_below_frozen_february_forecast", value, value, value, "million_bbl",
            "arithmetic_residual_march_june_preliminary_july_forecast", "2026-07-31", "2026-07-07", "medium",
            f"{FEB_URL} | {JUL_URL}", "Parent-region cumulative gap minus named country suballocations.",
            "Preserves exact regional accounting while acknowledging that STEO does not publish all country rows.",
            "Contains both shock response and unrelated revisions.", "Use this residual or its named country children, not both."))
    return rows


def build_us_stock_rows(feb: bytes, weekly_html: dict[str, str]) -> list[dict[str, str]]:
    feb_table = xlsx_rows(feb, 10)
    series = {
        "spr": (weekly_month_endpoints(weekly_html["spr"]), "COSQPUS", "public_strategic_stock_draw", SPR_URL,
                "Government SPR; exchanges may require later barrel returns."),
        "commercial_total": (weekly_month_endpoints(weekly_html["commercial_total"]), "PASXPUS", "total_commercial_petroleum_stock_draw",
                             COMMERCIAL_TOTAL_URL, "All commercial crude and petroleum products excluding SPR."),
        "commercial_crude": (weekly_month_endpoints(weekly_html["commercial_crude"]), "COSXPUS", "commercial_crude_stock_draw",
                             COMMERCIAL_CRUDE_URL, "Crude excluding SPR; memo subset of total commercial petroleum stocks."),
    }
    rows: list[dict[str, str]] = []
    feb_key = "2026-Feb"
    feb_actual = {name: values[0][feb_key][1] for name, values in series.items()}
    forecast_feb = {name: feb_table[mnemonic]["AZ"] for name, (_, mnemonic, _, _, _) in series.items()}
    previous_actual = feb_actual.copy()
    previous_forecast = forecast_feb.copy()
    month_names = {"2026-03": "2026-Mar", "2026-04": "2026-Apr", "2026-05": "2026-May", "2026-06": "2026-Jun", "2026-07": "2026-Jul"}
    for month in MONTHS:
        for name, (actuals, mnemonic, metric, source, description) in series.items():
            date_text, endpoint = actuals[month_names[month]]
            draw = previous_actual[name] - endpoint
            rows.append(make_row(
                f"us-{name}-actual-{month.replace('-', '')}", "stock_actual", "memo_subcomponent" if name == "commercial_crude" else "component",
                "United States", f"{month}-01", f"2026-{date_text}", month, metric, draw, draw, draw, "million_bbl",
                "weekly_observed", "2026-07-24", "2026-07-29", "high", source,
                "Prior selected weekly month-end stock level minus latest weekly level in the observation month; positive is a draw delivered from stocks.",
                f"{description} Endpoint is the last weekly observation, so periods are not exact calendar months.",
                "Observed inventory movement, but commercial movements include seasonal and market effects; SPR withdrawals may be exchanges.",
                "Commercial crude is inside commercial total. Never add those two rows. SPR and commercial total may be added."))
            forecast_endpoint = feb_table[mnemonic][MONTH_COLS[month]]
            forecast_draw = previous_forecast[name] - forecast_endpoint
            rows.append(make_row(
                f"us-{name}-feb-forecast-{month.replace('-', '')}", "stock_counterfactual", "memo_subcomponent" if name == "commercial_crude" else "component",
                "United States", f"{month}-01", f"{month}-{calendar.monthrange(2026, int(month[-2:]))[1]:02d}", month,
                metric, forecast_draw, forecast_draw, forecast_draw, "million_bbl", "frozen_february_forecast", "2026-07-31",
                "2026-02-10", "high", FEB_URL, "Prior February-STEO monthly endpoint minus current endpoint; positive is a planned draw and negative is a planned build.",
                f"Frozen prewar path for {description.lower()}", "Counterfactual, not observed supply.",
                "Use to calculate foregone builds; do not add the forecast stock movement directly to actual stock draws."))
            previous_actual[name] = endpoint
            previous_forecast[name] = forecast_endpoint

    for name, (actuals, mnemonic, metric, source, description) in series.items():
        jul_actual = actuals["2026-Jul"][1]
        jul_forecast = feb_table[mnemonic]["BE"]
        actual_draw = feb_actual[name] - jul_actual
        forecast_draw = forecast_feb[name] - jul_forecast
        change_swing = actual_draw - forecast_draw
        level_gap = jul_forecast - jul_actual
        level = "memo_subcomponent" if name == "commercial_crude" else "component"
        for suffix, result_metric, value, method, interpretation in [
            ("actual-cumulative", metric, actual_draw, "27 February actual endpoint minus 24 July actual endpoint.", f"Actual stocks fell by {actual_draw:.1f} mb."),
            ("forecast-cumulative", f"forecast_{metric}", forecast_draw, "February-STEO February endpoint minus July endpoint.", f"The frozen February path implied a {'draw' if forecast_draw >= 0 else 'build'} of {abs(forecast_draw):.1f} mb."),
            ("change-swing", f"actual_draw_plus_foregone_build_{metric}", change_swing, "Actual draw minus forecast draw; when the forecast expected a build this equals actual draw plus foregone build.", "Preferred additive accounting against observed February baseline."),
            ("july-level-gap", f"actual_stock_below_february_july_path_{metric}", level_gap, "February-STEO July endpoint minus 24 July weekly actual endpoint.", "Includes the February baseline level mismatch as well as the March-July change swing."),
        ]:
            rows.append(make_row(
                f"us-{name}-{suffix}", "stock_actual" if suffix == "actual-cumulative" else "stock_counterfactual_gap", level,
                "United States", "2026-03-01", "2026-07-24", "", result_metric, value, value, value, "million_bbl",
                "weekly_observed" if suffix == "actual-cumulative" else "observed_vs_frozen_forecast", "2026-07-24",
                "2026-07-29" if suffix == "actual-cumulative" else "2026-07-29_and_2026-02-10", "high", f"{source} | {FEB_URL}",
                method, interpretation, "Counterfactual comparison; not all commercial movement is attributable to Hormuz.",
                "Commercial crude is inside commercial total. Use either change-swing or actual draw plus foregone build, never both."))
    return rows


def build_collective_action_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    simple = [
        ("iea-announced", "IEA members", "emergency_oil_announced", 400, "million_bbl", "announcement", "2026-03-11", IEA_ACTION_URL, "Announced envelope, not delivered barrels."),
        ("iea-provisional-total", "IEA members", "provisional_country_contributions", 426, "million_bbl", "provisional_plan", "2026-03-19", IEA_SPLIT_URL, "Country table total; explicitly provisional and not equivalent to observed delivery."),
        ("iea-provisional-public", "IEA members", "provisional_public_stock_contribution", 280, "million_bbl", "provisional_plan", "2026-03-19", IEA_SPLIT_URL, "Component of provisional plan."),
        ("iea-provisional-industry", "IEA members", "provisional_obligated_industry_stock_contribution", 119, "million_bbl", "provisional_plan", "2026-03-19", IEA_SPLIT_URL, "Component of provisional plan; release of an obligation is not necessarily a measured physical draw."),
        ("iea-provisional-production", "IEA members", "provisional_production_increase_contribution", 28, "million_bbl", "provisional_plan", "2026-03-19", IEA_SPLIT_URL, "Production, not stocks; rounded components do not exactly reproduce the stated 426 mb total."),
        ("iea-actual-jul21", "IEA members", "emergency_oil_delivered", 290, "million_bbl", "observed_aggregate", "2026-07-21", IEA_JUL21_URL, "Preferred observed aggregate through 21 July; no public executed country split accompanies it."),
        ("oecd-govt-june", "OECD", "government_stock_release", 44, "million_bbl", "preliminary_observation", "2026-06-30", IEA_JUL_OMR_URL, "June component included within the collective-action delivery and global stocks."),
    ]
    for row_id, geography, metric, value, unit, status, end, source, note in simple:
        rows.append(make_row(row_id, "collective_action", "headline" if "actual" in row_id else "context", geography,
            end, end, "", metric, value, value, value, unit, status, end, end, "high", source,
            "Direct reported amount.", note, "Policy/stock accounting rather than causal demand evidence.",
            "The 290 mb actual aggregate supersedes the 400/426 mb plans for delivered-supply accounting. Components are nested."))

    plans = [
        ("United States", 172.2, "public stocks"),
        ("Japan", 79.8, "54.0 mb public plus 25.8 mb obligated industry stocks"),
        ("South Korea", 22.5, "public/industry split not finalized in the cited public table"),
        ("European Union aggregate", 80.0, "approximately 20% of the original 400 mb action; not an IEA-table country line"),
        ("Other IEA members", 71.5, "arithmetic residual to the 426 mb provisional total"),
    ]
    for geography, value, note in plans:
        slug = re.sub(r"[^a-z0-9]+", "-", geography.lower()).strip("-")
        source = IEA_SPLIT_URL if "European" not in geography else "https://energy.ec.europa.eu/news/commission-calls-eu-countries-coordinate-measures-ensure-oil-security-supply-amid-middle-east-energy-disruption-2026-03-31_en"
        rows.append(make_row(f"iea-plan-{slug}", "collective_action", "country_plan", geography, "2026-03-11", "2026-03-19", "",
            "provisional_emergency_contribution", value, value, value, "million_bbl", "provisional_plan", "2026-03-19", "2026-03-19",
            "high" if geography in {"United States", "Japan", "South Korea"} else "medium", source, "Direct table value or labeled arithmetic residual.",
            note, "Allocation is not proof of delivery.", "Do not add country plans to the delivered 290 mb aggregate."))

    # Imputation cases deliberately sum to the fixed 290 mb actual aggregate in every column.
    delivered = [
        ("United States", 103.994, 103.994, 103.994, "Direct weekly SPR change from 27 February to 17 July, the last weekly endpoint before the 21 July IEA statement."),
        ("Japan", 50.0, 61.8, 72.0, "Project allocation: base assumes all 25.8 mb private relief plus two of three equal 18 mb public tranches; third national release was canceled."),
        ("South Korea", 12.0, 15.0, 19.0, "Project allocation bounded below the 22.5 mb provisional plan; no public weekly execution series located."),
        ("European Union aggregate", 52.0, 60.0, 70.0, "Project allocation bounded below the approximately 80 mb plan; country execution is not public in one reconciled series."),
        ("Other IEA members", 72.006, 49.206, 25.006, "Closing residual so each imputation case equals the reported 290 mb delivered aggregate."),
    ]
    for geography, low, base, high, method in delivered:
        slug = re.sub(r"[^a-z0-9]+", "-", geography.lower()).strip("-")
        rows.append(make_row(f"iea-imputed-delivery-{slug}", "collective_action", "imputed_country_suballocation", geography,
            "2026-03-11", "2026-07-21", "", "imputed_emergency_oil_delivered", low, base, high, "million_bbl",
            "project_imputation_constrained_to_actual_aggregate", "2026-07-21", "2026-07-21", "low" if geography != "United States" else "high",
            f"{IEA_JUL21_URL} | {IEA_SPLIT_URL} | {SPR_URL}", method,
            "This is a transparent country attribution of a known aggregate, not an official executed country table.",
            "Only the U.S. component is directly observed at high frequency.", "Country imputation rows sum to 290 mb in each low/base/high case; use them instead of, never in addition to, the aggregate."))

    rows.append(make_row("iea-jul31-nowcast", "collective_action", "headline", "IEA members", "2026-03-11", "2026-07-31", "",
        "emergency_oil_delivered_july_end_nowcast", 290, 315, 330, "million_bbl", "project_nowcast", "2026-07-31", "2026-07-21", "medium_low",
        IEA_JUL21_URL, "Low holds the 21 July observation; base carries the reported May delivery rate of 2.5 mb/d through the last ten days; high allows modest acceleration below the plan envelope.",
        "Use only when the chart cutoff must be 31 July; otherwise use the 290 mb observed aggregate.", "Not an official July-end execution update.",
        "Alternative cutoff to the 290 mb row, not additive."))
    return rows


def build_country_mechanism_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    china_stock = [
        ("china-march-tanks", "2026-03-01", "2026-03-31", "crude_stock_draw", -40, "preliminary_observation", "IEA reported a 40 mb build; draw convention therefore records -40 mb."),
        ("china-june-tanks", "2026-06-01", "2026-06-30", "crude_stock_draw", 41, "preliminary_observation", "IEA reported China led the June non-OECD draw with a 41 mb decline."),
        ("china-known-months-net", "2026-03-01", "2026-06-30", "known_month_crude_stock_draw", 1, "partial_observation", "Net of March +40 mb build and June -41 mb draw; April, May, and July ownership-resolved changes remain unknown."),
    ]
    for row_id, start, end, metric, value, status, note in china_stock:
        rows.append(make_row(row_id, "country_stock_evidence", "memo", "China", start, end, start[:7] if start[:7] == end[:7] else "",
            metric, value, value, value, "million_bbl", status, end, "2026-07-10", "medium", IEA_JUL_OMR_URL,
            "IEA tank-change estimate; positive draw convention.", note,
            "Ownership is unresolved among government, commercial/operational, bonded, and other stocks.",
            "Included within global/non-OECD observed inventories; the known-month net is derived from the two monthly rows."))
    rows.append(make_row("china-government-spr", "country_stock_evidence", "context", "China", "2026-03-01", "2026-07-31", "",
        "confirmed_government_spr_release", None, None, None, "not_quantified", "not_publicly_confirmed", "2026-07-31", "2026-07-10",
        "medium_high_for_nonconfirmation", f"{EIA_CHINA_STOCK_URL} | {IEA_JUL_OMR_URL}",
        "Public evidence review; EIA estimates roughly 360 mb government-held and about 1 bn barrels commercial crude at end-2025, but China publishes no ownership-resolved release series.",
        "A large government-SPR release is not supported; commercial and operational use is better supported.",
        "Some hidden government use remains possible, so do not encode zero as a measured release.",
        "Use aggregate China tank changes in stock accounting; do not invent a separate government slice."))

    # NBS refinery-throughput shortfall versus reported prior-year comparison, converted with a range of crude barrel/tonne factors.
    for month, actual_mt, decline_pct, source in [
        ("2026-04", 54.65, 5.8, NBS_APR_URL),
        ("2026-05", 53.72, 9.1, NBS_MAY_URL),
        ("2026-06", 51.24, 17.7, NBS_JUN_URL),
    ]:
        prior_mt = actual_mt / (1 - decline_pct / 100)
        shortfall_mt = prior_mt - actual_mt
        low, base, high = (shortfall_mt * factor for factor in (7.1, 7.33, 7.5))
        rows.append(make_row(f"china-refinery-run-shortfall-{month.replace('-', '')}", "demand_mechanism", "memo_subset_proxy", "China",
            f"{month}-01", f"{month}-{calendar.monthrange(2026, int(month[-2:]))[1]:02d}", month,
            "refinery_throughput_below_prior_year_oil_equivalent", low, base, high, "million_bbl", "official_year_on_year_observation_converted",
            f"{month}-{calendar.monthrange(2026, int(month[-2:]))[1]:02d}",
            {"2026-04": "2026-05-19", "2026-05": "2026-06-17", "2026-06": "2026-07-17"}[month], "medium_high",
            source, f"Reported {actual_mt:.2f} Mt and {decline_pct:.1f}% y/y decline imply prior-year throughput {prior_mt:.2f} Mt and shortfall {shortfall_mt:.2f} Mt; convert at 7.1/7.33/7.5 bbl per metric tonne.",
            "Observed lower crude processing, not a direct measure of end-user oil demand.",
            "Likely reflects crude scarcity/run cuts plus macro and product-export decisions.",
            "Nested within China's EIA consumption revision and inventory/import adjustment; never add as a separate demand slice."))

    # Korea has no separate EIA STEO row; retain the prior bounded flow inference as a candidate suballocation of residual Asia.
    cumulative = [0.0, 0.0, 0.0]
    for month in MONTHS:
        days = calendar.monthrange(2026, int(month[-2:]))[1]
        values = [rate * days for rate in (0.05, 0.20, 0.40)]
        cumulative = [a + b for a, b in zip(cumulative, values)]
        rows.append(make_row(f"korea-demand-inference-{month.replace('-', '')}", "demand_country_imputation", "candidate_suballocation", "South Korea",
            f"{month}-01", f"{month}-{days:02d}", month, "inferred_consumption_reduction", *values, "million_bbl",
            "project_inference", "2026-07-31", "2026-07-06", "low", KOREA_URL,
            "Prior F6R bounded inference of 0.05/0.20/0.40 mb/d multiplied by calendar days.",
            "Exposure and reserve capacity are clear, but actual customs, runs, and end-use data are insufficient for a point estimate.",
            "Possible shortage, run-cut, conservation, and macro response.",
            "Candidate suballocation inside Asia/Oceania excluding China, India, and Japan; subtract from that residual if used."))
    rows.append(make_row("korea-demand-inference-cumulative", "demand_country_imputation", "candidate_suballocation", "South Korea",
        "2026-03-01", "2026-07-31", "", "inferred_consumption_reduction", *cumulative, "million_bbl", "project_inference",
        "2026-07-31", "2026-07-06", "low", KOREA_URL, "Sum of monthly bounded inference.",
        "Low/base/high are 7.65/30.6/61.2 mb; not a measured series.", "Possible shortage, run-cut, conservation, and macro response.",
        "Candidate suballocation inside the 146.3 mb residual Asia/Oceania demand gap; not additive to that residual."))

    context = [
        ("china-ev-share", "new_vehicle_sales_ev_share", 48, "percent", "EVs were 48% of new vehicle sales in 2024; structural context predating the shock."),
        ("china-renewables-capacity", "nonhydro_renewable_capacity_added", 356, "GW", "China added 277 GW solar and 79 GW wind in 2024."),
        ("china-renewables-capacity-share", "renewable_share_installed_generation_capacity", 55, "percent", "Renewables were 55% of installed power-generation capacity in 2024."),
        ("china-june-nev-output", "new_energy_vehicle_output_year_on_year_change", 29.4, "percent", "June 2026 new-energy vehicle output rose 29.4% y/y; a current electrification indicator, not measured oil displacement."),
        ("china-june-solar-generation", "solar_generation_year_on_year_change", 14.2, "percent", "June 2026 solar generation rose 14.2% y/y."),
        ("china-june-wind-generation", "wind_generation_year_on_year_change", -5.6, "percent", "June 2026 wind generation fell 5.6% y/y, illustrating why a renewables narrative cannot use solar alone."),
        ("china-june-thermal-generation", "thermal_generation_year_on_year_change", 0.5, "percent", "June 2026 thermal generation rose 0.5% y/y; the power mix did not shift uniformly away from fossil generation."),
    ]
    for row_id, metric, value, unit, note in context:
        rows.append(make_row(row_id, "structural_energy_context", "context", "China", "2024-01-01", "2024-12-31", "", metric,
            value, value, value, unit, "historical_observation" if "june" not in row_id else "current_official_observation",
            "2024-12-31" if "june" not in row_id else "2026-06-30", "2025" if "june" not in row_id else "2026-07-17", "high",
            EIA_CHINA_URL if "june" not in row_id else NBS_JUN_URL,
            "Direct EIA country-analysis statistic.", note,
            "EVs, electric rail, and LNG/electric trucks plausibly lowered transport-oil demand, but the February 2026 forecast already embedded these structural trends.",
            "Do not convert to a March-July oil slice: installed electricity capacity is not oil displacement, China uses little oil-fired power, and incremental post-February adoption is not isolated."))
    rows.append(make_row("global-fuel-switching-not-quantified", "structural_energy_context", "context", "Global", "2026-03-01", "2026-07-31", "",
        "incremental_realized_oil_displacement_from_fuel_switching_renewables_evs", None, None, None, "not_quantified",
        "policy_evidence_without_realized_volume", "2026-07-31", "2026-06-12", "medium", IEA_POLICY_URL,
        "IEA tracker documents measures in nearly 80 countries but does not publish a de-duplicated realized oil-savings volume.",
        "The correct historical accounting leaves this inside measured demand reduction or residual.",
        "Policies may matter, but announcements are not realized barrels and baseline structural trends are already forecast.",
        "No standalone renewable/EV/fuel-switching slice until incremental 2026 oil displacement is measured."))
    return rows


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Hormuz research ledger"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="hormuz-m8q8-"):
        feb = download(FEB_URL)
        july = download(JUL_URL)
        weekly_html = {
            "spr": download(SPR_URL).decode("latin-1"),
            "commercial_crude": download(COMMERCIAL_CRUDE_URL).decode("latin-1"),
            "commercial_total": download(COMMERCIAL_TOTAL_URL).decode("latin-1"),
        }
    rows = build_demand_rows(feb, july)
    rows.extend(build_us_stock_rows(feb, weekly_html))
    rows.extend(build_collective_action_rows())
    rows.extend(build_country_mechanism_rows())
    ids = [row["row_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate row IDs")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
