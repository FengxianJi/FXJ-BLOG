---
layout: default
title: Research Notes
permalink: /en/
lang: en
translation_url: /
---
<section class="home-intro">
  <p class="eyebrow">RESEARCH LOG · EVIDENCEPATCH</p>
  <h1>Clearer research evidence. More reliable evaluation.</h1>
  <p>Research updates on evidence augmentation, budget-aware experiments, and reliable scientific evaluation. We share methods, results, limitations, and evidence-based discussion.</p>
</section>
<h2>Latest posts</h2>
{% assign localized_posts = site.posts | where: "lang", "en" %}
<ul class="post-list">
  {% for post in localized_posts %}<li><span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span><h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2><p>{{ post.excerpt | strip_html | truncate: 220 }}</p></li>{% endfor %}
</ul>
