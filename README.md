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

## 自动发布到原 GitHub Pages

流程为：推送 `blog_source/main` → GitHub Actions 安装锁定依赖 → 构建并校验 → 将 `public/` 推送到 `EssieYiu.github.io/gh-pages` → GitHub Pages 更新博客。只发布生成目录；草稿备份和源码不会复制到发布分支。原 `master` 保留作为旧站备份。

工作流：`.github/workflows/deploy.yml`；发布脚本：`tools/publish.sh`。也可以在 Actions → Build and deploy blog → Run workflow 手动运行。未添加部署密钥时，工作流仅构建、校验并提示跳过发布。

### 首次启用（仅需一次）

1. 为发布创建一对专用 SSH 密钥。此次已在本机生成：公钥 `/root/.ssh/blog_pages_deploy.pub`，私钥 `/root/.ssh/blog_pages_deploy`。私钥未写入任何 Git 仓库。换电脑后也可用 `ssh-keygen -t ed25519 -f blog_pages_deploy -N ""` 重新生成一对，并同步替换以下两处。
2. 在 **EssieYiu.github.io** → Settings → Deploy keys → Add deploy key：标题可填 `blog_source auto deploy`，Key 粘贴**公钥**，勾选 **Allow write access**。
3. 在 **blog_source** → Settings → Secrets and variables → Actions → New repository secret：Name 填 **BLOG_DEPLOY_KEY**，Secret 粘贴**私钥完整内容**（包括 BEGIN/END 行）。不要将私钥作为普通文件提交。
4. 在 **EssieYiu.github.io** → Settings → Pages：Source 选 **Deploy from a branch**，Branch 选 **gh-pages**，目录选 **/(root)**，Save。若还没有 `gh-pages`，先在源码仓库 Actions 手动运行一次工作流，成功后再选。
5. 在源码仓库 Actions 查看工作流，确认发布成功；在博客仓库 Actions 查看 Pages 构建，完成后访问 https://essieyiu.github.io/ 。

此处用部署密钥执行跨仓库推送，不需要把默认 `GITHUB_TOKEN` 权限调大，也不需要把源码仓库开启 Pages。

### 以后更新

```bash
npm run new -- "文章标题"
# 编辑 source/_posts/ 下的文章并预览
npm run server
# 完成后保存并推送；随后自动发布

git add .
git commit -m "新增文章"
git push
```

若 Actions 失败，打开失败步骤的日志。构建或校验失败时不会发布。只有本次恢复固定的 8 篇文章会与旧站对比；新增文章正常参与构建，不要求出现在旧站恢复清单里。

本地 `_config.yml` 仍保留 `deploy: {}`，日常使用自动发布即可，不需要执行 `npm run deploy`。

## 保存源码

本工程已使用 Git 管理并连接到 `git@github.com:EssieYiu/blog_source.git`。维护后用 `git add`、`git commit`、`git push` 保存变更。需要备份整个本目录（含 `package-lock.json`、配置、`source/`、`scaffolds/`、`scripts/`、`tools/`、`recovery/`、本说明）纳入 Git 并推送备份。`.gitignore` 已排除依赖目录、构建结果和缓存。以后换电脑只需克隆源码、安装 Node 24、执行 `npm ci`。

参考：[Hexo 文档](https://hexo.io/zh-cn/docs/)、[NexT 文档](https://theme-next.js.org/docs/getting-started/)。
