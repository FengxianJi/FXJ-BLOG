---
layout: post
title: "EvidencePatch: Completed Experiment Results, Tables, and Figures"
date: 2026-11-18 03:00:00 +0000
categories: research
permalink: /en/research/2026/11/18/completed-experiment-results/
lang: en
translation_url: /research/2026/11/18/completed-experiment-results/
comments: true
---

This post collects completed score-evaluation panels with aggregate metrics. The scores are AI-reviewer proxies; they are not expert-confirmed concern resolution and do not establish a change in scientific quality. The 95% confidence intervals use paper-level bootstrap resampling.

## Confirmatory 300-paper experiment

MiniMax-M3 scored five conditions three times each for 300 papers. The primary contrast compares C5, the targeted evidence appendix, with C0, the unchanged paper.

| Contrast | Papers | Mean change (1–5 scale) | 95% CI | Raw p | Holm secondary p |
|---|---|---|---|---|---|
| C1 placebo − C0 baseline | 300 | -0.071 | [-0.113, -0.028] | 0.00216 | 0.00431 |
| C2 clarification − C0 baseline | 300 | -0.054 | [-0.094, -0.013] | 0.0236 | 0.0236 |
| C3 reproducibility − C0 baseline | 300 | -0.092 | [-0.132, -0.052] | 5.87e-06 | 1.76e-05 |
| C5 targeted evidence − C0 baseline (primary) | 300 | -0.233 | [-0.281, -0.187] | 2.34e-17 | — |

![300-paper primary experiment and evaluator-family estimates]({{ '/assets/results-2026-11-18/figure_01_primary300.png' | relative_url }})

[下载 PDF 图版]({{ '/assets/results-2026-11-18/figure_01_primary300.pdf' | relative_url }})

## Evaluator checks on the same cohort

The M3 primary run, a separate M3 execution, Mistral, and Qwen3 are reported separately; scores from different evaluators are not pooled.

| Evaluator/run | Papers | C5 − C0 | 95% CI | Raw p |
|---|---|---|---|---|
| MiniMax-M3 primary | 300 | -0.233 | [-0.281, -0.187] | 2.34e-17 |
| MiniMax-M3 same-cohort execution rerun | 300 | -0.216 | [-0.261, -0.170] | 8.48e-18 |
| Mistral-7B-Instruct CPU | 300 | -0.133 | [-0.210, -0.060] | 4.26e-04 |
| Qwen3-8B CPU | 300 | -0.857 | [-0.957, -0.757] | 3.29e-45 |

## Exploratory 10-method benchmark on 100 papers

One MiniMax-M3 evaluator scored each method once. Holm p-values correct for the method comparisons in this benchmark. Cost-greedy changed the score proxy by −0.14 (Holm p=0.023); this is a score change, not evidence that scientific quality declined.

| Method | Papers | Mean change vs. original | 95% CI | Holm p |
|---|---|---|---|---|
| Frozen original | 100 | +0.00 | [+0.00, +0.00] | — |
| One-shot generic LLM | 100 | -0.07 | [-0.19, +0.05] | 1 |
| Iterative generic LLM | 100 | -0.07 | [-0.19, +0.05] | 1 |
| DRPG-style | 100 | +0.00 | [-0.13, +0.13] | 1 |
| Retrieval only | 100 | -0.05 | [-0.13, +0.03] | 1 |
| Peerify-verify | 100 | +0.00 | [+0.00, +0.00] | 1 |
| Random budget | 100 | -0.11 | [-0.20, -0.02] | 0.213 |
| Cost-greedy | 100 | -0.14 | [-0.23, -0.06] | 0.0232 |
| All feasible | 100 | -0.10 | [-0.20, +0.00] | 0.527 |
| Oracle selector | 100 | -0.06 | [-0.14, +0.01] | 1 |

![Exploratory 10-method score-proxy comparison on 100 papers]({{ '/assets/results-2026-11-18/figure_02_baseline_methods100.png' | relative_url }})

[下载 PDF 图版]({{ '/assets/results-2026-11-18/figure_02_baseline_methods100.pdf' | relative_url }})

## BM25 risk-aware method and rescoring

The initial run evaluated method generation and scoring. The next two passes blindly rescored frozen outputs; they did not regenerate patches.

| Run | Papers | Mean change | 95% CI | Raw p | Run type |
|---|---|---|---|---|---|
| BM25 risk-aware initial run | 100 | +0.14 | [+0.03, +0.26] | 0.0333 | Method run and M3 score; exploratory |
| Frozen-output blind rescore 02 | 100 | +0.12 | [+0.02, +0.22] | 0.0428 | Rescore of frozen outputs; not method-generation replication |
| Frozen-output blind rescore 03 | 100 | +0.11 | [-0.01, +0.22] | 0.0895 | Rescore of frozen outputs; not method-generation replication |

The third rescore’s confidence interval includes zero. Paper-level score changes were weakly correlated across passes (ρ=0.157).

![BM25 risk-aware run and frozen-output rescoring]({{ '/assets/results-2026-11-18/figure_03_bm25_repeatability.png' | relative_url }})

[下载 PDF 图版]({{ '/assets/results-2026-11-18/figure_03_bm25_repeatability.pdf' | relative_url }})

## Unified rescore of 12 frozen methods

This is a unified blind rescore on the same 100-paper development cohort, not a fresh method-generation experiment. It covers 1,200/1,200 score cells. Section-context has raw p=0.053 and Holm-adjusted p=0.586.

| Method | Papers | Mean change vs. rescore original | 95% CI | Holm p |
|---|---|---|---|---|
| Frozen original | 100 | +0.00 | [+0.00, +0.00] | — |
| One-shot generic LLM | 100 | -0.07 | [-0.18, +0.04] | 1 |
| Iterative generic LLM | 100 | -0.11 | [-0.22, +0.00] | 0.801 |
| DRPG-style | 100 | -0.03 | [-0.15, +0.09] | 1 |
| Retrieval only | 100 | -0.06 | [-0.18, +0.06] | 1 |
| Peerify-verify | 100 | +0.03 | [-0.08, +0.14] | 1 |
| Random budget | 100 | -0.03 | [-0.15, +0.09] | 1 |
| Cost-greedy | 100 | -0.04 | [-0.17, +0.09] | 1 |
| All feasible | 100 | +0.05 | [-0.06, +0.16] | 1 |
| Oracle selector | 100 | -0.04 | [-0.17, +0.09] | 1 |
| EvidencePatch risk-aware | 100 | +0.03 | [-0.09, +0.15] | 1 |
| EvidencePatch section-context | 100 | +0.13 | [+0.01, +0.25] | 0.586 |

![Unified rescore of 12 frozen method outputs]({{ '/assets/results-2026-11-18/figure_04_unified_repeat03.png' | relative_url }})

[下载 PDF 图版]({{ '/assets/results-2026-11-18/figure_04_unified_repeat03.pdf' | relative_url }})

Only aggregate results from completed score panels are included here. Expert annotations are not part of these score metrics; results from separate designs are reported separately.
