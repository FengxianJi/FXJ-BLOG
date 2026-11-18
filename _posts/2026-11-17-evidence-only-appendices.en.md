---
layout: post
title: "EvidencePatch: When Does Revising a Paper from AI Reviews Actually Help?"
date: 2026-11-17 10:00:00 +0000
last_modified_at: 2026-11-18
categories: research
permalink: /en/research/2026/11/17/evidence-only-appendices/
lang: en
translation_url: /research/2026/11/17/evidence-only-appendices/
comments: true
math: true
---

**Code and experimental resources:** [GitHub repository](https://github.com/FengxianJi/EvidencePatch) · [Results and figures](https://github.com/FengxianJi/EvidencePatch/tree/main/results) · [Download ZIP](https://github.com/FengxianJi/EvidencePatch/archive/refs/heads/main.zip)

Send a paper to an AI reviewer, follow its suggestions, and ask for another review. The loop feels natural. But what does a higher score establish? And what should we conclude when the model judges a response more adequate while giving the paper a lower score?

EvidencePatch studies this feedback loop through evidence-grounded revision. Our current experiments show that improvement in a local concern-resolution proxy does not guarantee a higher overall AI recommendation score. Repeated evaluation of an unchanged version also produces paper-level variation.



![EvidencePatch workflow, evaluation disconnect, and repeatability]({{ '/assets/evidencepatch-feedback/main_framework.svg' | relative_url }})

*Figure 1. The method workflow, separately measured outcomes, and review stability. The two endpoints use different scales and eligible populations; their magnitudes are not directly comparable.*

## Turning a concern into an action

Consider an illustrative reviewer comment: “The paper does not explain how this hyperparameter was chosen.” The explanation might already exist in the paper, require a supported clarification, or depend on a sensitivity experiment that has never been run. Each situation calls for a different action.

EvidencePatch makes this distinction explicit:

1. **Decompose the review** into checkable concerns and identify the affected claims.
2. **Retrieve evidence** from the paper and available experimental artifacts, preserving source locations and version hashes.
3. **Plan under a budget:** choose evidence pointers, clarification, or experiments, while retaining unresolved concerns when support is missing. A risk-aware planner estimates relevance, uncertainty, and cost.
4. **Generate and verify a patch:** connect responses to sources and require completed execution artifacts for experimental result claims.

The implementation includes BM25 retrieval and risk-aware planning. Our 300-paper primary experiment tests a narrower intervention: a targeted appendix built from existing evidence while the main text remains frozen. It does not establish the superiority of the full planner, and it does not rerun experiments for every paper.

A schematic budgeted objective expresses the planning idea:
<div class="math-display">
\[
\mathcal A^*=\underset{\mathcal A\subseteq\mathcal C}{\operatorname{argmax}}\;\sum_{a\in\mathcal A}\left[\widehat g(a)-\lambda\widehat r(a)\right],\qquad\sum_{a\in\mathcal A}\widehat c(a)\leq B.
\]
</div>

Here $$\mathcal C$$ is the candidate action pool; $$\widehat g$$, $$\widehat r$$, and $$\widehat c$$ denote estimated gain, risk, and cost; $$B$$ is the budget and $$\lambda$$ controls the risk penalty. This summarizes the method design. Estimated gain is not verified resolution, and the primary appendix experiment does not validate this full objective.

## Adding evidence did not improve average scores

We evaluated 300 papers with human reviews under five conditions: original paper C0, neutral appendix C1, clarification C2, reproducibility information C3, and targeted evidence C5. MiniMax-M3 scored each condition three times; the analysis averages scores within each paper.

We define score changes as follows:
<div class="math-display">
\[
\bar S_i^{(c)}=\frac{1}{K}\sum_{k=1}^{K}S_{ik}^{(c)},\qquad d_i^S=\bar S_i^{(C5)}-\bar S_i^{(C0)},\qquad \Delta_S=\frac{1}{N}\sum_{i=1}^{N}d_i^S.
\]
</div>

$$S_{ik}^{(c)}$$ is the rating of paper $$i$$ under condition $$c$$ on repeat $$k$$; here $$K=3$$ and $$N=300$$. The 1–5 recommendations are ordinal; averaging them is the descriptive aggregation used in this experiment.

| Contrast | Papers | Mean change (1–5 scale) | 95% CI | Raw p | Holm secondary p |
|---|---|---|---|---|---|
| C1 placebo − C0 baseline | 300 | -0.071 | [-0.113, -0.028] | 0.00216 | 0.00431 |
| C2 clarification − C0 baseline | 300 | -0.054 | [-0.094, -0.013] | 0.0236 | 0.0236 |
| C3 reproducibility − C0 baseline | 300 | -0.092 | [-0.132, -0.052] | 5.87e-06 | 1.76e-05 |
| C5 targeted evidence − C0 baseline (primary) | 300 | -0.233 | [-0.281, -0.187] | 2.34e-17 | — |


C5 also scored 0.162 points below the length-matched neutral appendix. A separate M3 execution on the same cohort produced a C5−C0 effect of −0.216. Qwen3 and Mistral showed negative effects of −0.857 and −0.133, respectively.

These appendices did not raise the evaluators’ average scores. The result does not identify the cause of the decline or establish that scientific quality deteriorated.



![C5 minus C0 across four scoring panels]({{ '/assets/evidencepatch-feedback/score_effects.svg' | relative_url }})

*Figure 2. Separate estimates on the same 300-paper cohort. M3 uses three ratings per condition; Qwen3 and Mistral use one. The M3 rerun does not add independent papers.*

### Same-cohort evaluator estimates

The M3 primary run, a separate M3 execution, Mistral, and Qwen3 are reported separately; scores from different evaluators are not pooled.

| Evaluator/run | Papers | C5 − C0 | 95% CI | Raw p |
|---|---|---|---|---|
| MiniMax-M3 primary | 300 | -0.233 | [-0.281, -0.187] | 2.34e-17 |
| MiniMax-M3 same-cohort execution rerun | 300 | -0.216 | [-0.261, -0.170] | 8.48e-18 |
| Mistral-7B-Instruct CPU | 300 | -0.133 | [-0.210, -0.060] | 4.26e-04 |
| Qwen3-8B CPU | 300 | -0.857 | [-0.957, -0.757] | 3.29e-45 |

## A better local response can coexist with a lower overall score

We separately ran a randomized A/B concern assessment over the 300 papers. MiniMax-M3 labeled concern validity, repairability, and resolution under both versions. This is a same-family automated proxy; independent expert labels have not been returned.

Of the papers, 284 contained at least one model-labeled valid and repairable concern, giving 873 eligible concern pairs. Unresolved, partially resolved, and fully resolved labels are mapped to 0, 0.5, and 1. We average eligible labels within each paper before averaging across papers. The C5−C0 paper-macro proxy change was **+0.0559**, with a 95% interval of **[+0.0402, +0.0730]**. This weighted status proxy is neither a 1–5 recommendation score nor a directly equivalent increase in the fraction of fully resolved concerns.

The concern proxy has a different definition:
<div class="math-display">
\[
q_{ij}^{(c)}\in\{0,\tfrac12,1\},\quad R_i^{(c)}=\frac{1}{|E_i|}\sum_{j\in E_i}q_{ij}^{(c)},\quad \Delta_R=\frac{1}{|I_E|}\sum_{i\in I_E}\left(R_i^{(C5)}-R_i^{(C0)}\right).
\]
</div>

$$E_i$$ contains the concerns the model labels valid and repairable using existing evidence, clarification, or reanalysis. $$I_E=\{i:|E_i|>0\}$$ contains 284 papers. Labels $$q$$ encode unresolved, partial, and full resolution. New-experiment concerns are outside this denominator; papers receive equal weight.

The paper-level pairing reveals the mismatch:

| Among the 55 papers whose resolution proxy improved | Papers |
|---|---:|
| Overall score increased | 10 |
| Overall score stayed the same | 20 |
| Overall score decreased | 25 |

Across the 284 eligible papers, Spearman correlation between the two changes was 0.069, with a 95% interval spanning zero. **Under this evaluation setup, a positive AI judgment about a local response does not guarantee a higher overall AI recommendation.**

Source hashes and randomized condition mapping passed integrity checks. However, only 87.4% of nonempty supporting quotations matched the source text exactly, and two exceeded the requested word limit. Exact matching checks provenance, not whether a quotation logically supports a response. The observed proxy improvement therefore cannot be treated as expert-confirmed resolution.



![Overall score directions among 55 proxy-improved papers]({{ '/assets/evidencepatch-feedback/discordance.svg' | relative_url }})

*Figure 3. Score directions conditional on a positive concern-resolution proxy change. These are paired results, not new samples or expert resolution rates.*

## Why can the feedback loop come apart?

The two assessments receive different context and answer different questions. The holistic scorer sees the manuscript and supplement, without the complete original reviews; the C5 appendix itself contains selected review excerpts. The concern assessor sees the original reviews and compares the two versions concern by concern. Their outputs need not move together.

The proxy also covers a narrower set of problems. Among 1,745 extracted concerns, 717 were classified as requiring new experiments and 92 as core-method or claim defects. Neither category enters the eligible paired proxy. An appendix can improve a local explanation while leaving a major scientific gap intact.

The action categories offer a descriptive clue. For concerns classified as addressable with existing evidence, 24 of 80 moved from unresolved to partial or full resolution. The corresponding counts were 39 of 539 for clarification and 12 of 254 for reanalysis. This is consistent with evidence localization being most useful when the evidence already exists. Both the categories and outcomes remain model judgments.

We have not established whether the lower overall scores result from weak relevance, newly salient gaps, or evaluator sensitivity to presentation. A weak positive association appeared in one exploratory subgroup, but largely disappeared when the score contrast used the neutral appendix as its comparator. It does not identify a reliable condition for score improvement.

## Asking again can change the score even without a revision

Observed score changes also include evaluation variability. Across two M3 executions on unchanged papers and appendices, each averaging three ratings per condition, paper-level means matched exactly for only 47.7% of original packets and 43.3% of C5 packets.

The average C5−C0 effect remained negative, changing from −0.233 to −0.216. Yet the cross-run Pearson correlation of individual paper effects was only 0.105. An aggregate pattern can reproduce while individual improvement judgments remain unstable.

Our separate ten-paper iterative development pilot did not achieve stable improvement for every paper. Some failed cases used candidates selected for their development scores, introducing selection bias. Since successive rounds also change the candidate, their trajectories combine revision effects with evaluation variability. An isolated high score does not establish stable success.

Exact agreement between the three-rating means in two executions is:
<div class="math-display">
\[
A_c=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}\!\left[\bar S_{i,\mathrm{run1}}^{(c)}=\bar S_{i,\mathrm{run2}}^{(c)}\right].
\]
</div>

The indicator $$\mathbf 1[\cdot]$$ measures agreement on unchanged packets. This is score repeatability, not semantic agreement between review texts.

![Exact agreement of paper means across repeated frozen-input evaluations]({{ '/assets/evidencepatch-feedback/repeatability.svg' | relative_url }})

*Figure 4. Equal paper-mean scores across two runs. The manuscript version is unchanged; this agreement rate does not measure review accuracy.*

## What do the development baselines show?

The following tables complete the empirical picture. The 100-paper development cohort is separate from the primary 300-paper experiment. These score panels evaluate controls and method variants under their respective protocols; they are not one randomized, cost-matched confirmation of the full planner. The first table has ten baseline/control conditions, while the unified rescore includes two proposed variants.

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

*Figure 5. Ten registered baseline/control conditions on the separate 100-paper development cohort.*

[Download PDF figure]({{ '/assets/results-2026-11-18/figure_02_baseline_methods100.pdf' | relative_url }})

## BM25 risk-aware method and rescoring

The initial run evaluated method generation and scoring. The next two passes blindly rescored frozen outputs; they did not regenerate patches.

| Run | Papers | Mean change | 95% CI | Raw p | Run type |
|---|---|---|---|---|---|
| BM25 risk-aware initial run | 100 | +0.14 | [+0.03, +0.26] | 0.0333 | Method run and M3 score; exploratory |
| Frozen-output blind rescore 02 | 100 | +0.12 | [+0.02, +0.22] | 0.0428 | Rescore of frozen outputs; not method-generation replication |
| Frozen-output blind rescore 03 | 100 | +0.11 | [-0.01, +0.22] | 0.0895 | Rescore of frozen outputs; not method-generation replication |

The third rescore’s confidence interval includes zero. Paper-level score changes were weakly correlated across passes (ρ=0.157).

![BM25 risk-aware run and frozen-output rescoring]({{ '/assets/results-2026-11-18/figure_03_bm25_repeatability.png' | relative_url }})

*Figure 6. BM25 method run and repeated scoring of its frozen outputs.*

[Download PDF figure]({{ '/assets/results-2026-11-18/figure_03_bm25_repeatability.pdf' | relative_url }})

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

*Figure 7. Unified rescoring of ten controls and two EvidencePatch variants; all adjusted p-values exceed 0.05.*

[Download PDF figure]({{ '/assets/results-2026-11-18/figure_04_unified_repeat03.pdf' | relative_url }})

Only aggregate results from completed score panels are included here. Expert annotations are not part of these score metrics; results from separate designs are reported separately.

## Evaluating a revision loop

Each iteration should ask whether the original concern was valid, whether the response has sufficient evidence, whether the specific gap was resolved, whether the revision introduced problems, and whether the overall judgment changed reliably.

Concern IDs, version hashes, and evidence records make these questions traceable. Fixed-concern reassessment should accompany fresh review. A concern disappearing from the next review does not establish that it was resolved; different wording does not automatically identify a new concern.

Stopping should reflect evidence and budget. The system should stop when no supported action remains, when required experiments cannot currently be executed, or when the budget is exhausted, while preserving unresolved issues. Repeatedly sampling until a score reaches four risks mistaking evaluator variation for progress.

EvidencePatch’s clearest current finding is that this feedback loop needs separate measurements of **local responses, overall scores, and review stability**. We have implemented the evidence-constrained workflow and observed a disconnect among these outcomes. Independent expert adjudication of evidence support and substantive resolution remains the next critical step.

## Code, data, and reproduction resources

The [public EvidencePatch repository](https://github.com/FengxianJi/EvidencePatch) includes the method and ten registered controls, anonymous numeric outcomes, complete aggregate tables, figure exports, and reproduction scripts.

| Resource | Location |
|---|---|
| Method and baseline implementations | [method/](https://github.com/FengxianJi/EvidencePatch/tree/main/method) |
| Complete result tables | [results/tables/](https://github.com/FengxianJi/EvidencePatch/tree/main/results/tables) |
| Main figure and experiment plots (SVG / PNG / PDF) | [results/figures/](https://github.com/FengxianJi/EvidencePatch/tree/main/results/figures) |
| Anonymous numeric records and metric definitions | [Data guide](https://github.com/FengxianJi/EvidencePatch/blob/main/docs/DATA.md) |
| Reproduction and plotting commands | [scripts/](https://github.com/FengxianJi/EvidencePatch/tree/main/scripts) |

After downloading the repository, run `python3 scripts/reproduce_results.py` to recompute headline means, correlation, and disagreement counts without API calls or a GPU. Method demonstrations use explicitly synthetic inputs. Source papers, review text, credentials, and raw model responses are excluded. The original API study and expert adjudication cannot be reproduced from these public artifacts alone; the repository README describes the supported scope.
