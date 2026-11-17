# FXJ-BLOG

EvidencePatch 项目的研究博客，使用 Jekyll + GitHub Pages 发布，评论由 giscus / GitHub Discussions 提供。

## 内容维护

- 新文章放进 `_posts/`，文件名格式：`YYYY-MM-DD-title.md`。
- 每篇文章使用 Jekyll front matter；设置 `comments: true` 可显示 giscus 评论。
- 修改并推送到 `main` 后，GitHub Actions 会自动构建和部署。

## GitHub Pages 设置

仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。

## 评论设置

已启用 GitHub Discussions，文章按 URL pathname 映射到 `Announcements` 分类。评论者需通过 GitHub 授权 giscus。请确认 giscus app 已安装到此仓库。
