# PHP Note

## 超全局变量

$GLOBALS：引用全局作用域中可用的全部变量

$_SERVER：服务器和执行环境信息 

e.g.$_SERVER['PHP_SELF']

'PHP_SELF'：当前执行脚本的文件名。

REQUEST_URI:URI用来指定要访问的页面，如/index.html

$_GET：通过URL参数传递给当前脚本的变量的数组

e.g.something($_GET["name"])

url?name=xxx，则something(xxx)

$_POST：当http post请求的Content-type是*pplication/x-www-form-urlencoded* 或 *multipart/form-data* 时，会将变量以关联数组形式传入当前脚本

$_FILES：通过http post方式上传到当前脚本的项目的数组

$_COOKIE：通过 HTTP Cookies 方式传递给当前脚本的变量的数组

$_SESSION:当前脚本可用 SESSION 变量的数组

$_ REQUEST:默认情况下包含了$_ GET,$_ POST,$_COOKIE的数组

$_ENV:通过环境方式传递给当前脚本的变量的数组。

## 处理表单

```html
<form action="action.php" method="post">
    <p>name:<input type = "text" name="name"/></p>
    <p>age:<input type="text" name="age"/></p>
    <p><input type="submit"/></p>
</form>
```

打印来自表单的数据

```php
hello,<?php echo htmlspecialchars($_POST['name']);?>
You are <?php echo (int)$_POST['age'];?> years old.
```

## 基本语法

#### 标记

<?php...?>

<? ...?>

#### 注释

//注释注释     #注释注释    / * 注释 */

### 变量类型

#### 数组

array(key=>value

, ...

)；

key可以是一个integer或者string

value可以是任意类型的值

key会有强制转换，如包含有合法整型值的字符串会被转化为整型，浮点数转化为整型，布尔值转化为整型，NULL会被转化为空字符串。key会有强制覆盖，同一个键名，后面会覆盖前面

#### 对象

```php
<?php
 class foo{
    function do_foo(){
        echo "Doing foo.";
    }
}
$bar = new foo;
$bar->do_foo();
?>
```

array转换成object将使键名成为属性名并具有相对应的值

### 函数

isset检查是否设置了某个变量

var_dump 用于输出变量的相关信息

strstr(str1,str2)判断str2是否str1的字串，并返回从str2第一次出现的位置开始到str1结尾的子串

substr(string1, startPos,[length])子串，字符位置从0开始计数，startPos开始取子串的索引值

str_replace(search, replace, subject, [count])将subject中全部的search都被replace替换掉，并返回结果

parse_str(encoded_string, [result])将字符串解析成多个变量并设置到当前作用域

eregi(pattern, string,[regs])存在空字符截断漏洞，正则匹配

extract从数组中将变量导入当前的符号表

## 文件操作相关函数

### file_get_contents



### 魔术常量

__ LINE __文件中的当前行号

__ FILE __ 文件的完整路径和文件名

__ DIR __ 文件所在的目录

__ FUNCTION __ 函数名称

__ CLASS __ 类的名称

__ TRAIT __ trait的名字

__ METHOD __ 类的方法名

__ NAMESPACE __ 当前命名空间的名称

### 类与对象

#### 魔术方法

__ construct(), __ destrcuct(), __ call(), __ callStatic, __ get(), __ set(), 

__ isset(), __ unset, __ sleep(), __ wakeup(), __ toString(), __ invoke(), 

__ set_state(), __ clone(), __ debuginfo()

##### __ sleep() 和 __ wakeup()

serialize()函数会检查类中是否存在一个魔术方法__sleep()。如果存在，该方法会先被调用，然后再执行序列化操作。

#### 序列化

序列化一个对象将会保存对象的所有变量，但是不会保存对象的方法，只会保存类的名字。

serialize()：序列化

unserialize()：反序列化

## 伪协议

### file://

在双off条件下也可以使用

allow_url_fopen:off/on

allow_url_include:off/on

用于访问本地文件系统

### php://

php://filter双off也可以使用

php://input, php://stdin, php://memory, php://temp需开启allow_url_include

#### php://filter

它是一种元封装器，设计用于数据流打开时的筛选过滤应用。

```
resource=<要过滤的数据流> 参数是必须的。指定了要筛选过滤的数据流
read=<读链的筛选列表> 参数可选，可以设定一个或多个过滤器名称，以管道符|分割
write=<写链的筛选列表> 同上
<;两个链的筛选列表> 任何没有以read=或write=作前缀的筛选器列表会视情况应用于读或写链
```

例子，任意读取文件的payload

```php
php://filter/read=convert.base64-encode/resource=upload.php
```

字符串过滤器

```php
string.rot13
string.toupper
string.tolower
string.strip_tags
```

例如

```php
<?php
$filename = $_GET['a'];
$data = "test test";
file_put_content($filename,$data);
?>
```

可以往服务器中写入一个文件内容全为小写且文件名为test.php的文件

```
?a=php://filter/write=string.tolower/resource=test.php
```

#### php://input

是个可以访问请求的原始数据的只读流，可以读取到 post没有解析的原始数据，将post请求中的post数据作为php代码执行。enctype="multipart/form-data"的时候php://input是无效的