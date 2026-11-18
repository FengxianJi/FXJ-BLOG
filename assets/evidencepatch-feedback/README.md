# EvidencePatch feedback figures

Aggregate-only assets for the bilingual EvidencePatch post. No paper text, reviews, credentials, or per-paper identifiers are included.

- `main_framework.svg`: three-panel main figure: method workflow, separate evaluation endpoints, and frozen-input repeatability. `main_framework.png` is a raster export.
- `score_effects`, `discordance`, `repeatability`: charts supplied as SVG, PNG, and PDF.
- `aggregate_data.json`: source hashes and aggregate values. The two endpoints have different scales and eligible populations. Score effects are AI judgments; concern outcomes remain same-family proxies.

Rebuild from the repository root with `python3 scripts/build_feedback_figures.py` (Python standard library and gnuplot). For the main PNG, run `convert -background white assets/evidencepatch-feedback/main_framework.svg assets/evidencepatch-feedback/main_framework.png` if ImageMagick is available.

The diagram's budget-planning flow summarizes the proposed method. The 300-paper intervention tests frozen-body evidence appendices, not the complete planner or repeated revision efficacy. Disagreement counts are conditional on 55 proxy-improved papers among 284 eligible papers. Repeatability compares three-rating paper means in two executions on unchanged inputs.
