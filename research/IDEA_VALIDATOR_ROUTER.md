# Roblox Game Idea Validator & Research Router

> **Purpose:** Lightweight rule & router for any AI agent evaluating a new Roblox game concept, mechanic, or pivot for this project. Read this file first instead of loading entire 30-page PDFs into context.

## 1. Knowledge Base Router (Where to Look)

Consult these durable local documents based on the question:

| Document | Path | What it contains | When to read |
| :--- | :--- | :--- | :--- |
| **Deep Trends & Psychology (28 pp.)** | `output/pdf/Roblox_Trends_2020_2025_Deep_Research_RU.pdf` | 2020–2025 monthly top-game map (pp. 7–12), psychological engines (pp. 6, 16), 5-loop retention ladder (p. 17), RFY algorithm & weekly cadence (pp. 14–15, 18), 2026–2027 forecast (pp. 19–20), Dark Fantasy Keeper thesis (p. 21), guardrails (p. 24). | Checking macro trends, psychological needs, RFY metrics, seasonality, or retention loops. |
| **10-Idea Evaluation Report (PDF)** | `output/pdf/Roblox_10_Game_Ideas_Evaluation_RU.pdf` | Strict 100-point Top-10 audit of the 10 proposed concepts + Mini-Game Hub vs live Roblox competitors, CCU benchmarks, fatal flaws, and pivot recipes. | Avoiding repeated mistakes, checking competitor benchmarks, or seeing the strict Top-10 filter. |
| **10-Idea Deep-Dive Playbook (12 pp.)** | `output/pdf/Roblox_10_Ideas_Deep_Dive_Playbook_RU.pdf` | 1 dedicated page per game: Bull/Bear case, 5-loop 2026–2027 redesign, fair monetization, 2-week MVP, and realistic small-team CCU/DevEx tiers (500–3,000+ CCU). | Turning a promising raw concept into a profitable small-team hit (500–5,000+ CCU) or planning a 2-week MVP. |
| **Raw Concept Deck 1** | `research/inputs/roblox_mini_game_hub_visual_concept.pdf` | Original 5 mini-game hub definitions (`Ice Arena`, `Teacher Abuse`, `Build & Break`, `Color Switch Panic`, `Don't Look Behind`). | Checking original wording/art of Deck 1. |
| **Raw Concept Deck 2** | `research/inputs/Roblox_5_Yangi_Oyin_Goyalari_Rasmlar_Bilan.pdf` | Original 5 standalone ideas (`Lost City`, `Restaurant Empire`, `Deep Ocean`, `Delivery Rush`, `Dream Park`). | Checking original wording/art of Deck 2. |
| **Live Production State** | `GRAPHICS.md` | Current Pink House Studio build, asset inventory, performance profiles, and audit log. | Checking technical feasibility or integrating a mechanic into Pink House. |

---

## 2. Hard Auto-Reject / Red-Flag Gates (Check FIRST)

Before scoring, check these 5 instant blockers. If any triggers, flag it prominently at the top of the verdict:

1. **Moderation / Policy Trap:** Does the title, theme, or core verb risk Roblox Safety takedown or discovery suppression? *(Example: "Teacher Abuse" violates school harassment/violence sensitivity; paid-item theft or undisclosed randomized odds violate Roblox Monetization policy.)*
2. **Unfocused Hub Trap:** Is it a multi-game hub trying to launch 4–5 unrelated genres at once? Post-2025 RFY rewards one crystal-clear thumbnail promise and low first-play bounce; ship the single strongest loop standalone first.
3. **Clone Without Systemic Twist:** Does an entrenched evergreen (`Color Block`, `Epic Minigames`, `Theme Park Tycoon 2`, `Restaurant Tycoon 2`, `Taxi Boss`, `Brookhaven`) already own this exact loop with 5–10 years of content? A visual reskin alone fails.
4. **Content-Treadmill / Passive-Walk Trap:** Does retention depend on hand-building new puzzles/maps every week with no player-generated drama or compounding ownership? *(Example: pure puzzle adventure or passive observation without catching/risk/status.)*
5. **Unverified Closed Data:** Never invent private Creator Analytics, D1/D7 numbers, or revenue. Mark estimates/inferences explicitly and verify live competitors via web search if not already in the PDFs.

---

## 3. Mandatory 100-Point Scoring Rubric

Score every proposed Roblox game idea objectively across 6 weighted pillars:

| # | Pillar | Max | Key Question |
| :- | :--- | :-: | :--- |
| 1 | **10-Second Hook & Clip Virality** | **15** | Can a player understand the fantasy in <10 sec and generate a funny/tense 10-sec TikTok/Shorts clip? |
| 2 | **Competitor Space & Differentiation** | **15** | Is there a real gap against live Roblox competitors (verified via web/Rolimon's/RoMonitor), or is it saturated? |
| 3 | **Retention Ladder (D1 / D7 / D28)** | **20** | Does it satisfy all 5 nested loops (0–10s, 10–90s, 3–15m, 1–7d, 2–4w) with compounding ownership or mastery? |
| 4 | **Social Generativity & Co-Play** | **20** | Do players create stories, drama, or mutual dependency for each other (driving RFY `intentional co-play`)? |
| 5 | **2026–2027 Trend & RFY Fit** | **15** | Does it align with high-confidence 2026–2027 engines (cozy+danger 75%, co-op survival 70%, social ownership 70%, creator live events 65%)? |
| 6 | **Feasibility, Mobile & Policy Safety** | **15** | Can a small team ship a vertical slice in 2–4 weeks, hit smooth low-end mobile performance, and pass Roblox moderation cleanly? |

### Verdict Thresholds
- **75–100 — BUILD (Green):** Strong top-potential candidate; proceed to a 1-week instrumented MVP test.
- **55–74 — PIVOT (Amber):** Core spark is viable, but has 1–2 fatal gaps (naming, retention, or differentiation); specify exact required upgrades before writing code.
- **0–54 — KILL (Red):** Saturated, low-retention, or structurally mismatched with 2026–2027 RFY; do not build as proposed (salvage at most 1 mechanic if useful elsewhere).

---

## 4. Required Output Format When Evaluating Any Idea

Every agent evaluation must output:
1. **Scorecard Table** (6 pillars + total `/100` + `BUILD / PIVOT / KILL` verdict).
2. **Live Competitor Check** (named Roblox competitors, typical CCU range if available, saturation level).
3. **5-Loop Retention Check** (`0–10s` → `10–90s` → `3–15m` → `1–7d` → `2–4w`).
4. **Fatal Flaws & Red Flags** (honest list — no sugarcoating).
5. **Top-Potential Upgrade Recipe** (the 2–3 concrete changes required if the user insists on building it).
6. **1-Week MVP Kill/Go Gate** (exact playable test + metrics: PTR, bounce <60s, first reward <90s, co-play replay).
