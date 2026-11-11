---
title: picoCTF 2018 Web Writeup
date: 2019-09-29
categories: CTF
---



## valut

点进去查看，发现是一个登陆的页面。查看源代码

![]({{site.url}}/../../../../assets/images/20190929/valut2.png)

可以看到query直接使用字符串拼接的方式获取用户输入的username和password，后面也做了校验。不巧的是，这里的两次校验（user_match和password_match）都是校验了username，而password并没有进行校验。这样以来，就可以直接对password进行注入即可。

```sql
password = a' or 1=1;
```

![]({{site.url}}/../../../../assets/images/20190929/valut1.png)

## Aritisinal Handcraft HTTP3

nc上目标地址之后出现如下页面，输入完验证码之后就可以发送手动的HTTP请求

![]({{site.url}}/../../../../assets/images/20190929/http3-0.png)

首先发送一个HTTP GET请求当前/页面看看是什么

![]({{site.url}}/../../../../assets/images/20190929/http3-1.png)

发现有一个login的链接，于是发送一个GET请求到login页面

![]({{site.url}}/../../../../assets/images/20190929/http3-2.png)

看到了输入username和password的地方

按照题目所给的用户名和密码，发送一个POST请求

![]({{site.url}}/../../../../assets/images/20190929/http3-3.png)

再次向/页面发送GET，请求，带上cookie，即可得到flag

![]({{site.url}}/../../../../assets/images/20190929/http3-4.png)

（持续更新中）

