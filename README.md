# Essie 博客维护说明

这是从 `../EssieYiu.github.io` 的已发布网页恢复的 Hexo 源工程。旧目录保持原样。源码仓库为 `git@github.com:EssieYiu/blog_source.git`；新工程尚未部署到线上博客。

## 第一次使用

安装 Node.js 24 LTS（自带 npm），然后在此目录执行：

```bash
npm ci
npm run server
```

打开 http://localhost:4000 。如果使用 nvm，可先运行 `nvm install` 和 `nvm use`，版本由 `.nvmrc` 指定。当前环境已安装 Node 24，可直接运行上述命令；换电脑后需重新安装。

## 写文章

```bash
npm run new -- "文章标题"
npm run server
```

编辑 `source/_posts/` 下的新 Markdown 文件。文章开头的 `title` 是标题，`date` 是发布时间，`tags` 和 `categories` 是标签、分类。`<!-- more -->` 之前的内容显示在首页摘要中。

新建文章会生成同名图片目录，可以把图片放进去并写 `{% asset_img example.png 图片说明 %}`。普通 Markdown 图片也可以使用站内绝对路径，例如 `![说明](/images/example.png)`。

公式使用 `$...$` 或单独成行的 `$$...$$`，构建时由 MathJax 生成 SVG，无需访客另外加载公式脚本。Markdown 渲染入口在 `scripts/markdown.js`，使用当前版本的 markdown-it，避免旧渲染包装插件的依赖兼容问题。

恢复文章设置了 `disableNunjucks: true`，因此其中用普通 Markdown 图片引用，不使用 Hexo 模板标签。恢复文章的 `permalink` 保留原网址，修改标题时不要随意改变该字段。

## 修改外观

- `_config.yml`：标题、作者、网址、文章生成规则。
- `_config.next.yml`：NexT Gemini 主题、导航、头像。
- `source/about/index.md`：关于页。
- `source/images/`：图片。

当前使用 Hexo 8 和 NexT 8，沿用 Gemini 布局；不是原 NexT 5 主题的逐像素复原。旧 Gitalk 未启用，也没有迁入旧 OAuth 密钥。

## 生成与检查

```bash
npm run clean
npm run build
python -m pip install -r tools/requirements.txt
npm run check
```

静态站点输出在 `public/`。检查脚本比对原站的 8 篇文章路径、标题、代码块、公式渲染和图片引用，结果写入 `recovery/validation.json`。脚本需要旁边保留旧仓库；日常写作和构建只需要 Node，无需 Python。

`tools/recover.py` 仅用于首次恢复，若已有 `source/_posts` 会拒绝覆盖。不要在日常维护时重新运行迁移或删除恢复后的文章。

## 恢复记录

- `recovery/manifest.json`：已发布文章与源文件、旧网址的对应关系。
- `recovery/original-markdown/`：旧仓库中所有 Markdown 和草稿的副本，放在生成目录之外，不会自动发布。
- 已修复旧图片路径中的 Jekyll 模板残留、重复目录和 6 处 `.jp` 后缀；将公式中的字面量 `#` 转义。
- Markdown 从已发布 HTML 提取，保留正文、代码及已渲染页面中的 TeX；原稿中已丢失的信息无法凭空还原。旧网页本身若已有排版或公式内容错误，仍需逐篇复核。

## 发布到原 GitHub Pages

当前没有配置部署目标，`npm run deploy` 不会发布到远端。先在 GitHub 仓库 Settings → Pages 确认实际发布方式。

若继续使用 Git 分支发布：在独立的源码仓库或源码分支中保存本工程，确认预览后再将 `_config.yml` 的 `deploy: {}` 替换为：

```yaml
deploy:
  type: git
  repo: git@github.com:EssieYiu/EssieYiu.github.io.git
  branch: master  # 仅在 Pages 确认发布分支就是 master 时使用
```

配置好 GitHub SSH 认证后执行 `npm run deploy`。部署会用本工程生成的站点替换目标分支内容，因此必须先把旧站和源码分别备份好，再发布。不要直接把源码推到当前存放成品的 master 分支。

也可以改用 GitHub Actions 自动构建，但需要先确定源码要保存在哪个仓库、Pages 使用何种发布方式。

## 保存源码

本工程已使用 Git 管理并连接到 `git@github.com:EssieYiu/blog_source.git`。维护后用 `git add`、`git commit`、`git push` 保存变更。需要备份整个本目录（含 `package-lock.json`、配置、`source/`、`scaffolds/`、`scripts/`、`tools/`、`recovery/`、本说明）纳入 Git 并推送备份。`.gitignore` 已排除依赖目录、构建结果和缓存。以后换电脑只需克隆源码、安装 Node 24、执行 `npm ci`。

参考：[Hexo 文档](https://hexo.io/zh-cn/docs/)、[NexT 文档](https://theme-next.js.org/docs/getting-started/)。
