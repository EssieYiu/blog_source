# Hexo使用小记

（官方文档是最好的参考）

## 常用操作

hexo new [layout] <title> 创建一篇新的文章

layout默认值有post/page/draft

hexo generate生成静态文件

hexo server 启动服务器

### 布署

hexo clean

hexo deploy

## 其他

### 文章摘要

```yaml
This is extract
<!-- more -->
This is main content
```

### 不能显示markdown中的图片的问题

在markdown中插入图片要能在网站上正常显示：

首先在_config.yml中设置post-asset-enable为true，s这样，新建文章的时候会同时建立一个同名文件夹，将图片放进文件夹中，并且使用标签插件对图片进行引用

{% asset_img example.jpg [title] %}

官方文档中对这一点也有进行说明

### 不能显示数学公式的问题

搜了网上找到了解决方案

首先修改渲染引擎

```shell
npm uninstall hexo-renderer-marked --save
npm install hexo-renderer-kramed --save
```

接下来对第11行的escape和第20行的em值进行修改

```javascript
//escape: /^\\([\\`*{}\[\]()#$+\-.!_>])/,
  escape: /^\\([`*\[\]()#$+\-.!_>])/,
      
//em: /^\b_((?:__|[\s\S])+?)_\b|^\*((?:\*\*|[\s\S])+?)\*(?!\*)/,
  em: /^\*((?:\*\*|[\s\S])+?)\*(?!\*)/,
```

在所使用的主题中开启mathjax，enable的false改成true

```yaml
mathjax:
  enable: true
  per_page: false
  cdn: //cdn.bootcss.com/mathjax/2.7.1/latest.js?config=TeX-AMS-MML_HTMLorMML
```

在文章的Front Matter中加上一条mathjax

```yaml
---
title:
tag:
date:
mathjax: true
```

 即可

