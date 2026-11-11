---
title: "数据库复习总结"
date: "2019-12-30T23:34:12+08:00"
permalink: "2019/12/30/databaseReview/"
mathjax: true
disableNunjucks: true
categories: ["note"]
---

（未完）



<!-- more -->



## 1 引言

**数据字典**是指对数据的数据项、数据结构、数据流、数据存储、处理逻辑等进行定义和描述，其目的是对数据流程图中的各个元素做出详细的说明，使用数据字典为简单的建模项目。简而言之，数据字典是描述数据的信息集合，是对系统中使用的所有数据元素的定义的集合

**DBMS**：数据库管理系统，有一个互相关联的数据的集合和一组用以访问这些数据的程序组成。这个数据集合通常称作数据库。

**SQL**：结构化查询语言，structured query language

**DML**：数据操纵语言

**DDL**：数据定义语言

**物理数据独立性**：应用程序如果不依赖于物理模式，它们就被称为是具有物理数据独立性，因此即使物理模式改变了它们也无需重写

## 2 关系模型介绍

### 关系数据库的结构

关系数据库由**表**的集合构成，每个表有唯一的名字

**关系**用来指代表，**元组**用来指代行，**属性**指代表中的列

**关系实例**：包含的一组特定的行

属性的**域**：对于关系的每个属性，都存在一个允许取值的集合

我们要求对所有关系r而言，r的所有属性的域都是原子的

### 数据库模式

**数据库模式**：数据库的逻辑设计

**数据库实例**：给定时刻数据库中数据的一个快照

**关系模式**：对应于程序设计中的“类型定义”，由属性序列及各属性对应域组成

### 码

**超码**是一个或多个属性的集合，这些属性的组合可以使我们在一个关系中唯一地标识一个元组

如果K是一个超码，那么K的任意超集也是超码

**候选码**：是超码，它的任意真子集都不能成为超码，它就是最小超码

**主码**：被数据库设计者选中的、主要用来在一个关系中区分不同元组的候选码

**外码**：一个关系模式r1在它的属性中包括另一个关系模式r2的主码，那么这个属性在r1上称作参照r2的外码。关系r1也称为外码依赖的参照关系，r2叫做外码的被参照关系。

## 3 初级SQL

### 数据定义

#### 基本类型

char, varchar, int, numeric, real, double, float,

#### 基本模式定义

创建department关系模式



```sql
create table department
	(dept_name varchar(20) not null,
	building varchar(15),
	budget numeric(12,2), //定点数，12位数字，2位在小数点右边
	primary key (dept_name)); //完整性约束
```



#### 完整性约束

**primary key**(a,b,c):属性a,b,c构成关系的主码

**Foreign key**(a,b,c) **references** s:关系中任意元组在属性(a,b,c)上的取值必须对应于关系s中某元组在主码属性上的取值

**Not null**：表明在该属性上不允许空值

SQL禁止破坏完整性约束的任何数据库更新

### 数据库的修改



```sql
//插入
insert into instructor
    values(10211,'Smith','Biology',66000);
insert into instructor
    select ID, name, dept_name, 18000
    from student
    where dept_name = 'Music' and tot_cred>144;
    //在查询结果的基础上插入元组
//删除
delete from student ;
drop table r; //整个关系模式都删掉
delete from r; //删掉关系中的所有元组
delete from r where P; //删除满足条件P的r中的元组
//在已有关系中中增加或去掉属性,新属性上的取值为null
alter table r add A D;
alter table r drop A;
//更新
update instructor
set salary = salary*1.05
where salary < (select avg(salary) from instructor);
```



- 只能删除整个元组，而不能只删除某些属性上的值
- delete命令只能作用于一个关系
- 在执行插入前先执行完select语句是非常重要的，例如在student上没有主码约束的话，下面的请求会插入无数元组

  

```sql
insert into student 
	selcet * from student
```



case结构



```text
case
	when pred1, then result1
	when pred2, then result2
	…
	else result0
end
```




```sql
update instructor
set salary = case 
			when salary <= 10000 then salary*1.05
			when salary <= 20000 then salary*1.04
			else salary*1.03
			end
```



### SQL查询



```sql
select xx,xx from table1,table2 where predicate
```



select \* 表示选择所有属性

#### 单关系查询



```
select distinct dept_name from instructor;
//distinct强行删除重复
select all dept_name from instructor;
//all指明不去重
select ID, salary*1.1 from instructor;
//可以使用+-*/运算表达式
select name from instructor where dept_name='Comp.Sci' and salary > 70000;
//where子句中允许使用and or not，也可以有>< <= >= <>等
```



#### 多关系查询



```text
select name, instructor.dept_name, building from instructor, department where instructoe.dept_name=department.dept_name
```



出现在多个表格中的属性名，如这里的dept_name，关系名用作前缀来区分

#### 自然连接 natural join

自然连接运算作用于两个关系，并产生一个关系作为结果，它只考虑那些在两个关系模式中都出现的属性上取值相同的元组对



```text
select name, course_id from instructor natural join teaches
```



#### join…using

指定需要取值相同的列，进行连接



```text
select name, title from (instructor natural join teaches) join course using (course_id)
```



### 附加的基本运算

#### 更名运算 as



```sql
select T.name, S.course_id
from instructor as T, teaches as S
where T.ID = S.ID;
```



#### 字符串运算

字符串相等运算大小写敏感

##### 通配符

- 百分号`%`：匹配任意子串
- 下划线`_`：匹配任意一个字符

使用`like`：匹配模式，反斜杠`\`转义



```sql
like '%Comp%' //匹配任何包含Comp子串的字符串
like '___' //匹配只包含三个字符的字符串
like 'ab\%cd%' //匹配以ab%cd开头的字符串
```




```sql
select dept_name from department where building like '%Watsons%'
```



#### 排序元组的显示次序 order by

asc表示升序（默认），desc表示降序



```sql
select * from instructor order by salary desc, name asc
```



#### where子句谓词

**between, not between**



```sql
select name
from instructor 
where salary between 9000 and 10000
```



**(a,b,c,…)表示n维元组**



```sql
select name, course_id
from instructor, teaches
where (instructor.ID, dept_name) = (teaches.ID,'Biology');
```



### 集合运算

`union`，`intersect`, `except`对应集合论中$\bigcup, \bigcap, -$的操作

使用这三个操作默认去重，保留重复要使用`all`

### 空值 Null values

用**is null**判断空值

涉及空值的任何比较运算的结果视为unknown

unknown or true = true

unknown and flase = flase

unknown and/or 的其它情况和not unknown均为unknown

### 聚集函数

- avg 平均
- min 最小
- max 最大
- sum 总和
- count 计数

注意sum和avg的输入必须是数字集，其它的可以不是

#### 基本聚集



```sql
select avg(salary) as avg_salary from instructor where dept_name = 'Comp.Sci'
```



默认有all，保留重复元素（如计算平均值时很重要）

若要去掉重复元素，使用distinct



```sql
select count(distinct ID)
from teaches
where semester = 'Spring' and year = 2010;
```



SQL不允许在用count(\*)的时候使用distinct



```sql
select count(*)
from course;
```



#### group by分组聚集

**Select 后面跟的选择属性集合需要是group by后面跟的属性集合的子集，否则属性需要出现在聚集函数内部**



```sql
select dept_name,avg(salary) as avg_salary
from instructor
group by dept_name; //找出每个系的平均工资
```



#### Having子句

分组限定条件，having子句中的谓词在**形成分组之后才起作用**，针对group by子句构成的分组



```sql
select dept_name, avg(salary) as avg_salary
from instructor
group by dept_name
having avg(salary) > 42000;
```



与select子句情况类似，任何出现在having子句中，但**没有被聚集的属性必须出现在group by子句中**，否则查询就是错误的

#### 对空值和布尔值的聚集

**除了count(\*)以外，聚合函数忽略输入集合中的空值**

由于空值被忽略，有可能造册灰姑娘参加函数运算的输入值集合为空集。**规定空集的count运算值为0**，其他聚合运算在输入为空集的情况下**返回一个空值**

布尔值有两个聚合函数：Some,every——可以用来处理布尔值的集合

### 嵌套子查询

select-from-where表达式嵌套在另一个查询的where子句中

#### 集合成员资格 in/not in

in/not in 测试元组是否集合中的成员



```text
select distinct course_id 
from section 
where semester='Fall' and year = 2009 and course_id in 
	(select course_id 
     from section 
     where semester = 'Spring' and year = 2010)
```



#### 集合的比较

| comparison | > | < | >= | <= | <> |
| --- | --- | --- | --- | --- | --- |
| some | 略 |  |  |  |  |
| all |  |  |  |  |

in等价于`=some`

not in等价于 `<>all`



```sql
select name 
from instructor
where salary > some (select salary
                     from instructor
                     where dept_name = 'Biology');
```



#### 空关系测试 exist/not exist

exist结构在作为参数的子查询非空的时候返回true

**Exist** r 等价于r不为空值

**Not exist** r 等价于r为空值



```sql
//找到所有参加了生物系的所有课程的学生
select distinct S.ID, S.name
from student as S
where not exists 
	((select course_id 
	 from course
	 where dept_name = 'Biology')
	 except
	 (select T.course_id 
	 from takes as T
	 where S.ID = T.ID));
```



注意$X \subseteq Y \iff X-Y=\varnothing$

来自外层查询的一个相关名称（S）可以用在where子句的子查询中。使用了来自外层查询相关名称的子查询被称作**相关子查询**

#### 重复元组存在性测试 unique

如果作为参数的子查询结果中没有重复的元组，unique结构将返回true值



```sql
//找出所有在2009年最多开设一次的课程
select T.course_id
from courses as T
where unique(select R.course_id
             from section as R 
             where T.course_id = R.course_id and
                R.year = 2009);
```



#### from子句中的子查询

可以使用as子句给此**子查询的结果关系起名字**，并对属性进行重命名



```sql
select dept_name, avg_salary
from (select dept_name, avg(salary) as avg_salary
        from instructor
        group by dept_name)
        as dept_avg(dept_name,avg_salary)
where avg_salary > 42000;
```



子查询的结果关系被命名为dept_avg，属性名是dept_name 和 avg_salary

#### with子句

提供定义临时关系的方法，这个定义只对包含with子句的查询有效



```sql
with max_budget(value) as 
    (select max(budget)
     from department)
select budget
from department, max_budget
where department.budget = max_budget.value;
```



#### 标量子查询

子查询只返回包含**单个属性的单个元组**

sql允许标量子查询出现在返回单个值的表达能够出现的任何地方



```sql
//查询每个系的导师数量
select dept_name,
    (select count(*)
     from instructor
     where department.dept_name = instructor.dept_name)
     as num_instructors
from department;
```



## 4 中级SQL

### 连接表达式

#### 连接条件 on

与自然连接的区别：自然连接相同的字段出现一次，而这里出现两次；若想只显示一次，则需要select指定字段

on条件可以表示任何SQL谓词，可以表示比自然连接更丰富的连接条件



```sql
select * from student join takes on student.ID = takes.ID
```



#### 外连接

外连接在结果中**创建包含空值元组**的方式，保留了在连接中丢失的元组

**左外连接**left outer join，只保留出现在左外连接运算之前（左边）的关系的元组

**右外连接**right outer join，只保留出现在右外连接运算之前（右边）的关系的元组

**全外连接**full outer join，保留出现在两个关系中的元组

前面不保留未匹配元组的连接运算被称作**内连接**运算，不加outer默认使用内连接（也可以加关键词**inner**）



```text
//找出一门课也没有选的学生
select ID from student natural left outer join takes
where course_id is null
```



在左外连接中，左侧关系中不匹配右侧关系任何元组的元组被添上空值并加到结果中。上面的左外连接使得结果中没有选课的学生的元组也得以保留，相对应的属于takes字段的部分为null。

on子句可以和外连接一起使用。on和where在外连接中的表现是不同的。on条件是外连接声明的一部分，但where子句却不是。



```sql
select * from student left outer join takes on student.ID = takes.ID;
select * from student left outer join takes on true
where student.ID = takes.ID
```



上述第一个表达中，没有选课的学生会在结果中，左外连接保留了左边的所有元组。第二个表达中，on true的条件实际产生了一个两个关系的笛卡尔积，where筛选的时候，由于没有选课的学生ID不会出现在takes中，没有选课的学生就被过滤掉了。

### 视图

#### 视图定义

通过查询来定义“虚关系”，并不预先计算并存储，而是使用的时候才通过执行查询被计算出来。

任何像这种不是逻辑模型的一部分，但作为虚关系对用户可见的关系称为**视图**。

作用：掩盖敏感数据、给出灵活数据收集方式

视图并不是一个物理的表格，不会存储到硬盘上

**视图定义**



```sql
create view v as <query expression>
```



例如



```sql
create view faculty as select ID, name, dept_name from instructor
```



一旦定义了视图，我们就可以用视图名指代该视图生成的虚关系。视图也可以调用视图。

直接依赖，v2直接被v1引用

非直接依赖，有一个依赖的路径

递归依赖，自己依赖了自己，需要进行视图展开，从最底层开始代进去

**物化视图**：如果用于定义视图的实际关系改变，视图也跟着修改。这样的视图称物化视图。

物化视图需要维护。

#### 视图更新

一般不允许对视图关系进行修改。

可更新的SQL视图要满足：

- from子句中只有一个数据库关系
- select子句中只包含关系的属性名，不包含任何表达式、聚集或distinct声明
- 任何没有出现在select子句中的属性可以取空值，没有not null约束，也不构成主码的一部分
- 查询中不含有group by或having子句

满足这些限制，视图允许执行update，insert，delete操作

可以在视图定义的末尾包含`with check option`的子句方式来定义视图。如果向视图中插入不满足视图的where子句条件的元组，数据库系统将拒绝该操作

### 事务

**事务**由查询和（或）更新语句的序列组成。

当一条sql语句被执行，就隐式地开始了一个事务，commit/rollback work会结束一个事务。

### 完整性约束

完整性约束保证授权用户对数据库所做的修改不会破坏数据库的一致性。

#### not null约束

属性值不能为空值

#### unique约束



```sql
unique(A1,A2,A3,...An)
```



unique声明支出属性A1,A2,A3,…,An形成了一个候选码，即在关系中没有两个元组能在所有列出的属性上取值相同。注意候选码值可以为null，除非被声明为not null。而null不等于任何值。

#### check子句

`check(P)`，关系中的每个元组必须满足谓词P



```sql
create table section
	(course_id varchar(8),
	...,
	semester varchar(6),
	primary key(course_id,sec_id, semester,year),
	check(semester in('Fall','Winter','Spring','Summer')));
```



#### 参照完整性

我们常常希望保证在一个关系中给定属性集上的取值也在另一关系的特定属性集的取值中出现。这种情况称为**参照完整性**。

参照完整性约束/子集依赖：r2中$\alpha$上的取值集合必须是r1中K1上的取值集合的子集。参照完整性约束不要求K1是r1的主码，故r1中可能多个元组在属性K1上取值相同。（而外码约束要求K1是r1的主码）

违反参照完整性约束时：

- 拒绝执行导致完整性破化的操作
- on delete cascade，“级联”删除

#### 事务中对完整性约束的违反

有一些事务执行过程中会违反完整性约束，但执行完后就不违反了。如插入两个元组，互为配偶，无论先插入哪个，在配偶属性上都会违反完整性约束。

`initially deffered`子句加入到约束声明中，在事务结束的时候检查。

对于声明为可延迟的约束，执行`set constraints constrant-list deferred`语句作为事务的一部分，会导致对指定约束的检查被延迟到该事务结束时执行。

#### 复杂check条件和断言

check子句中的谓词可以是包含子查询的任意谓词



```sql
check time_slot_id in (select time_slot_id from time_slot)
```



断言



```sql
create assertion <assertion-name> check <predicate>
```



一个断言就是一个谓词，它表达了我们希望数据库总能满足的一个条件。

### SQL的数据类型与模式

日期和时间类型：date,time,timestamp

默认值:default关键字，在create table的时候可以用在某个属性上

创建索引`create index studentID_index on student(ID)`

创建与现有的某个表模式相同的表`create table T2 like T1`

### 授权

#### 权限

权限包括：select, insert, update, delete

授予权限



```sql
grant <权限列表> on <关系名或视图名> to <用户/角色列表>
```



收回权限



```sql
revoke <权限列表> on <关系名或视图名> from <用户/角色列表>
```



用户名**public**指系统的所有当前用户和将来的用户，对public授权即对现在和未来所有用户授权

#### 角色

创建角色



```sql
create role instructor
```



角色可以授予给用户，角色也可以授予给角色



```sql
grant dean to Amit;
create role dean;
grant instructor to dean;
grant dean to Satoshi
```



注意角色链上的权限

#### 视图的授权

创建视图的用户不需要获得该视图上的所有权限，他得到的权限不会为他提供超越现有权限的额外授权。创建视图的用户如果没有关系上的update权限，那么也不能update视图。

#### 模式的授权

只有模式的拥有者才能执行对模式的任何修改：如创建/删除关系，增加/删除关系的属性，增加/删除索引

**references权限**：允许用户在创建关系时声明外码

需要此权限的原因：用户在某一关系上声明外码的行为会影响到被参照的关系

#### 权限的收回

默认是级联收回，但可以申明**restrict**防止级联收回

声明了restrict之后，若收回产生了级联收回，系统就会返回错误，并且不执行收权动作

grant option允许用户将权限授予给其他的用户，要注意**授权链**



```sql
grant select on department to Amit with grant option
```



下面的语句仅仅收回grant option，并不收回select权限本身



```sql
revoke grant option for select on department from Amit
```



最好是将权限授予给角色，而不是用户，这样方便管理

## 6 形式化关系查询语言

（侧重关系代数，注意外连接的关系代数写法。元组关系演算只要会写基本查询即可）

### 关系代数

#### 基本运算

六个基本操作：选择$\sigma$、投影$\Pi$、并集$\bigcup$、集合差$-$、卡氏积$\times$、更名$\rho$

**选择$\sigma$**

在关系中选出满足给定谓词的元组



```sql
select * from instructor where dept_name = "Physics"
```




$$

\sigma_{dept\_name='Physics'}(instructor)
$$



允许在谓词中使用and$\land$, or$\lor$,not$\neg$,>,<之类

**投影$\Pi$**

返回的关系只有某些选定的属性



```sql
select ID, name, salary from instructor
```




$$

\Pi_{ID,name,salary}(instructor)
$$



关系运算的组合



```sql
select name from instructor where dept_name='Physics'
```




$$

\Pi_{name}(\sigma_{dept\_name='Physics'}(instructor))
$$



**并运算$\bigcup$**

找到2009年秋季学期或2010年春季学期，或两者皆开的所有课程



$$

\Pi_{course\_id}(\sigma_{semester='Fall'\land year=2009}(section))\bigcup \Pi_{course\_id}(\sigma_{semester='Spring'\land year=2010}(section))
$$



注意并运算是集合运算，不会出现重复元组

**集合差-**

找到2009年秋季学期开，但2010年春季学期不开的课



$$

\Pi_{course\_id}(\sigma_{semester='Fall'\land year=2009}(section))- \Pi_{course\_id}(\sigma_{semester='Spring'\land year=2010}(section))
$$



并运算和集合差运算的**两个关系必须要相容**，两个关系是同元的，且对应的属性域都相同

**卡氏积$\times$**

找到所有物理系的教师和他们所授课程



```sql
select name, course_id from 
	(select * from instructor full outer join teaches where dept_name='Physics')
where instructor.ID = teaches.ID
```




$$

\Pi_{name,course\_id}(\sigma_{instructor.ID=teaches.ID}(\sigma_{dept\_name='Physics'}(instructor\times teaches)))
$$



**更名运算$\rho$**

选出不是最高工资的老师和薪水



$$

\Pi_{instructor,salary}(\sigma_{instructor.salary<d.salary}(instructor\times \rho_{d}(instructor)))
$$



#### 附加的运算

集合交$\bigcap$、自然连接$\bowtie$、赋值、外连接、除法$\div$

**集合交**

用法类似于集合并

**自然连接**

选出老师和他们所授的课



$$

\Pi_{name,course\_id}(instructor\bowtie teaches)
$$



**赋值运算**

给临时关系变量赋值



$$

temp1 \leftarrow R\times S\\
temp2 \leftarrow \sigma_{r.A1=s.A1 \land ...}(temp1)\\
result=\Pi_{R\bigcup S}(temp2)
$$



**外连接**

左外连接⟕右外连接⟖，全外连接⟗

**除法$\div$**

除法是笛卡尔积的逆运算

$r\div s = t$条件：S是R的真子集，结果t是满足以下条件的最大的集合$t\times s \subseteq r$

#### 扩展的运算

**广义投影**



$$

\Pi_{F1,F2,...,Fn}(E)
$$



其中，$F_i$是设计常量以及E中的模式中属性的算数表达式，例如



$$

\Pi_{ID,name,dept_name,salary/12}(instructor)
$$



**聚集G**

聚集函数输入值的一个汇集，将单一值作为结果返回，聚集函数如sum，count，min，max

多重集：汇集中的一个值可以出现多次。集合是多重集的特例，每个值只出现一次

找出所有教师工资的总和



$$

G_{sum(salary)}(instrutor)
$$



使用distinct



$$

G_{count\_distinct(ID)}(\sigma_{semester='Spring'\land year=2010}(teaches))
$$



有时候希望对一组元组集合而不是单个元组集合执行聚集函数，比如求出每个系的平均工资



$$

_{dept\_name}G_{average(salary)}(instructor)
$$



```sql
select dept_name, average(salary) from instructor group by dept_name
```



#### 关系代数优先权

1. $\sigma,\Pi,\rho$
2. $\times, \bowtie$
3. $\bigcap$
4. $\bigcup,-$

### 元组关系演算

非过程性的查询语言

- 查询的形式为${t|p(t)}$，所有使为此P为真的元组t的集合。
- $t[A]$表示元组t在属性A上的值
- $t \in r$表示元组t在关系r中

#### 查询示例

找出所有工资在80000美元以上的教师的元组



$$

\{t|t \in instructor \land t[salary]>80000\}
$$



假设只要ID属性，要引入$\exists$



$$

\{t|\exists s \in instructor(t[ID]=s[ID] \land s[salary] > 80000)\}
$$



元组变量t只定义在ID属性上，因此结果得到ID上的关系

在多个关系中进行查询，找出位置在Watson楼的系中的所有教师姓名



$$

\{t|\exists s \in instructor(t[name]=s[name] \land \\
\exists u \in department(u[dept\_name]=s[dept\_name] \land u[building]='Watson'))\}
$$



## 7 数据库设计和E-R模型

### 设计过程概览

**设计阶段**

- 描述用户需求
- 概念设计（常用实体-联系模型表示）
- 功能需求规格说明
- 从抽象数据模型到数据库实现
  - 逻辑设计阶段
  - 物理设计阶段（10章11章）

**设计选择**

避免这两个主要的缺陷：

- 冗余
- 不完整

### 实体-联系模型

三个基本概念：实体集、联系集、属性

#### 实体集

**实体**是现实世界中可区别于所有其他对象的一个“事物”或“对象”

**实体集**是相同类型即具有相同性质（或属性）的一个实体集合

#### 联系集

**联系**是指多个实体间的相互关联

**联系集**是相同类型联系的集合

联系也可以具有**描述性属性**

**自环的**（递归的）联系集：自己和自己关联（如先修课程关系）

联系集的**度**：联系中的实体集的个数

二元联系（只关联两个实体）

#### 属性

属性的**域/值集**：属性可取值的集合

E-R模型中的属性类型：

- 简单和复合属性：复合属性可以再划分为更小的其他属性
- 单值和多值属性：单值如学生实体的学号，多值如教师实体的电话号码（看实体在此属性上对应多少个值）
- 派生属性：从别的相关属性或实体派生出来。派生属性的值不存储，需要的时候计算。如属性students_advised表示一个教师指导的学生数，可以通过统计和一个教师相关联的学生实体数知道。

### 约束

#### 映射基数

映射基数/基数比率：表示一个实体通过一个联系集能关联的实体的个数

一对一、一对多、多对一、多对多

#### 参与约束

**全部**：实体集E中的**每一个**实体都参与到联系集R的至少一个联系中

**部分**：E中只有**部分**实体参与到R的联系中

#### 码

实体的码是一个足以区分每个实体的属性集。超码、候选码、主码的概念同前。

### 实体-联系图

#### 基本结构

- **分成两部分的矩形**代表实体集
- **菱形**代表联系集
- **未分割的矩形**代表联系集的属性。构成主码的属性以下划线标明
- **线段**将实体集连接到联系集
- **虚线**将联系集属性连接到联系集
- **双线**显示实体在联系集中的参与度
- **双菱形**代表连接到弱实体集的标志性联系集

![](/2019/12/30/databaseReview/ER_structure.jpg)

#### 映射基数

一方用带箭头的，多方不带箭头

![](/2019/12/30/databaseReview/ER_mapping.jpg)

![](/2019/12/30/databaseReview/ER_mapping.jpg)

用`L..H`表示，L表示最小的映射基数，H表示最大的映射基数，例如下图，`0..*`表示instructor可以有0个学生或多个学生，`1..1`表示学生最多有一个老师。因此是一个一对多的。

![](/2019/12/30/databaseReview/ER_example1.jpg)

![](/2019/12/30/databaseReview/ER_example1.jpg)

#### 参与度

全参与用双线，部分参与用单线

![](/2019/12/30/databaseReview/ER_participate.jpg)

每一个section至少对应一个course，有的course可以没有上课时间section，一个course可以对应多个section

#### 复杂的属性

![](/2019/12/30/databaseReview/ER_complex.jpg)

name,address，street复合属性，{phone_number}多值属性，age()派生属性

注意多值属性会破坏原子性

#### 角色

在菱形和矩形之间的连线上进行标注来表示角色

![](/2019/12/30/databaseReview/ER_role.jpg)

![](/2019/12/30/databaseReview/ER_role.jpg)

#### 非二元的联系

在这种联系中，最多使用一个箭头（一方），否则会造成歧义

### 弱实体集

- **没有足够的属性以形成主码的实体集**，它的存在依赖于另一个实体集（标识/属主实体集）。【有主码的实体集称强实体集】
- 将弱实体集与其标识实体集相关联的联系称为**标识性联系**
- 弱实体集的主码由**标识实体集的主码**加上该弱实体集的**分辨符**构成。
- 关联弱实体集和标识强实体集的联系集用**双菱形**表示；弱实体集的分辨符用**虚下划线**标明

### 转换为关系模式

（关注生成的关系模式的属性、主码、外码约束）

#### 具有简单属性的强实体集的表示

强实体集有n个**属性**，就用有n个属性的关系模式来表示它

强实体集的主码就是生成的模式的**主码**

#### 具有复杂属性的强实体集的表示

**复合属性**

为每个子属性创建一个单独的属性来处理复合属性。而复合属性自身并不会创建属性。

比如复合属性name，模式中生成的属性为first_name,middle_initial,last_name，注意没有单独的name属性了。

**多值属性**

对于一个多值属性M，构建关系模式R，该模式包含一个对应于M的属性A，以及对应于M所在的实体集或联系集的主码的属性（主码属性到了生成的R中作为主码）。

比如instructor_phone(ID,phone_number)

#### 弱实体集的表示

假设A是弱实体集，有n个属性，B是A依赖的标识实体集，主码包括m个属性。那么生成的关系模式为这**m+n个属性**。关系模式的主码是**A的分辨符+B的主码**。

要为生成的关系模式上建立外码约束，指明m个属性参照关系B的主码。

#### 联系集的表示

假设R是联系集，a1,…an表示所有的参与R的实体集主码的并集构成的属性集合，设R的描述属性为b1,..bm,那么生成的关系模式属性为这**m+n个属性**。

选择联系集的主码：

- 对于多对多的关系，参与实体集的**主码属性的并集**称为主码
- 对于一对一的，**任意**一个实体集的主码都可以选作主码。
- 对于多对一，一对多，选择**多方**的主码作为主码

对于每个与联系集R相关的实体集Ei，我们建立一个关系模式R上的**外码约束**，R中来自Ei主码属性的那些参照关系模式Ei的主码

##### 模式的冗余

一般情况下，连接弱实体集与其所依赖的强实体集的联系集的模式是冗余的，而且在基于E-R图的关系数据库设计中不必给出

##### 模式的合并

考虑从实体集A到实体集B的一个多对一的联系AB，进一步假设A在该联系集中的参与是全部的。那么我们可以将A和AB模式合并称单个包含两个模式所有属性的并集的模式。合并后模式的主码是其模式中融入了联系集模式的那个**实体集的主码**。

## 8 关系数据库设计

### 原子域和第一范式

一个域是**原子的**，如果该域的元素被认为是不可分的单元。

我们称一个关系模式R属于**第一范式**，如果R的所有属性的域都是原子的。

### 使用函数依赖进行分解

表示法说明：

- r(R)：该模式是关系r的，R表示属性集
- 当属性集是一个超码时，用K表示

#### 码和函数依赖

令r(R)是一个关系模式。

R的子集K是r(R)的超码的条件是：在关系r(R)的任意合法实例中，对于r的实例中的所有元组对$t_1和t_2$总满足$若t_1 \neq t_2,则t_1[K] \neq t_2[K]$，即没有两条元组在属性K上具有相同的值。

**函数依赖**$\alpha \rightarrow \beta$：对实例中所有元组对$t_1和t_2,若t_1[\alpha]=t_2[\alpha]，则t1[\beta]=t2[\beta]$

【属性组x的取值能够唯一确定属性组y的值，那么x函数确定y，y是关于x的一个函数】

如果模式r(R)中的每个合法实例都满足函数依赖，我们说该函数依赖在模式r(R)上成立。

如果函数依赖$K \rightarrow R$在r(R)上成立，则K是r(R)的一个超码。

**平凡依赖**：如果$\beta \subseteq \alpha$，则形如$\alpha \rightarrow \beta$的函数依赖是平凡的。

**函数依赖集的闭包**：$F^+$，表示F集合的闭包，从给定F集合推导出的所有函数依赖的集合

#### Boyce-Codd范式(2.5范式)

具有函数依赖集$F$的关系模式$R$属于BCNF的条件是，对$F$的闭包**$F^+$中所有**形如$a\rightarrow b$的函数依赖集。函数依赖至少符合下面两种情况之一:

- $a \rightarrow b$ 是平凡的
- 超码依赖：$a$是R的一个超码

##### 分解成BCNF

设R为不属于BCNF的一个模式。则存在至少一个非平凡的函数依赖$\alpha \rightarrow \beta$，其中$\alpha$不是R的超码，我们在设计中用一下两个模式取代R

- $(\alpha \bigcup \beta)$
- $(R-(\beta - \alpha))$

##### BCNF和依赖保持

BCNF可以做到无损连接，但是并不总是做到依赖保持

#### 第三范式

具有函数依赖集F的关系模式R属于第三范式的条件是：对于$F^+$中所有形如$\alpha \rightarrow \beta$的函数依赖，至少以下一项成立：

- $\alpha \rightarrow \beta$是一个平凡的函数依赖
- $\alpha$是R的一个超码
- $\beta - \alpha$中的每个属性A都包含于R的一个候选码中

注意任何满足BCNF的模式也满足3NF，3NF的定义允许某些BCNF中不允许的函数依赖。

### 函数依赖理论

#### 函数依赖集的闭包

**ArmStrong公理**

- 自反律：$若\alpha为一属性集且\beta \subseteq \alpha，则$$\alpha \rightarrow \beta成立$
- 增补律：$若\alpha \rightarrow \beta成立且\gamma为一属性集，则\gamma \alpha \rightarrow \gamma \beta成立$
- 传递律：$若\alpha \rightarrow \beta和\beta \rightarrow \gamma成立，则\alpha \rightarrow \gamma成立$

ArmStrong公理是正确且有效的，这些规则是完备的

便于计算的规则

- 合并律：$若\alpha \rightarrow \beta和\alpha \rightarrow \gamma成立，则\alpha \rightarrow \beta\gamma成立$
- 分解律：$若\alpha \rightarrow \beta\gamma成立，则\alpha \rightarrow \beta和\alpha \rightarrow \gamma成立$
- 伪传递律：$若\alpha \rightarrow \beta和\gamma\beta \rightarrow \delta成立，则\alpha\gamma \rightarrow \delta成立$

**计算$F^+$**



$$

\begin{align}
&F^+=F\\
&repeat\\
&\quad for \space each \space F^+中的函数依赖f \\
&\quad \quad 在f上应用自反律和增补律\\
&\quad \quad 将结果加入到F^+中\\
&\quad for \space each \space F^+中的一对函数依赖f_1和f_2\\
&\quad \quad if \space f_1和f_2可以使用传递律结合起来\\
&\quad \qquad 将结果加入到F^+中 \\
&until \space F^+不再发生变化
\end{align}
$$



#### 属性集的闭包

如果$\alpha \rightarrow \beta$，我们称属性B被$\alpha$函数确定。**要判断集合$\alpha$是否为超码，须计算$\alpha$函数确定的属性集**。一种方法是计算$F^+$，找出左半部为$\alpha$的函数依赖，并合并这些函数依赖的右半部，但是开销很大。

令$\alpha$为一个属性集。我们将函数依赖集F下被$\alpha$函数确定的所有属性的集合称为F下$\alpha$的闭包，记为$\alpha^+$

**计算$\alpha^+$**



$$

\begin{align}
&result := \alpha\\
&repeat\\
&\quad for \space each 函数依赖\beta \rightarrow \gamma \space in F \space do \\
&\quad\quad begin\\
&\quad\quad\quad if \space \beta \subseteq result \space then\space result:=result\bigcup\gamma;\\
&\quad\quad end\\
&until(result不变);
\end{align}
$$



#### 正则覆盖

无关属性：如果去除函数依赖中的一个属性不改变该函数依赖集的闭包，则称该属性是无关的。形式化定义如下：考虑函数依赖集F及F中 的函数依赖$\alpha \rightarrow \beta$

- 如果 $A \in \alpha$并且F逻辑蕴含$(F-{\alpha \rightarrow \beta}\bigcup {(\alpha-A) \rightarrow \beta})$，则属性A在$\alpha$中是无关的【考虑函数依赖的左边：$\alpha$不需要A也能推出$\beta$】
- 如果$A \in \beta$并且函数依赖集$(F-{\alpha \rightarrow \beta})\bigcup {\alpha \rightarrow(\beta - A )})$逻辑蕴含F，则属性A在$\beta$中是无关的【考虑函数依赖的右边：$\beta$中的A属性可以被其他的函数依赖推出来】

注意蕴含的方向，如果左半部分和右半部分交换，蕴含关系将总是成立的。

F的正则覆盖$F_c$是一个依赖集，使得F逻辑蕴含$F_c$中的所有依赖，并且$F_c$逻辑蕴含F中的所有依赖。此外$F_c$必须具有如下性质：

- $F_c$中任何函数依赖都不含无关属性
- $F_c$中函数依赖的**左半部都是唯一的**，即$F_c$中不存在两个依赖$\alpha_1 \rightarrow \beta_1$和$\alpha_2 \rightarrow \beta_2$满足$\alpha_1 = \alpha_2$

**计算正则覆盖**



$$

\begin{align}
&F_c=F\\
&repeat\\
&\quad 使用合并律将F_c中所有形如\alpha_1 \rightarrow \beta_1 和\alpha_1 \rightarrow \beta_2的依赖替换为\alpha_1 \rightarrow \beta_1 \beta_2\\
&\quad 在F_c中寻找一个函数依赖\alpha \rightarrow \beta,它在 \alpha或在\beta中具有一个无关属性\\
&\quad/*注意使用的是F_c而不是F检验无关属性*/\\
&\quad如果找到一个无关属性，则将它从F_c中的\alpha \rightarrow \beta中删除\\
&until(F_c不变)
\end{align}
$$



#### 无损分解

**无损分解**：令r(R)为一个关系模式，F为r(R)上的函数依赖集。令$R_1$和$R_2$为R的分解。如果用两个关系模式r($R_1$)，r($R_2$)替代r(R)时没有信息损失，则我们称该分解是无损分解。用关系代数可以表示为:



$$

\Pi_{R_1}(r) \bowtie \Pi_{R_2}(r) = r
$$



分解后的两个模式自然连接的结果和原来被分解的模式一样。

不是无损分解的分解称为**有损分解**。

**用函数依赖来说明无损分解**

$R_1,R_2$是R的无损分解如果以下函数依赖中至少有一个属于$F^+$：

- $R_1 \bigcap R_2 \rightarrow R_1$
- $R_1 \bigcap R_2 \rightarrow R_2$

即如果**$R_1 \bigcap R_2$是$R_1$或$R_2$的超码**，R上的分解就是无损分解。

#### 保持依赖

令F为模式R上的一个函数依赖集，$R_1,R_2,…R_n$为R的一个分解。F在$R_i$上的**限定**是$F^+$中所有只包含$R_i$中属性的函数依赖的集合$F_i$。

令$F’ = F_1 \bigcup F_2 \bigcup …\bigcup F_n$。我们称具有性质$F’^+=F^+$的分解为**保持依赖的分解**。

**避免计算$F^+$的验证保持依赖的方法**

result = $\alpha$

repeat

​ for each 分解后的$R_i$

​ $t = (result \bigcap R_i)^+ \bigcap R_i$

​ $result = result \bigcup t$

​ until (result没有变化)

### 分解算法

#### BCNF分解

##### BCNF的判定方法

简化判定一个关系是否BCNF：

- 检查非平凡依赖$\alpha \rightarrow \beta$，计算属性的闭包$\alpha^+$，检查它是否包含R中的所有属性，即验证它是否R的超码
- 检查关系R是否BCNF，检查F中的依赖就可以了【F中的依赖满足，$F^+$的也会满足】

分解后的关系$R_i$判定是否BCNF：

- 对于$R_i$中属性的每个子集$\alpha$，确保$\alpha^+$（F下的属性闭包）要么不包含$R_i - \alpha$的任何属性，要么包含$R_i$的所有属性

##### BCNF分解算法

result := {R}

​ done := false;

​ 计算$F^+$;

​ while (not done) do

​ if (result中存在模式$R_i$不属于BCNF)

​ then begin

​ 令$\alpha \rightarrow \beta$为一个在$R_i$上成立的非平凡函数依赖，满足$\alpha \rightarrow R_i$不属于$F^+$，并且$\alpha \bigcap \beta = \emptyset$;

​ $result := (result-R_i)\bigcup (R_i-\beta)\bigcup (\alpha,\beta)$;

​ end

​ else done := done

#### 3NF分解

#### BCNF和3NF的比较

3NF优点：保持依赖，无损分解

BCNF不一定是依赖保持的

### 多值依赖

令r(R)为一关系模式，并令$\alpha \subseteq R 且 \beta \subseteq R$。多值依赖$\alpha \rightarrow \rightarrow \beta$在R上成立的条件是，在关系r(R)的任意合法实例中，对于r中任意一对满足$t_1[\alpha]=t_2[\alpha]$的元组对$t_1和t_2$，r中都存在元组$t_3$和$t_4$，使得



$$

t_1[\alpha]=t_2[\alpha]=t3[\alpha]=t_4[\alpha]\\
t_3[\beta] = t1[\beta]\\
t_3[R-\beta]=t_2[R-\beta]\\
t_4[\beta] = t_2[\beta]\\
t_4[R-\beta]=t_1[R-\beta]
$$



#### 冗余度排序

4NF < BCNF < 3NF < 1NF

## 11 索引和散列

### 基本概念

基本索引类型：

- 顺序索引
- 散列索引

### 顺序索引

**聚集索引（主索引）**：包含记录的文件按照某个搜索码指定的顺序排序

**非聚集索引（辅助索引）**：搜索码指定的顺序与文件中记录的物理顺序不同

在搜索码上有聚集索引的文件称作**索引顺序文件**。

**索引项/索引记录**：由一个搜索码值和指向具有该搜索码值的一条或多条记录的指针构成。

两类顺序索引：

- **稠密索引**：在稠密索引中，文件中的的每个搜索码值都有一个索引项
- **稀疏索引**：在稀疏索引中，只为搜索码的某些值建立索引项

**多级索引**：具有两级多两级以上的索引称为多级索引

如在原始的内层索引上构造一个稀疏的外层索引

### $B^+$树索引文件

$B^+$树索引采用平衡树结构，其中树根到树叶的每条路径的长度相同。树种每个非叶节点有$\lceil n/2\rceil \sim n$个子女，其中n对于特定的树是固定的。（n可以理解为节点最大指针数，故节点最大能放n-1个值）

#### $B^+$树的结构

![](/2019/12/30/databaseReview/b_leaf.jpg)

![](/2019/12/30/databaseReview/b_leaf.jpg)

**叶子节点**

对 $i=1,2,…,n-1$，指针$P_i$指向具有搜索码值$K_i$的一条文件记录。

指针$P_n$用来指向按照搜索码顺序的下一个叶子节点（一般右边兄弟节点）

叶子节点包含的值的范围是$\lceil(n-1)/2\rceil \sim (n-1)$

**非叶节点**

形成叶节点上的一个多级（稀疏）索引

在$P_1$指向的子树中的所有的搜索码值都比$K_1$小

对于$P*i$所指向的子树，里面搜索码的值大于等于$K*{i-1}$，小于等于$K_i$

$P*n$所指向的子树，里面搜索码的值大于等于$K*{n-1}$

**根节点**

包含的指针数可以小于$\lceil n/2 \rceil$

除非整棵树只有一个节点，否则根节点必须至少包含两个指针

#### $B^+$树的更新

##### 插入

在一个已经建好的树中插入/构造一个二叉树

1. 先找到搜索码在叶子节点上的位置
2. 如果搜索码值已经出现在叶子节点上

   1. 把新记录插到原表里面
   2. 如果必要的话，添加一个指针到桶/链表里面，物理地址插入到叶子节点里来
3. 若搜索码值没有出现

   1. 把记录添加到主文件中，如果必要的话创建一个桶
   2. 对索引树作修改。如果当前叶子节点还有空间，把key-value和pointer加进去，要排序
   3. 否则，分割节点（当前叶子节点没有空间了）

**分割叶子节点：**

取n对search-key-value和poniter，排好序，分成两部分，前一部分留在旧节点，剩下的放到新节点里面

记新节点为p，令k为p中最小的key-value，**在被分割节点（旧节点）的父节点中插入(k,p)**【注意，(k,p)这个值既出现在新叶子节点中，也出现在父节点中，这个父节点也成为新节点的父节点】

**分割父节点：**

若父节点是满的，对父节点进行分割，之后再分割子节点

**分割节点自下往上，直到找到一个不是满的节点**

最坏情况导致树的高度增加1，根节点也进行了分割

分割父节点的时候，分成了两部分新的节点，第二部分的第一个节点直接向上挪动，而不会再出现在原先的节点中。例如：

![](/2019/12/30/databaseReview/b_splitFather.jpg)

![](/2019/12/30/databaseReview/b_splitFather.jpg)

##### 删除

寻找要删除的记录，将它从主文件和桶中删除

从叶子节点上删除指针和搜索码

如果节点N因删除而条目太少，而且它有一个兄弟节点可以进行合并的，则进行合并：

1. 把两个节点的所有的搜索码值和指针插入到单一节点中，删除另外一个节点
2. 删除$(K_{i-1},P_i)$,$P_i$是原来指向被删除的节点的指针，来自被删节点的父节点，**递归地重复这个过程**
3. 若N和N’不是叶子节点：复制搜索码$K_{i-1}$到新的节点

否则，如果节点N因删除而条目太少，而且兄弟节点不能进行合并，那么**重新分配指针**：

1. 重新分配，在叶子节点，直接从兄弟节点拉过来就可
2. 若N和N’不是叶子节点，N实际上从父节点借一个条目，然后，父节点再从N’借一个

一般能合并的话优先考虑具有相同父母的兄弟节点

先尝试进行合并，不能合并再借

重新分配，一般借一个码值就可以了

![](/2019/12/30/databaseReview/b_delete.jpg)

![](/2019/12/30/databaseReview/b_delete.jpg)

#### 不唯一的搜索码

假如一个关系可以拥有多个包含同一搜索码值的记录，那么该搜索码称为**不唯一搜索码**。

不唯一搜索码影响查找效率。

一种解决方法：原始搜索码+额外的属性=复合搜索码。这个额外属性也称**唯一化属性**。

#### $B^+$树更新的复杂性

在最坏情况下，一次插入的I/O操作次数可能正比于$log_{\lceil n/2 \rceil}(N)$，其中n值节点中指针最大值，N是索引文件的记录条数。

删除也是。

### 散列索引

#### 静态散列

$H(K_i)$给出了存放记录的桶的地址。

桶溢出处理：线性探查法

#### 动态散列

桶号可以进行扩展。

可扩展散列：其中一个桶满了的时候，所有的桶进行double，桶号就变了，可以利用的哈希桶也增多了。mysql使用的

### 有序索引和哈希的比较

哈希只能做一个精确值的查找，但是范围查找难做到

哈希精确值查找效率高

**主索引不能为空，唯一索引可以取空值**

## 12 查询处理

### 概述

查询处理的过程如下

![](/2019/12/30/databaseReview/query_process.jpg)

![](/2019/12/30/databaseReview/query_process.jpg)

### 查询代价的度量

主要因素：磁盘交互时间

简化起见，忽略CPU时间，仅用磁盘存取代价来度量查询计划的代价。

Number of seeks\*average-seek-cost寻址

Number of read\*average-block-read-cost读

Number of blocks written\*average-block-write-cost写

读和写：block transfers

我们用传送磁盘块数number of block transfer以及搜索磁盘次数number of seeks来度量查询计划的代价

$t_T$：time to transfer block传输盘块的时间

$t_S$：time for seek one 搜索磁盘的时间

### 选择操作

#### 使用文件扫描和索引的选择

##### 线性查找

**A1 线性查找**：在线性搜索中，系统扫描每一个文件块，对所有记录都进行测试，看它们是否满足选择条件

##### 索引扫描

**A2 主索引，码属性等值比较**：对于具有主索引的码属性的等值比较，我们可以使用索引检索到满足相应等值条件的唯一一条记录

**A3 主索引，非码属性等值比较**：当选择条件是基于非码属性A的等值比较时，我们可以利用主索引检索到多条记录

**A4 辅助索引，等值比较**：若等值条件是码属性上的，则该策略可检索到唯一一条记录；若索引字段是非码属性，则可能检索到多条记录。

#### 涉及选择的比较

考虑形如$\sigma_{A \leq v}(r)$

**A5 主索引，比较**：在选择条件是比较时，可以使用顺序主索引（如$B^+$树主索引）

**A6 辅助索引，比较**

**选择算法代价估计**

|  | 算法 | 开销 | 原因 |
| --- | --- | --- | --- |
| A1 | 线性搜索 | $t_s+b_r\*t_T$ | 一次初始搜索加上$b_r$个块传输。$b_r$表示在文件中的块数量 |
| A1 | 线性搜索，码属性等值比较 | 平均$t_s+(b_r/2)\*t_T$ | 因为最多一条记录满足条件，所以只需要找到所需的记录，扫描就可终止。最坏情况仍然需要$b_r$个块传输 |
| A2 | $B^+$树主索引，码属性等值比较 | $(h_i+1)\*(t_T+t_s)$ | 其中$h_i$表示索引的高度。索引查找穿越树的高度，再加上一次IO来取记录，一次IO需要一次搜索和一次块传输 |
| A3 | $B^+$树主索引，非码属性等值比较 | $h_i*(t_T+t_s)+b*t_T$ | 树的每层一次搜索，第一个块一次搜索。b是包含具有指定搜索码记录的块数。 |
| A4 | $B^+$树辅助索引，非码属性等值比较 | $(h_i+n)\*(t_T+t_s)$ | n是所取记录数。索引查找的代价和A3相似，但是每条记录可能在不同的块上，这需要每条记录一次搜索。如果n值比较大，代价可能会非常高。 |
| A5 | $B^+$树主索引，比较 | $h_i*(t_T+t_s)+b*t_T$ | 同A3 |
| A6 | $B^+$树辅助索引，比较 | $(h_i+n)\*(t_T+t_s)$ | 同A4 |

#### 复杂选择的实现

- 合取
- 析取
- 取反

A7 利用一个索引的合取选择

A8 使用组合索引的合取选择

A9 通过标识符的交实现合取选择

A10 通过标识符的并实现析取选择

### 排序

#### 外部排序归并算法

M表示内存缓冲区中可以用于排序的块数。

1. 建立多个排好序的归并段。
2. 对归并段进行归并。暂定归并段的总数N小于M，这样我们可以为每个归并段文件分配一个块，此外剩下的空间还应能容纳存放结果的一个块。

**二路归并排序**（要掌握）

通常M=3，两个块放输入，一个块放输出

![](/2019/12/30/databaseReview/merge.jpg)

![](/2019/12/30/databaseReview/merge.jpg)

#### 外部排序归并的代价分析

记$b*r$代表包含关系r中记录的磁盘块数。第一阶段读入关系的每一数据块并写出，共需$2b_r$次磁盘块传输。初始归并段数为$\lceil b_r/M \rceil$。每一趟归并会使归并段疏密减少为原来的$1/(M-1)$。总共所需归并趟数为$\lceil log*{M-1}(b_r/M)\rceil$

关系外排序的磁盘块传输总数：$b*r(2\lceil log*{M-1}(b_r/M)\rceil +1)$

### 连接运算

用等值连接表示形如$r \bowtie_{r.A=s.B} s$的连接

下面用$b_r,b_s$分别表示关系r和关系s中的磁盘块数，$n_r,n_s$表示关系r和s中的记录数。

#### 嵌套循环连接

- 嵌套循环连接算法的代价很大，因为该算法逐个检查两个关系中的每一对元组
- 在最坏情况下，缓冲区只能容纳每个关系中的一个数据块，这时共需$n_r \times b_s +b_r$次块传输
- 如果一个关系能完全放在内存中，那么把这个关系作为内层关系来处理是有好处的。因为这样内层循环关系只需要读一次
- 在最好的情况下，内存能**同时容纳两个关系**，此时每一数据块只需读一次，只需要$b_r+b_s$次块传输加上两次磁盘搜索

![](/2019/12/30/databaseReview/nested.jpg)

![](/2019/12/30/databaseReview/nested.jpg)

#### 块嵌套循环连接

- 在最坏的情况下，对于外层关系中的每一个块，内层关系s的每一块只须读一次，而不是对外层关系的每一个元组读一次。因此，在最坏情况下，共需$b_r \*b_s +b_r$次块传输
- 显然，如果内存不能容纳任何一个关系，则使用较小的关系作为外层关系更有效
- 在最好的情况下，内存能容纳内层关系，需要$b_r+b_s$次块传输加上两次磁盘搜索（把较小的关系作为内层关系）
- 假设内存有M块，代价是：$块传输:\lceil b_r/(M-2)\*b_s+b_r \rceil ;磁盘搜索:2\lceil b_r/(M-2)\rceil$

![](/2019/12/30/databaseReview/block_nested.jpg)

![](/2019/12/30/databaseReview/block_nested.jpg)

#### 索引嵌套循环连接

在嵌套循环连接中， 如果内层关系中的连接属性上有索引，则可以使用索引查找替代文件扫描

对于外层关系的r的每一个元组，需要在关系s的索引上进行查找，检索相关元组。

在最坏情况下，缓冲区只能容纳关系r的一块和索引的一块。

此时，读取关系r需要$b_r$次IO操作，这里$b_r$指包含关系r中记录的磁盘块数

连接的时间代价可以用$b_r(t_T+t_s)+n_r\*c$来计算。

#### 归并连接

可用于计算自然连接和等值连接

假设为每个关系分配$b_b$个缓冲块：

代价：$b_r+b_s$次块传输+$\lceil b_r/b_b \rceil + \lceil b_s/b_b \rceil$次搜索

![](/2019/12/30/databaseReview/merge_join.jpg)

![](/2019/12/30/databaseReview/merge_join.jpg)

#### 散列连接

可以实现自然连接和等值连接

在哈希连接算法中，用散列函数h来划分两个关系的元组，此算法的基本思想是把这两个关系的元组划分成在连接属性值上具有相同散列值的元组集合。

![](/2019/12/30/databaseReview/hash_join.jpg)

![](/2019/12/30/databaseReview/hash_join.jpg)

## 13 查询优化

掌握等价转化的基本规则

掌握选择操作有关的

### 等价规则

1. 合取选择运算可分解为单个选择运算的序列。该变换称为$\sigma$的级联

   

$$

\sigma_{\theta_1 \wedge \theta_2}(E) = \sigma_{\theta_1}(\sigma_{\theta_2}(E))
$$


2. 选择运算满足交换律

   

$$

\sigma_{\theta_1}(\sigma_{\theta_2}(E)) = \sigma_{\theta_2}(\sigma_{\theta_1}(E))
$$


3. 一系列投影运算中只有最后一个是必须的，其余的可省略。该转换也可称为$\sigma$的级联

   

$$

\Pi_{L_1}(\Pi_{L_2}(..(\Pi_{L_n}(E))...)=\Pi_{L_1}(E)
$$


4. 选择操作可与笛卡尔积以及$\theta$连接相结合

   1. $\sigma*{\theta}(E_1 \times E_2) = E_1 \bowtie*{\theta} E_2$
   2. $\sigma*{\theta_1}(E_1 \bowtie*{\theta*2} E_2)=E_1 \bowtie*{\theta_1 \wedge \theta_2}E2$
5. $\theta$连接运算满足交换律

   

$$

E_1 \bowtie_{\theta} E_2 = E_2 \bowtie_{\theta} E_1
$$


6. 1. 自然连接运算满足结合律

$$

(E_1\bowtie E_2)\bowtie E_3 = E_1 \bowtie(E_2\bowtie E_3)
$$


7. $\theta$连接具有以下方式的结合律

   

$$

   (E_1 \bowtie_{\theta_1} E_2)\bowtie_{\theta_2 \wedge \theta_3} E_3 = E_1 \bowtie_{\theta_1 \wedge \theta_3}(E_2 \bowtie_{\theta_2} E_3)
$$



   其中$\theta_2$只涉及$E_2,E_3$的属性。由于其中任意一个条件都可为空，因此笛卡尔积运算也满足结合律。连接运算满足结合律、交换律在查询优化中对于重排连接顺序是很重要的。
8. 选择运算在下面两个条件下对$\theta$连接运算具有分配律

   1. 当选择条件$\theta_0$中的所有属性只涉及参与连接运算的表达式之一（比如$E_1$）时，满足分配律

      

$$

\sigma_{\theta_0}(E_1 \bowtie_{\theta} E_2) = (\sigma_{\theta_0}(E_1))\bowtie_{\theta} E_2
$$


   2. 当选择条件$\theta_1$只涉及$E_1$的属性，选择条件$\theta_2$只涉及$E_2$的属性时，满足分配律

      

$$

\sigma_{\theta_1 \wedge \theta_2}(E_1 \bowtie_{\theta} E_2) = (\sigma_{\theta_1}(E_1)) \bowtie_{\theta} (\sigma_{\theta_2}(E_2))
$$


9. 投影运算在下面条件下对$\theta$连接运算具有分配律

   1. 令$L_1,L_2$分别代表$E_1,E_2$的属性。假设连接条件$\theta$只涉及$L_1 \bigcup L_2$中的属性，则：

      

$$

\Pi_{L_1 \bigcup L_2}(E_1 \bowtie_{\theta}E_2)=(\Pi_{L_1}(E_1))\bowtie_{\theta} (\Pi_{L_2}(E_2)))
$$


   2. 考虑连接$E*1 \bowtie*{\theta} E_2$。令$L_1,L_2$分别代表$E_1,E_2$的属性集；令$L_3$是$E_1$出现在连接条件$\theta$但不在$L_1 \bigcup L_2$中的属性；令$L_4$是$E_2$出现在连接条件$\theta$中但不在$L_1\bigcup L_2$中的属性，那么

      

$$

\Pi_{L_1 \bigcup L_2}(E_1 \bowtie_{\theta}E_2) = \Pi_{L_1 \bigcup L_2}((\Pi_{L_1\bigcup L_3}(E_1)\bowtie_{\theta}(\Pi_{L_2\bigcup L_4}(E_2))))
$$



1. 集合的并与交满足交换律

   

$$

E_1 \bigcup E_2 = E_2 \bigcup E_1\\
E_1 \bigcap E_2 = E_2 \bigcap E_1
$$


2. 集合的并与交满足结合律

   

$$

(E_1 \bigcup E_2) \bigcup E_3= E_1 \bigcup (E_2 \bigcup E_3)\\
(E_1 \bigcap E_2) \bigcap E_3= E_1 \bigcap (E_2 \bigcap E_3)
$$


3. 选择运算对并、交、差运算具有分配律

   

$$

\sigma_P(E_1 - E_2) = \sigma_P(E_1)-\sigma_P(E_2)
$$



   上述等价规则将`-`替换成$\bigcup,\bigcap$也成立，进一步有

   

$$

\sigma_P(E_1 - E_2) = \sigma_P(E_1)-E_2
$$



   上述等价规则将`-`替换成$\bigcap$时成立，但$\bigcup$不成立
4. 投影运算对并运算具有分配律

   

$$

\Pi_L(E_1\bigcup E_2) = (\Pi_L(E_1)\bigcup \Pi_L(E_2))
$$



## 14 事务

事务是访问并可能更新各种数据项的一个程序执行单元，用形如`begin transaction`和`end transaction`语句来界定。

### 事务的ACID特性

- **原子性**：事务的所有操作在数据库中要么全部正确反应出来，要么完全不反应。
  - 保证原子性的思路：对于事务要执行写操作的数据项，数据库系统在磁盘上记录其旧值。记录在日志文件中。
- **一致性**：隔离执行事务时，保持数据库的一致性。
  - 例如：A向B转账，一致性要求事务执行前后不改变A+B的和
- **隔离性**：尽管多个事务可能并发执行，每个事务都感觉不到系统中有其他事务在执行。
  - 事务的隔离性确保事务并发执行后的系统状态与这些事务以某种次序**一个接一个地执行**后的状态是等价的。确保隔离性是数据库系统中**并发控制系统**的责任
- **持久性**：一个事务成功完成后，它对数据库的改变必须是永久的，即使出现系统故障。（确保以下两条中的任何一条来达到持久性）
  - 事务做的更新在事务结束前已经写入磁盘
  - 有关事务已执行的更新信息已写到磁盘上，并且此类信息必须充分，能让数据库在系统出现故障后重新启动时重新构造更新

### 存储结构

- **易失性存储器**：信息通常在系统崩溃后不会幸存
- **非易失性存储器**：信息会在系统崩溃后幸存
- **稳定性存储器**：信息永远不会丢失（丢失的可能性微乎其微）

事务修改写入稳定性存储器（持久性），日志记录写入稳定性存储器（原子性）

### 事务原子性和持久性

**中止**事务造成的变更被撤销，称事务**已回滚**，典型方法：维护**日志**。

撤销**已提交**事务方法：执行一个**补偿事务**。

![](/2019/12/30/databaseReview/14-1.jpg)

![](/2019/12/30/databaseReview/14-1.jpg)

进入中止状态后，系统有两种选择：

- **重启**事务：仅当引起事务中止的是*硬件错误*而不是事务内部逻辑的软件错误。
- **杀死**事务：通常是事务*内部逻辑*造成的错误

### 事务隔离性

- 提高吞吐量和资源利用率：I/O活动可以和CPU处理并行执行
- 减少等待时间：不同时长事务共享CPU周期和磁盘存取。减少执行事务时不可预测的延迟。

不是所有的并发执行都能得到正确的结果。

并发调度的原则：要和某一个串行调度等价。这样可以保证数据库的一致性

### 可串行化

如果某调度和某一个串行调度等价，那么称其串行等价的。

- 冲突可串行化
- 视图可串行化

#### 指令冲突

对同一个数据，至少有一个是write指令的时候，这两条指令是冲突的

1. I=read(Q), J=read(Q)，顺序无关紧要。非冲突
2. I=read(Q), J=write(Q)，次序重要。冲突
3. I=write(Q), J=read(Q)，次序重要。冲突
4. I=write(Q), J=write(Q)，次序重要，影响后面读Q的指令。冲突

如果调度S可以经过一系列非冲突指令交换成S‘，称S和S’冲突等价。（注意是交换两个事务不冲突的指令，单个事务的内部读写顺序仍然相同）

若一个调度S与一个串行调度冲突等价，则称调度S是**冲突可串行化**的。

#### 优先图

有向边Ti->Tj表示在Ti和Tj对同一个数据项Q至少有一个是写，且Ti在Tj之前执行。

- 在Tj执行read(Q)之前，Ti执行write(Q)
- 在Tj执行write(Q)之前，Ti执行read(Q)
- 在Tj执行write(Q)之前，Ti执行write(Q)

如果优先图有环，则是非冲突可串行化的。

串行化顺序可以通过拓扑排序得到。

#### 视图可串行化

如果一个调度S的视图等价于一个串行调度的视图，那么称它为视图可串行化的。

### 事务隔离和原子性

#### 可恢复调度

可恢复调度应满足：对每对事务Ti和Tj，若Tj读取了之前由Ti所写的数据项，则Ti先于Tj提交

#### 无级联调度

无级联调度应满足：对于每对事务Ti和Tj，如果Tj读取了先前由Ti所写的数据项，则Ti必须在Tj**这一读操作前**提交。

每一个无级联调度都是可恢复调度。

缺点：并发性差。

### 事务隔离性级别

- 可串行化serializable：通常保证可串行化调度。
- 可重复读repeatable read：只允许读取已提交数据，而且在一个事务两次读取一个数据项期间，其他事务不得更新该数据。但该事务不要求与其他事务可串行化。
- 已提交读read commited：只允许读取已提交数据，但不要求可重复读。比如，在事务两次读取一个数据项期间，另一个事务更新了该数据并提交
- 未提交读read uncommited：允许读取未提交数据。这是SQL允许的最低一致性级别

以上所有隔离性级别都不允许**脏写**，即如果一个数据项已经被另外一个尚未提交或终止的事务写入，则不允许对该数据项执行写操作

## 15 并发控制

### 锁

- 共享的：S锁，如果事务获得了数据项Q上的S锁，则它可以读Q
- 排他的：X锁，如果事务获得了数据项Q上的X锁，它既可读又可写Q

使用lock-S(Q)表示申请共享锁，lock-X(Q)表示申请排他锁，unlock(Q)表示释放锁

**锁相容性矩阵**

|  | S | X |
| --- | --- | --- |
| S | true | false |
| X | false | false |

只有两个S锁是兼容的

### 死锁

事务都在等待其他事务释放锁，哪一个事务都不能正常执行。

如果在申请对另一数据项加锁之前我们不对当前锁住的数据项解锁，则可能会发生死锁。

死锁比产生不一致状态要好，死锁可以通过回滚来解决。

### 两阶段封锁协议

该协议要求每个事务分两个阶段提出加锁和解锁申请

1. **增长阶段**：事务可以获得锁，但不能释放锁
2. **缩减阶段**：事务可以释放锁，但不能获得锁

两阶段封锁协议保证冲突可串行化。

对于任何事务，在调度中该事务获得其最后加锁的位置称为事务的**封锁点**。

**严格两阶段封锁协议**：还要求事务持有的所有排他锁必须在事务提交后方可释放

**强两阶段封锁协议**：要求事务提交之前不得释放任何锁

### 死锁处理

#### 死锁预防

- 要求每个事务在它执行之前获得所有要用到的数据项的锁
- 只能按照制定好的偏序访问数据项

**更多的死锁预防策略**

时间戳

1. wait-die机制（基于非抢占技术）

   当事务Ti申请的数据项当前被Tj所持有，仅当Ti的时间戳小于Tj的时间戳时，允许Ti等待，否则Ti回滚（死亡）【“年老”的事务可以等待，“年轻”的事务立即回滚】
2. wound-wait机制（基于抢占技术）

   当事务Ti申请的数据项当前被Tj所持有，仅当Ti的时间戳大于Tj的时间戳时，允许Ti等待，否则，Tj回滚。【“年轻”的事务可以等待，“年老”的事务立即回滚】
3. 基于锁超时

   申请的事务至多等待一段给定的时间，若在此期间内未授予该事务锁，则称该事务超时，此时事务自己回滚并重启。【可能会出现“饿死”】

#### 死锁检测与恢复

**死锁检测**

等待图：边集E的每一元素是Ti->Tj，表示事务Ti在等待Tj释放所需数据项

当它存在**环**的话，就会进入**死锁**的状态（offline的方式，那么就需要知道所有事务的加锁请求）

**死锁恢复**

解除死锁的最通常做法是回滚一个或多个事务

1.选择牺牲者：决定回滚哪一些事务

2.回滚

Total rollback：回滚整个事务，重启它

Partial rollback：仅回滚必要的打破死锁的部分

3.饿死：总是被选择为牺牲者的事务可能会饿死

## 16 恢复系统

### 故障分类

- Transaction failure事务故障
- - Logical errors逻辑错误
  - System errors系统错误
- System crash系统崩溃
- Disk failure磁盘故障

### 日志记录

假设日志保存在稳定性存储器中

日志主要记录数据库的更新操作（插入，删除，更新，select操作没必要进行恢复）

将一个更新日志记录表示为`<Ti,Xj,V1,V2>`表明事务Ti对数据项Xj进行了写操作，操作前Xj的值是V1，操作后是V2



```text
<Ti start> 事务开始
<Ti commit> 事务提交
<Ti abort> 事务中止
```



### 数据库修改

#### 立即修改immediate-modification

数据库修改在事务提交commit之前发生

- 更新日志记录必须在数据库之前写
- 输出更新块到磁盘可能发生在任何时间（在事务commit之前或之后）

【很灵活，但撤销比较麻烦，有些数据存到buffer/disk，有些没存，commit之前/后故障，commit前故障，要撤销，commit后故障，重新算一遍，没被写的保留的数据要写出去】

#### 延迟修改deferred-modification

直到事务commit的临界点，才修改数据库，输出到buffer/disk

【简单，但效率低】

### 使用日志来重做和撤销事务

日志只需要记录写操作，读操作并不需要记录

#### 并发控制和恢复

所有的事务共享一个buffer和一个日志

如果事务T要对一个东西进行修改，其它事务要直到Tcommit或者abort了才能够对这个东西进行修改（加锁）

#### 取消和重做操作undo&redo

undo一个日志记录写**旧值**V1到X

redo一个日志记录写**新值**V2到X

##### 事务的取消和重做

undo是**从后往前**的，从日志的对Ti的最后一个记录开始

- 每次一个数据项被恢复到它的旧值V，一个特殊的日志记录被写出【称补偿记录compensation】
- 当事务的undo完成之后，日志记录`<Ti abort>`就被写出

redo**从前往后**，从日志对Ti的第一个记录开始

- 在这种情况下不再添加新的日志记录，没有必要添加

undo的事情是没有完成的

redo这些事情是本身已经完成了的，commit之后来了故障，可能是立即修改，可能IO并没空闲，没有被及时写道磁盘上。它已经commit了，只是相关的修改没有写到磁盘上，只能重做了。

##### 从失败中恢复

- 需要undo，如果日志：
- - 包含记录`<Ti start>`
  - 但没有`<Ti commit>`或`<Ti abort>`
- 需要redo，如果日志：
- - 包含`<Ti start>`
  - 包含`<Ti commit>`或`<Ti abort>`

### 检查点

主要是便于恢复，不用扫描整个日志。周期性往日志中加检查点。恢复时从检查点开始扫描日志即可。

检查点的执行过程如下：

1. 将当前位于主存中的所有日志记录输出到稳定存储器
2. 将所有修改的缓冲块输出到磁盘
3. 将一个日志记录`<checkpoint L>`输出到稳定存储器，其中L是执行检查点时正活跃的事务的列表。

### 恢复算法

#### 日志记录Logging（在正常操作的时候）

- `<Ti start>` 在事务开始的时候
- `<Ti,Xj,V1,V2>`对于每一个更新
- `<Ti commit>`在事务结束的时候

#### 事务回滚Transaction rollback

- 令Ti为要回滚的事务
- 从后向前扫描，对每一个这样的记录`<Ti,Xj,V1,V2>`
- - 操作undo，通过写V1到Xj
  - 写一个记录`<Ti,Xj,V1>`
  - - 这样的记录被称作弥补记录
- 一旦记录`<Ti start>`被读到，停止扫描，且写日志`<Ti abort>`

### 故障恢复

redo阶段，重放所有事务的升级，不论它们是否commit/abort/incomplete

undo阶段，重做所有的不完整的事务

### Redo phase

1. 寻找最后的`<checkpoints L>`记录，设置undo-list为L
2. 从前往后从`<checkpoints L>`记录开始扫描
3. 1. 当一个记录`<Ti, Xj, V1,V2>/<Ti,Xj,Vj>`被找到，redo它，通过写V2到Xj
   2. 当一个记录`<Ti start>`被找到，添加Ti 到undo list
   3. 当一个记录`<Ti commit>`或者`<Ti abort>`被找到，把它从undo-list中移除

### Undo phase

1. 从后往前扫描
2. 1. 当一个日志记录`<Ti, Xj, V1, V2>`被找到，且Ti在undo-list中，undo它：
   2. 1. 写V1到Xj
      2. 写日志`<Ti,Xj,V1>`
3. 1. 当日志记录`<Ti start>`被发现，且Ti在undo-list中
4. 1. 1. 写日志`<Ti abort>`
      2. 将Ti从undo-list中移除
5. 1. 当undo-list为空则停止
