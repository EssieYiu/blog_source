'use strict';

// Register a current Markdown engine directly: the older Hexo wrapper depends
// on removed markdown-it internals. Math is rendered to SVG during generation.
const MarkdownIt = require('markdown-it');
const mathjax = require('markdown-it-mathjax3');
const anchor = require('markdown-it-anchor');
const { highlight } = require('hexo-util');
const md = new MarkdownIt({ html: true, linkify: false, typographer: false });
md.use(mathjax).use(anchor);
md.renderer.rules.fence = (tokens, index) => {
  const token = tokens[index];
  return highlight(token.content, {
    lang: token.info.trim().split(/\s+/)[0],
    gutter: true,
    wrap: true,
    stripIndent: false
  });
};
hexo.extend.renderer.register('md', 'html', data => md.render(data.text), true);
hexo.extend.renderer.register('markdown', 'html', data => md.render(data.text), true);
