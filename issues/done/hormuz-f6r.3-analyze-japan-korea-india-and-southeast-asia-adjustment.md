---
id: "hormuz-f6r.3"
title: "Analyze Japan, Korea, India, and Southeast Asia adjustment"
type: "task"
status: "done"
priority: "P1"
parent: "hormuz-f6r"
labels:
  - "asia"
  - "importers"
  - "imports"
  - "tradeflows"
blocked_by: []
blocks:
  - "hormuz-f6r.5"
  - "hormuz-s49.4"
children: []
owner: "jtbwedgwood@gmail.com"
created_at: "2026-07-06T06:09:44Z"
updated_at: "2026-07-06T23:40:00Z"
---

# Analyze Japan, Korea, India, and Southeast Asia adjustment

## Description

Assess how major Asian importers previously reliant on Hormuz cargoes are sourcing alternatives or reducing consumption.

## Acceptance Criteria

Country notes include exposure, alternative suppliers, storage buffers, policy response, and demand-side evidence.

## Dependency Notes

- Parent: `hormuz-f6r` - RQ3: Map destinations and importer adjustment
- Former blocker cleared for this task: `hormuz-f6r.1` - Build importer exposure matrix. The matrix still matters for downstream quantification/figures, but these country notes now stand on public-source evidence and completed KMZ/S49 notes.
- Cleared dependency: `hormuz-kmz.3` - Estimate supply removed, delayed, or rerouted
- Blocks: `hormuz-f6r.5` - Quantify replacement supply and demand destruction
- Blocks: `hormuz-s49.4` - Assess LNG and gas storage buffering

## Work Notes

- 2026-07-06: Claimed for preliminary Japan/Korea/India/Southeast Asia adjustment analysis. `hormuz-f6r.1` remains the formal matrix dependency, but country research can proceed using completed KMZ tables and will be reconciled after the matrix lands.
- 2026-07-06: Advanced and closed current-stage country adjustment analysis using completed KMZ/S49 notes plus public official/current sources. Removed `hormuz-f6r.1` as a blocker for this task because the acceptance criteria are met as country notes; reconciliation with the importer exposure matrix remains a downstream refinement for `hormuz-f6r.5`/`hormuz-f6r.6`, not a blocker here.

### Current-stage answer

High-confidence observed facts:

- EIA's 2024 route data put 84% of Hormuz crude/condensate and 83% of Hormuz LNG going to Asia. China, India, Japan, and South Korea together accounted for 69% of Hormuz crude/condensate flows; China, India, and South Korea accounted for 52% of Hormuz LNG flows. Source: EIA Today in Energy, 2025-06-16 and 2025-06-24, accessed 2026-07-06.
- Qatar/UAE LNG has no practical seaborne bypass in the completed KMZ/S49 notes; EIA says Qatar exported 9.3 Bcf/d and the UAE 0.7 Bcf/d of LNG through Hormuz in 2024. Source: EIA LNG chokepoint article, accessed 2026-07-06.
- Oil has more substitution optionality than LNG because Saudi Yanbu / East-West and UAE Fujairah routes can bypass Hormuz, but EIA's available spare bypass estimate is limited and KMZ notes caution that nameplate capacity is not spare capacity.
- Fertilizer, sulfur, LPG, naphtha, and petrochemical feedstocks matter for Asia, but public country-level inventory data are much weaker than oil/LNG data. Use these as exposure mechanisms unless country-specific stock evidence exists.

| Importer / group | Exposure | Alternative suppliers / routes | Storage buffers | Policy response | Demand-side evidence | Inference, kept separate |
| --- | --- | --- | --- | --- | --- | --- |
| Japan | Oil exposure is high because METI says Japan relies on the Middle East for more than 90% of crude imports; Qatar LNG exposure is modest because METI said Qatar was about 4% of Japan LNG imports. | Observed alternatives named by METI: Yanbu on Saudi Arabia's Red Sea coast, Fujairah in the UAE, increased U.S. procurement, and possible Central Asia/South America supply. METI estimated alternative crude procurement covering about 60% of May would-have-been Hormuz volume and 70%+ for June. | METI said public + private oil stockpiles totaled 254 days on 2026-03-03; Japan's IEA release allocation was about 79.8 mb / 80 mb. LNG buffer: METI said about three weeks of LNG stock; S49/IEA note gives LNG tank capacity equivalent to about 36 days of domestic gas demand, with no underground gas storage. | Private oil reserves began releasing 2026-03-16; national reserves began 2026-03-26; gasoline/fuel subsidies restarted 2026-03-19; third national release was canceled on 2026-05-15 after alternative procurement improved; private stockholding obligation stayed reduced from 70 to 55 days through 2026-06-15. | METI did not frame Japan as needing immediate broad demand cuts; it said current conditions had no immediate impact on oil supply/demand and focused on supply logistics, reserves, subsidies, anti-hoarding information, and LNG sharing between utilities. | Japan's adjustment looks like the cleanest "reserve bridge plus route substitution" case: high crude exposure but strong policy buffers, weak Qatar-LNG exposure, and limited evidence of demand destruction so far. |
| South Korea | High LNG and condensate exposure via Qatar; MOTIR states Qatar is Korea's third-largest LNG supplier and refers to four force majeure declarations after the Middle East war. EIA places South Korea among top Hormuz crude destinations and among China/India/Korea top Hormuz LNG destinations. | Observed alternative action is diplomatic/supplier prioritization, not a quantified replacement slate: MOTIR visited Saudi Arabia and Qatar to stabilize crude/gas supplies, and Qatar reaffirmed top-priority LNG/condensate supply to Korea once Hormuz normalized. | S49/IEA/KOGAS note: no underground gas storage; KOGAS stores gas as LNG in above-ground tanks. KOGAS terminals have 74 tanks and 6.56 bcm capacity; reserve rule equals 7 days mandatory + 30 days preventive reserves based on average daily domestic sales. Oil: IEA allocation was 22.5 mb; KNOC public material shows about 99.49 mb strategic reserves at end-2024 and 146 mb capacity. | MOTIR's visible response is energy diplomacy with Qatar/Saudi/UAE plus supply-chain cooperation. No public weekly reserve-release series or quantified private stockholding relief was found. | No official demand curtailment evidence found in reviewed public Korean sources; adjustment is framed around supplier assurance and LNG/condensate priority. | Korea is a "contract continuity under physical-route stress" case: sizeable Qatar exposure and good LNG tank rule/capacity on paper, but less public transparency on actual drawdown than Japan/India. |
| India | Crude: government said before the crisis about 45% of crude imports transited Hormuz. LNG/gas: government said total gas consumption was 189 MMSCMD, domestic production 97.5 MMSCMD, and 47.4 MMSCMD affected by force majeure; parliamentary statement used a 30 MMSCMD Gulf-source gas disruption figure. LPG: India imports about 60% of LPG consumption, and about 90% of those imports come through Hormuz. | Observed alternatives: crude imports from around 40 countries; non-Hormuz crude sourcing rose to about 70% of crude imports from 55% pre-conflict; additional crude and LNG cargoes were reported en route. LPG alternatives explicitly named: United States, Norway, Canada, Algeria, Russia, plus remaining Gulf sources. | Oil: PPAC FAQ says Phase-I strategic reserves are 5.33 MMT across Visakhapatnam, Mangalore, and Padur, with Phase-II 6.5 MMT approved in principle; official 2026 releases reviewed here emphasize commercial/government supply management rather than a quantified SPR draw. Gas storage: S49 found no public national gas-storage inventory comparable to GIE/KOGAS. Fertilizer: S49.5 supports India-only seasonal stock proxies for urea/DAP/MOP/NPKS. | Natural Gas Control Order on 2026-03-09 prioritized households/CNG at 100%, industry about 80%, fertilizer about 70%, and reduced gas to refineries/petrochemicals. LPG Control Order on 2026-03-08 directed refineries/petrochemical complexes to maximize LPG yields and route C3/C4 streams into domestic LPG; government created a committee for commercial LPG allocation, expanded delivery authentication, and increased booking intervals. | Strongest demand-side evidence among the reviewed countries: gas allocation cuts for industrial/fertilizer/refining/petrochemical users; commercial LPG allocation limits; minimum LPG booking gap increased; alternate fuels activated for hospitality/restaurant segment; anti-hoarding enforcement. | India is the clearest "substitution plus rationing by priority" case. Crude replacement looks relatively successful; LPG and gas show real demand management and sectoral rationing, especially outside households/CNG. |
| Southeast Asia, aggregate | IEA 2026 Southeast Asia Outlook says pre-crisis about 60% of regional crude imports and one-third of gas imports came from the Middle East, and 45% of oil product supply depended on Middle Eastern crude. IEA highlights naphtha, LPG, petrochemicals, refining, power generation, and cooking fuels as immediate pressure points. | Observed/current regional alternatives are less country-specific in public official material: IEA says governments are seeking alternative fuel supplies, reinforcing domestic energy preferences, and considering domestic oil/gas, coal, renewables, electrification, efficiency, and regional cooperation. | Public stock data are uneven and generally weaker than Japan/Korea. S49 did not find a regionwide public gas/oil stock dashboard comparable to GIE or KOGAS. Market journalism and regional commentary report country reserve figures, but treat those as secondary unless verified against official national sources. | IEA says near-term measures include demand restraint such as public transport and remote work, price controls/subsidies, and emergency efforts to secure alternative supplies. It also says regional fossil-fuel subsidies were about USD 40 billion before the crisis and are set to rise sharply in 2026. | IEA explicitly observes demand-restraint measures and fuel switching, including toward coal for power; it also notes EV incentives in Viet Nam and wider electrification/efficiency as resilience levers. | Southeast Asia is not one adjustment story. Singapore/Thailand/Viet Nam/Philippines are the key follow-up importers for LNG and refined-product exposure; Indonesia/Malaysia are partly cushioned by domestic resources but still exposed through oil products, LPG, petrochemicals, and regional prices. |

### Country notes

#### Japan

Observed facts:

- METI said on 2026-03-03 that some Japan-bound Middle East crude tankers had halted in the Persian Gulf, Japan depended on the Middle East for more than 90% of crude imports, and Japan had 254 days of oil stockpiles across public and private sectors.
- METI said Qatar supplied about 4% of Japan's LNG imports; Japan had LNG stock for about three weeks of national consumption and a system for ANRE-mediated LNG sharing among power and gas companies.
- On 2026-03-13, METI said private reserve release would begin 2026-03-16 and national reserve release in late March; on 2026-03-24 it specified roughly one month of national reserves beginning 2026-03-26 and roughly five days of joint producer-country stocks.
- METI named non-Hormuz alternatives: Saudi Yanbu, UAE Fujairah, U.S. procurement, and possibly Central Asia/South America. On 2026-05-15 it estimated alternative procurement for 60% of May and 70%+ of June would-have-been Hormuz crude, canceled a third national stockpile release, and maintained the private stockholding obligation reduction from 70 to 55 days.

Inference:

- Japan's crude adjustment is credible as a bridge for months, not a permanent solution: reserves and route-switching cover a large part of near-term flow, but not all normal Hormuz exposure. Demand-side evidence is weak; Japan's public response emphasizes logistics, reserves, subsidies, and anti-hoarding rather than reducing consumption.
- Japan is less exposed to Qatar LNG than Korea/India, so LNG is a price/spot-market risk more than a near-term volume crisis in the public METI record.

#### South Korea

Observed facts:

- EIA identifies South Korea as a top Hormuz crude destination and, with China and India, part of the top destination group for Hormuz LNG.
- MOTIR said Qatar is Korea's third-largest LNG supplier. The 2026-06-16 MOTIR release says the minister visited Qatar after Saudi Arabia to stabilize crude and gas supplies; Qatar reaffirmed Korea's top-priority status for LNG and condensate once Hormuz normalized and discussed Ras Laffan conditions after four force majeure declarations.
- S49.2 records Korea's IEA oil-stock release allocation at 22.5 mb and KNOC public material showing 99.49 mb strategic reserves at end-2024 and 146 mb capacity.
- S49.4 records Korea's LNG/gas buffer: no underground gas storage, KOGAS LNG tanks as the buffer, 74 tanks / 6.56 bcm storage capacity, and legal gas inventory equal to 7 days mandatory plus 30 days preventive reserves.

Inference:

- Korea appears more exposed to physical Qatar LNG interruption than Japan but has a clearer formal LNG inventory rule. The public record does not yet show how much of the 37-day reserve was physically available during the shock or how much demand was reduced.
- The visible adjustment path is diplomacy and contractual prioritization, not diversified replacement volumes. This should be treated as a medium-confidence stabilization channel rather than proof that lost LNG was fully replaced.

#### India

Observed facts:

- Government of India said on 2026-03-11 that crude supply was secure, daily consumption was about 55 lakh barrels, and secured diversified procurement exceeded normal Hormuz-route volume. It said crude imports from non-Hormuz routes had risen to about 70% from about 55% previously, with India importing crude from about 40 countries.
- The minister's 2026-03-12 parliamentary statement said about 45% of pre-crisis crude imports used the Hormuz route and that refineries were operating at high utilization, in some cases above 100%.
- For gas, the 2026-03-11 briefing said total consumption was about 189 MMSCMD, domestic production 97.5 MMSCMD, and 47.4 MMSCMD affected by force majeure. The 2026-03-12 parliamentary statement described a 30 MMSCMD Gulf-source gas disruption from a major Qatari processing facility.
- The Natural Gas Control Order prioritized 100% supply for household PNG/CNG, about 80% for industrial/manufacturing users, about 70% for fertilizer plants, and managed reductions for refineries/petrochemicals.
- For LPG, India said it imports about 60% of consumption and roughly 90% of imports come through Hormuz. The LPG Control Order redirected refinery/petrochemical C3/C4 streams into LPG, increasing domestic LPG output by about 25% in the briefing / 28% in the parliamentary statement. Alternative LPG suppliers named in Parliament were the United States, Norway, Canada, Algeria, and Russia.
- Commercial LPG was rationed: a committee was created for restaurant/hotel/commercial allocations, commercial LPG allocation was set at 20% of average monthly requirement from 2026-03-12, and the domestic booking gap was increased from 21 to 25 days in one release and described as 25 days urban / 45 days rural in the parliamentary statement.

Inference:

- India's crude adjustment is the strongest observed substitution case in this task: government-reported non-Hormuz crude sourcing rose quickly and refineries kept running. But LPG and gas show real scarcity, with explicit priority allocation and demand management.
- Fertilizer and petrochemicals are the key Indian second-round channels. The government protected fertilizer at about 70% gas supply, which is a cut but less severe than refinery/petrochemical gas reductions; S49.5's fertilizer stock notes support treating India as the best public case study for days-of-cover proxies.

#### Southeast Asia

Observed facts:

- IEA says Southeast Asia's pre-crisis exposure was around 60% of crude imports from the Middle East, one-third of gas imports from the Middle East, and 45% of oil product supply dependent on Middle Eastern crude.
- IEA says immediate impacts are concentrated in refining, petrochemicals, power generation, cooking fuels, naphtha, LPG, and chemical products. It also notes many regional refineries are configured for medium/heavy Gulf crudes, reducing flexibility and utilization when those crudes are lost.
- IEA says governments are using short-term demand restraint, including public transport and remote work, emergency interventions such as price controls and subsidies, and efforts to secure alternative fuel supplies.
- IEA says the shock has tightened LNG markets and prompted some fuel switching toward coal; it also points to EV incentives in Viet Nam and the broader role of electrification, efficiency, renewables, domestic resources, and regional cooperation.

Inference:

- Treat Southeast Asia as a cluster, not a single importer. The key high-exposure follow-up countries are Singapore, Thailand, Viet Nam, and the Philippines for LNG/refined products/petrochemicals and LPG; Indonesia and Malaysia have domestic-resource cushions but remain exposed through products, LPG, petrochemicals, and regional price spillovers.
- The region's near-term buffers look thinner and less transparent than Japan/Korea oil/gas reserves. The rigorous current claim is not "X days of cover" but "visible demand restraint plus subsidies/price controls plus alternative cargo searches, against high structural Middle East dependence."

### Source breadcrumbs

All sources accessed 2026-07-06.

- EIA, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint," 2025-06-16: https://www.eia.gov/todayinenergy/detail.php?id=65504
- EIA, "About one-fifth of global liquefied natural gas trade flows through the Strait of Hormuz," 2025-06-24: https://www.eia.gov/todayinenergy/detail.php?id=65584
- METI, press conference excerpt, 2026-03-03: https://www.meti.go.jp/english/speeches/press_conferences/2026/0303001.html
- METI, press conference excerpt, 2026-03-13: https://www.meti.go.jp/english/speeches/press_conferences/2026/0313001.html
- METI, press conference excerpt, 2026-03-24: https://www.meti.go.jp/english/speeches/press_conferences/2026/0324001.html
- METI, "Lowered Private Oil Stockpiling Obligation to Be Maintained," 2026-05-15: https://www.meti.go.jp/english/press/2026/0515_003.html
- IEA, "Japan Natural Gas Security Policy": https://www.iea.org/articles/japan-natural-gas-security-policy
- MOTIR, "Korea, Qatar Agree to Resume Stable LNG Imports and Expand Cooperation in Advanced Industries," 2026-06-16: https://english.motir.go.kr/eng/article/EATCLdfa319ada/2661/view
- IEA, "Korea Natural Gas Security Policy": https://www.iea.org/articles/korea-natural-gas-security-policy
- KOGAS LNG terminal/storage pages used by S49.4: https://www.kogas.or.kr/site/eng/1040303000000 and https://www.kogas.or.kr/site/eng/1030903020000
- PIB India, "Inter-Ministerial Briefing held on Recent Developments in West Asia," 2026-03-11: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2238525&lang=1&reg=3
- PIB India, "Statement by Union Minister for Petroleum and Natural Gas...," 2026-03-12: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2239021&lang=2&reg=3
- PPAC FAQ on India's strategic petroleum reserves: https://ppac.gov.in/faqs
- IEA, "India Gas Market Report," executive summary, 2025: https://www.iea.org/reports/india-gas-market-report/executive-summary
- IEA, "Southeast Asia Energy Outlook 2026," executive summary: https://www.iea.org/reports/southeast-asia-energy-outlook-2026/executive-summary
- IEA, "Strait of Hormuz crisis reinforces need for Southeast Asia to tackle major energy vulnerabilities," 2026-06-16: https://www.iea.org/news/strait-of-hormuz-crisis-reinforces-need-for-southeast-asia-to-tackle-major-energy-vulnerabilities
- Local source anchors used: `issues/done/hormuz-kmz.1-estimate-normal-hormuz-export-flows-by-country-and-product.md`, `issues/done/hormuz-kmz.3-estimate-supply-removed-delayed-or-rerouted.md`, `issues/done/hormuz-kmz.7-produce-product-disruption-master-table.md`, `issues/done/hormuz-s49.2-quantify-oecd-and-us-reserve-response.md`, `issues/blocked/hormuz-s49.4-assess-lng-and-gas-storage-buffering.md`, `issues/done/hormuz-s49.5-assess-fertilizer-and-chemical-inventory-buffers.md`.

### Completion Note

- 2026-07-06: Acceptance criteria met for current stage. Country notes cover exposure, alternative suppliers/routes, storage buffers, policy response, and demand-side evidence for Japan, Korea, India, and Southeast Asia, with observed facts separated from inference. No derived CSV was added.
