# FXJ-BLOG

EvidencePatch 最终博客的发布仓库：Jekyll + GitHub Pages，支持中英文切换及 giscus 评论。

## 双语文章

每篇文章在 `_posts/` 中维护一对文件：`.md` 为中文，`.en.md` 为英文；两者的 `translation_url` 应指向对方的 `permalink`。`scripts/manage_blog.py check` 会检查所有双语配对、翻译链接、图片引用和 SVG 语法。旧实验汇总文章及其跳转页已删除。

| 目录/文件 | 用途 |
|---|---|
| `_posts/` | 双语发布正文，含公式和图引用 |
| `assets/evidencepatch-feedback/` | 主图、评分/分歧/重复性图、聚合数据与来源哈希 |
| `assets/results-2026-11-18/` | 正文中仍引用的基线与复评分图，并非旧文章副本 |
| `scripts/build_feedback_figures.py` | Python 标准库 + gnuplot 绘图 |
| `scripts/manage_blog.py` | 检查最终稿、重建图、同步本地镜像 |
| `_layouts/`、`_includes/` | 页面布局、公式渲染入口和评论 |
| `_config.yml` | Jekyll、语言和发布配置 |
| `.github/workflows/pages.yml` | 推送 main 后构建与部署 |

## 维护命令

在仓库目录执行；Python 标准库即可检查/同步，绘图另需 gnuplot：

```bash
make check    # 检查双语稿、公式数量、图片引用与 SVG
make figures  # 用保存的聚合数据重新生成图
make sync     # 同步到工作区 ../EvidencePatch/blog/（须有该目录）
```

只维护 `_posts/`，`EvidencePatch/blog/` 是自动同步的本地镜像。不要在两个位置独立编辑。新实验聚合结果应先在实验目录校验，再更新 `aggregate_data.json`，随后绘图和检查。绘图不读取论文原文或密钥，不启动 API/GPU。

网站发布后地址：

- [中文](https://fengxianji.github.io/FXJ-BLOG/research/2026/11/17/evidence-only-appendices/)
- [English](https://fengxianji.github.io/FXJ-BLOG/en/research/2026/11/17/evidence-only-appendices/)

## 发布与历史材料

提交并推送到 main 会触发 Pages。`scripts/` 和 `Makefile` 保存在仓库供复现，排除在网站构建之外。旧英文汇总 PDF 已移到项目工作区 `docs/history/blog_exports/`，它不是当前最终稿 PDF。

GitHub Pages Source 使用 GitHub Actions。giscus 按 URL pathname 将评论关联到 Discussions / Announcements；最终文章 URL 保持不变。

## 研究资源仓库

方法代码、匿名数值结果、完整表格和复现脚本发布在 [FengxianJi/EvidencePatch](https://github.com/FengxianJi/EvidencePatch)。最终中英文文章的开头和文末均提供入口。
