---
layout: default
title: 研究文章
lang: zh-CN
translation_url: /en/
---
<section class="home-intro">
  <p class="eyebrow">RESEARCH LOG · EVIDENCEPATCH</p>
  <h1>让研究证据更清晰，也让评估更可靠。</h1>
  <p>这里记录 EvidencePatch 关于科学论文证据补充、预算约束实验与可靠评估的研究进展。我们公开方法、结果和局限，也欢迎基于证据的讨论。</p>
</section>
<h2>最新文章</h2>
<ul class="post-list">
  {% assign localized_posts = site.posts | where: "lang", "zh-CN" %}
  {% for post in localized_posts %}<li><span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span><h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2><p>{{ post.excerpt | strip_html | truncate: 220 }}</p></li>{% endfor %}
</ul>
