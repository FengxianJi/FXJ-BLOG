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

| Contrast | Mean change on the 1–5 score scale | 95% paper-bootstrap interval |
|---|---:|---|
| Neutral appendix C1 − original C0 | −0.071 | [−0.113, −0.028] |
| Clarification C2 − original C0 | −0.054 | [−0.094, −0.013] |
| Reproducibility C3 − original C0 | −0.092 | [−0.132, −0.052] |
| Targeted evidence C5 − original C0 | **−0.233** | **[−0.281, −0.187]** |

C5 also scored 0.162 points below the length-matched neutral appendix. A separate M3 execution on the same cohort produced a C5−C0 effect of −0.216. Qwen3 and Mistral showed negative effects of −0.857 and −0.133, respectively.

These appendices did not raise the evaluators’ average scores. The result does not identify the cause of the decline or establish that scientific quality deteriorated.



![C5 minus C0 across four scoring panels]({{ '/assets/evidencepatch-feedback/score_effects.svg' | relative_url }})

*Figure 2. Separate estimates on the same 300-paper cohort. M3 uses three ratings per condition; Qwen3 and Mistral use one. The M3 rerun does not add independent papers.*

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

## Evaluating a revision loop

Each iteration should ask whether the original concern was valid, whether the response has sufficient evidence, whether the specific gap was resolved, whether the revision introduced problems, and whether the overall judgment changed reliably.

Concern IDs, version hashes, and evidence records make these questions traceable. Fixed-concern reassessment should accompany fresh review. A concern disappearing from the next review does not establish that it was resolved; different wording does not automatically identify a new concern.

Stopping should reflect evidence and budget. The system should stop when no supported action remains, when required experiments cannot currently be executed, or when the budget is exhausted, while preserving unresolved issues. Repeatedly sampling until a score reaches four risks mistaking evaluator variation for progress.

EvidencePatch’s clearest current finding is that this feedback loop needs separate measurements of **local responses, overall scores, and review stability**. We have implemented the evidence-constrained workflow and observed a disconnect among these outcomes. Independent expert adjudication of evidence support and substantive resolution remains the next critical step.

[See the completed experiment tables and figures]({{ '/en/research/2026/11/18/completed-experiment-results/' | relative_url }}).
