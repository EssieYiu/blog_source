# python requests 笔记

## 发送请求

```python
>>> r = request.get('http://domaim.com:port/something')
>>> r = requests.post('http://domain.com:port/something, data={'key1':'value1','key2':'value2'}')
```

其他的http请求如put,delete,head,options同理

## 使用params关键字传递URL参数

传递URL的query string参数，如

http://domaim.com/somthing?username='abc'&password='cde'

```python
>>> payload = {'username':'abc','password':'cde'}
>>> r = requests.get('http://domain.com/somthin',params = payload)
```

还可以将列表作为值传入

## 响应内容

```python
import requests
r = requests.get('http://domain.com/somthing')
print(r.text)
```

r.encoding属性是requests用来解码服务器的文本编码格式，可以修改

## 二进制响应内容

可以以字节的方式访问请求响应体，对于非文本请求

```python
>>> r.content
```

requests会自动为你解码gzip和deflate传输编码的响应数据

例如，以请求返回的二进制数据创建一张图片，可以使用以下代码

```python
from PIL import image
from io import BytesIO
i = image.open(BytesIO(r.content))
```

## JSON响应内容

```
>>> r.json()
```

使用`r.raise_for_status()`或者`r.status_code`检查请求是否成功

## 原始套接字响应内容

```python
>>> r.raw
>>> r.raw.read(10)
```

但一般情况下，应当以下面的模式将文本流保存到文件

```python
with open(filename, 'wb') ad fd:
	for chunk in r.iter_content(chunk_size):
		fd,write(chunk)
```

流下载时，上面是优先推荐的获取内容方式，chunk_size根据实际情况可以调整大小

## 定制请求头

```
url = 'http://domain.com/something'
headers = {'user-agent':'something'}
r.requests.get(url, headers=headers)
```

