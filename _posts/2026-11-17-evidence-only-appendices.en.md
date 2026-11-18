---
layout: post
title: "We Added Evidence to 300 Papers. AI Review Scores Went Down."
date: 2026-11-17 10:00:00 +0000
categories: research
permalink: /en/research/2026/11/17/evidence-only-appendices/
lang: en
author: "Fengxian Ji, Fan Zhang, Zhuohan Xie"
translation_url: /research/2026/11/17/evidence-only-appendices/
comments: true
---

*An EvidencePatch research update on evidence-only appendices and AI reviewer scores.*

We started with a practical question: reviewers sometimes miss evidence that is already in a paper. If we organize the relevant passages into a short, clear appendix, will an AI reviewer notice them more easily and give the paper a higher score?

Our current 300-paper study says no. In the primary MiniMax-M3 evaluation, a targeted evidence appendix lowered the mean score proxy by **0.233 points on a 1–5 scale** compared with the unchanged paper (95% paper-bootstrap confidence interval: **−0.281 to −0.187**; paired signed-rank *p* = **2.34 × 10⁻¹⁷**). A separate M3 execution on the same papers also moved in the negative direction (**−0.216**). Two other reviewer models showed negative average changes as well, with different magnitudes: **−0.133** for Mistral and **−0.857** for Qwen3.

This was not the result we hoped for, but it is informative: making existing evidence easier to find did not reliably raise these models’ scores.

## What we did

We used 300 papers with human reviews from ICLR and NeurIPS records. For each paper, we kept the main text fixed and compared several material conditions: the original paper, length and content controls, and a targeted appendix that linked reviewer concerns to passages already in the paper. The primary MiniMax-M3 panel scored five conditions three times each. We also ran a separate M3 evaluation on the same cohort and evaluated it with Qwen3 and Mistral.

The intervention was deliberately narrow. It could reorganize or point to existing evidence; it could not add results from a new experiment or change the paper’s scientific claims. We checked source hashes and the provenance of quoted text. These checks confirm that the quotations came from the frozen paper. They do not establish that a quotation logically supports a claim or that it resolves a reviewer’s concern.

## A score is not a resolution label

AI scores can change for several reasons: evidence may be easier to find, a model may prefer a particular presentation, or the supplement may fail to address the reviewer’s concern. A score increase alone cannot distinguish among these possibilities.

We therefore treat scores as measurements of model judgments, not as evidence that scientific quality changed. The cross-model results make the same point: all three model families moved downward on average, but Qwen3’s change was much larger than Mistral’s. The result depends in part on the evaluator. A higher score from one evaluator does not by itself show that a scientific concern was resolved.

In a separate 100-paper development cohort, we also repeated a blind M3 scoring pass over frozen outputs from the risk-aware method. The repeat produced a mean change of **+0.11** (95% confidence interval: **−0.01 to +0.22**, *p* = **0.090**), compared with **+0.14** in the earlier pass. Paper-level score changes were only weakly correlated across the two passes (**ρ = 0.157**). This was a rescore of already generated outputs, not a new run of method generation. It is a reminder to interpret small apparent gains cautiously.

## What we can and cannot conclude

We can conclude that the evidence-only appendix tested in this cohort did not increase mean AI reviewer scores. A second M3 execution also showed a negative change, as did the two other reviewer models.

We cannot conclude that appendices are useless, that adding a genuinely needed experiment would not help, or that human reviewers would respond in the same way. Most importantly, we do not yet have returned expert labels to determine whether the supplements resolved valid concerns. The blinded expert annotation package is prepared, but annotations have not been returned. Paper-level reuse rights are also still under review, so this post reports aggregate results only.

## Completed results, tables, and figures

Authors: Fengxian Ji, Fan Zhang, Zhuohan Xie. [See the bilingual experiment-results summary]({{ '/en/research/2026/11/18/completed-experiment-results/' | relative_url }}).
