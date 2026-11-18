---
layout: post
title: "What Controls Can Tell Us: Fair Comparisons of Self-Improving Research Agents"
date: 2026-11-18 10:00:00 +0000
last_modified_at: 2026-11-18
categories: research
permalink: /en/research/2026/11/18/controlling-rsi-comparisons/
lang: en
author: "Fengxian Ji"
translation_url: /research/2026/11/18/controlling-rsi-comparisons/
comments: true
math: true
figure_count: 2
---

Recursive self-improvement (RSI) agents repeatedly propose changes, run experiments, and revise their research plans in response to results. When we compare two RSI frameworks, a final score alone rarely answers the central question: **Did one framework improve the research more effectively, or did it happen to receive an easier idea, a more favorable revision direction, or a larger experimental budget?**

Controls give both frameworks the same starting point and constraints, so we can examine their improvement trajectories under matched conditions. They do not prove by themselves that one framework is better. They make the comparison closer to a causal question: what changes when we switch frameworks while holding the other conditions fixed?

**Code and public results:** [SciCTRL-Bench open-source code](https://github.com/FengxianJi/SciCTRL-Bench-Open) · [Download ZIP](https://github.com/FengxianJi/SciCTRL-Bench-Open/archive/refs/heads/main.zip) · [Pilot summary data](https://github.com/FengxianJi/SciCTRL-Bench-Open/blob/main/results/pilot_summary.json)

[![Matched design for comparing RSI frameworks on the same idea, direction, and budget]({{ '/assets/scictrl-rsi/matched-controls.svg' | relative_url }})]({{ '/assets/scictrl-rsi/matched-controls.svg' | relative_url }})

*Figure 1. A paired design gives both frameworks the same idea, data, tools, model, budget, evaluator, and preregistered revision direction, then compares their full trajectories. This is an evaluation schematic, not a completed RSI comparison. Click the image to open the SVG.*

## Why a single score is not enough

Suppose an idea has five possible revision directions. Direction A is easier to test; direction B is riskier but could yield a larger gain. Framework A improves its score by 17% on direction A, while framework B gains 16% on direction B. Those final scores cannot tell us whether the frameworks faced comparable opportunities, or whether the difference came from the framework, task difficulty, or experimental noise.

The problem is even clearer when the frameworks receive different ideas. The difficulty of the idea, available data, and feasible revisions can all differ. Even if framework A scores higher than framework B, the gap cannot be attributed directly to the RSI framework.

Controlling variables does not mean rewriting every idea into the same prompt. It means representing each research task as an inspectable object: the initial idea, factors that may change, conditions that must remain fixed, evaluation metrics, and experimental budget. Each framework then receives the same task instances and operating constraints.

## Which conditions should be fixed?

| Comparison element | Hold constant within paired runs | Record as an outcome or covariate |
|---|---|---|
| Initial task | Same idea, data, initial code, and known evidence | Task source, domain, difficulty tier |
| Revision space | Same preregistered directions and boundaries | Which direction the agent selects; boundary violations |
| Evaluation environment | Same metrics, executor, hidden checks, and success criteria | Invalid experiments, failure causes, evaluator uncertainty |
| Run budget | Same iteration, time, or model-call limits | Actual tokens, cost, wall-clock time |
| Model and tools | Same model snapshot, tool access, and task prompt | Random seed, failed calls, retries |

Each idea, revision direction, and repeated run can form a paired block. Both frameworks run under the same conditions, and we compare within-block differences rather than pooling final scores from unrelated tasks. Multiple directions also let us test a framework-by-direction interaction: an RSI system may be stronger at experimental design but show no advantage in hypothesis revision.

## Evaluate the trajectory, not only the final score

An RSI process is long, and its final score compresses several kinds of failure into one number. An agent may identify a modifiable factor correctly but implement the code incorrectly. Its code may run while the experiment fails to distinguish competing hypotheses. The experiment may be sound while the final explanation attributes the gain to the wrong factor. Recording only the endpoint makes these failures hard to separate.

A paired evaluation should preserve at least three layers of outcomes:

1. **Direction identification:** Did the agent identify the factors it was allowed to change? Did it alter anything that had to remain fixed?
2. **Execution and attribution:** Did the experiment follow the plan, and do the results support the claimed causal explanation?
3. **Outcome and cost:** Did the research metric improve? Was the gain stable across repeated runs? How many calls, how much time, and how much compute did it require?

These metrics are not substitutes for one another. Correctly identifying a direction does not guarantee a valid experiment, and one successful run does not establish a reproducible gain. Reports should separate success rate, out-of-scope revision rate, attribution error, paired effects, and confidence intervals. They should cluster by idea or source project so that similar variants from one project are not counted as independent evidence.

## What results do we have so far?

Our current results mainly check whether task construction and evaluation procedures are trustworthy; they do not establish that one RSI framework wins. The construction audit covers 68 cases, and all eight structural checks passed. These checks cover whether the intervention matches its registration, certificate validation, shortcut rejection, reference repairs, and leakage of private labels into public prompts.

An earlier diagnostic pilot ran 32 tasks across eight programmatic task families. All 32 passed numerical and final-source verification. In a blind test, all 16 original proposals were classified correctly; rewritten proposals achieved 14/16, with 87.5% balanced accuracy and an AUC of 0.883. A CPU control stress test also covered eight families, four implementations, and three hidden instances, for 96 executions.

These numbers come from current project records; task-level traces and evaluator-only labels are not released. They reveal a useful issue: the original-proposal blind test already reached a ceiling, so the task may not distinguish methods well. The lower result after rewriting also shows why semantic preservation needs its own check. But these experiments do not compare two RSI frameworks on matched ideas. They cannot show that controls improve RSI performance. Passing a construction audit means only that structural checks passed; it is not expert validation or evidence of real-world scientific effectiveness.

| Diagnostic | Observed result | What it supports | What it does not support |
|---|---:|---|---|
| VSRO construction audit | 68 cases; 8/8 structural gates passed | The constructor met the listed structural checks | Expert review or real-world scientific validity |
| Eight-domain CPU diagnostic pilot | 32/32 passed numerical and final-source checks; 56 model calls | These programmatic tasks ran and passed the specified artifact checks | A paired comparison of two native RSI frameworks |
| Original-proposal blind test | 16/16 correct; 100% balanced accuracy | Labels were fully separable on this sample | Generalization; a ceiling score may indicate an easy task |
| Rewritten-proposal blind test | 14/16 correct; 87.5% balanced accuracy; AUC 0.883 | A measurable classification signal remained after rewriting | RSI improvement or a causal effect |
| CPU control stress test | 96 executions (8 families × 4 implementations × 3 hidden instances) | Specified controls were checked across several implementations | 96 independent research projects or expert validation |
| DiscoveryBench development audit | 153 tasks; 6/6 data-integrity checks passed | The downloaded development split passed the listed data checks | Framework effects; tasks are not strict matched causal pairs |

[![Task checks, blind tests, and CPU stress-test counts from the SciCTRL diagnostic pilot]({{ '/assets/scictrl-rsi/pilot-diagnostics.svg' | relative_url }})]({{ '/assets/scictrl-rsi/pilot-diagnostics.svg' | relative_url }})

*Figure 2. Numerical/source checks, proposal blind-test accuracy, and the separate 96-execution CPU control stress test. Values come from the [public aggregate JSON](https://github.com/FengxianJi/SciCTRL-Bench-Open/blob/main/results/pilot_summary.json). These are diagnostic-pilot results, not an RSI framework ranking. Click the image to open the SVG.*

The DiscoveryBench development-set audit covers 153 tasks, with all six data-integrity checks passing. However, its task files are not strictly matched causal pairs. The split is useful for calibrating ingestion and task coverage, but it should not by itself estimate a causal difference between RSI frameworks. A complete paired run of two native RSI frameworks on the same ideas, revision directions, and budgets is still missing.

## Next: from “looks higher” to interpretable comparisons

The next stage should freeze task versions, control directions, and evaluators before each framework runs within matched blocks. Random factors that cannot be fixed should be recorded and repeated. To determine which revision direction works better, we should treat direction as an experimental factor and estimate its effect, rather than mixing outcomes from different directions into a single framework score.

This separates two questions: **Which RSI framework is more reliable on the same idea and revision direction?** And **which revision directions actually help, and under what task conditions?** The first compares agent frameworks; the second studies the boundaries and improvement opportunities of ideas. Controls let us test these questions separately and locate failures across identification, execution, attribution, and outcome.

The current evidence supports a methodological conclusion: without matched tasks and process-level records, final scores are insufficient for comparing RSI frameworks. Claims about which framework is better must wait for the paired experiment.
