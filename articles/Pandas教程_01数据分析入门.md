![图片](https://uploader.shimo.im/f/hebPzvm91sYc2vIU.jpg!thumbnail)

**编者按：数据处理是数据分析的核心部分，通过爬虫或者实际生产过程中初步获取的数据通常具有很多的“垃圾数据”，比如重复数据或者值缺失，不连续数据等等。这时就需要对数据首先进行筛选，补全等“清洗”操作。**

**公众号预览摘要：数据的处理的软件包有很多，在python中主要应用Pandas来进行处理。**

**正文开始：**

数据处理是数据分析的核心部分，通过爬虫或者实际生产过程中初步获取的数据通常具有很多的“垃圾数据”，比如重复数据或者值缺失，不连续数据等等。这时就需要对数据首先进行筛选，补全等“清洗”操作。除此之外，“清洗”好的数据也需要根据不同的用途来进行转换，以适应分析，预测或者可视化的需求。

数据的处理的软件包有很多，在python中主要应用Pandas来进行处理。Pandas是一个十分成熟的数据处理包，熟练掌握可以高效并且方便地将数据进行转换和清洗，本节主要整理了pandas的一些基本技能和实用技巧，为励志成为数据分析师的你铺路搭桥。

以下是本教程的总体提纲，这篇文章首先对pandas的基本操作进行介绍，其他内容敬请期待后续的文章。另附上我征稿通知的链接：[数据科学 | 『运筹OR帷幄』数据分析、可视化、爬虫系列教程征稿](https://mp.weixin.qq.com/s?__biz=Mzg2MTA0NzA0Mw==&mid=2247488619&idx=1&sn=da90c515cb8f4d6a5a27ebf521f4bb02&chksm=ce1c4407f96bcd11b0c1289aff1d859dfa25a57250c8ea8d4968281be5e3345da4ca95f16e21&mpshare=1&scene=1&srcid=&key=579ba6bfe709a41a4575480c3eecf67f0485fab26336fb7b742eaa6e2d919e311b87e53f4fdbc1404d46a277c5feafa133134eff4c93476a19aaaabe91ac5ac9ebce58368f854b562323371f3ed475ec&ascene=1&uin=OTM2MzU5OTA3&devicetype=Windows+7&version=62060739&lang=zh_CN&pass_ticket=wAURlZr9rSekbcNMrsaFld9o9uxw3bqlxdrMWDEuuwRV3hGuJ3bKn0m5LkocueTW)

一  数据分析相关python包介绍

* 常用数据分析库NumPy, Pandas, SciPy, statssmodels, scikit-learn, NLTK的简介与安装
* 数据分析开发环境搭建

二  数据的导入与导出

* 读取csv数据
* 读取mysql数据

三  数据提取与筛选

* 常见的数据格式与形态
* Python对不同形式数据的读写

四  数据清洗处理

* 如何对数据进行清洗
* Pandas基本数据结构与功能
* Pandas统计相关功能
* Pandas缺失数据处理
* Pandas层次化索引
* Pandas DataFrame

五 高性能科学计算和数据分析的基础包Numpy

* NumPy的性能优势
* 数组对象处理
* 文件输入输出
* 线性代数相关功能
* 高效操作实践

五  统计分析

* 线性回归
* 逻辑回归
* SVM
* K紧邻算法
* 神经网络
* 机器学习库Scikit-Learn与应用
* 使用NLTK进行Python文本分析
* Python深度学习keras入门
## Pandas入门
Pandas 是基于 NumPy 的一个开源 Python 库，它被广泛用于数据分析，以及数据清洗和准备等工作。数据科学家经常和表格形式的数据（比如.csv、.tsv、.xlsx）打交道。Pandas可以使用类似SQL的方式非常方便地加载、处理、分析这些表格形式的数据。搭配Matplotlib和Seaborn效果更好。

pandas可以满足以下需求：

* 具备按轴自动或显式数据对齐功能的数据结构。这可以防止许多由于数据未对齐以及来自不同数据源（索引方式不同）的数据而导致的常见错误、集成时间序列功能、既能处理时间序列数据也能处理非时间序列数据的数据结构、数学运算和简约（比如对某个轴求和）可以根据不同的元数据（轴编号）执行、
* 灵活处理缺失数据、
* 在实际构建任何模型之前，任何机器学习项目中的大量时间都必须花费在准备数据、
* 分析基本趋势和模式上。因此需要Pandas来进行处理。

下面我们开始今天的学习之旅。

### Pandas的安装与导入
首先，在使用Pandas前，必须安装Pandas。如果你安装过Anaconda，就可以执行如下命令安装Pandas：

```
	conda install pandas
```
如果没有安装Anaconda，也没有关系，可以使用Python的pip命令来安装：
```
	pip install pandas
```
注意：pandas安装会用到numpy库，因此在安装pandas之前一定要安装好numpy。
导入：为了简便，这里使用pd作为pandas的缩写，因为pandas依赖numpy，所以在使用之前需要安装和导入numpy

```
import numpy as np
import pandas as pd
```
打印pandas的版本
```
pd.__version__
```
考虑如下的Python字典数据和Python列表标签：
```
data = {'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
        'age': [2.5, 3, 0.5, np.nan, 5, 2, 4.5, np.nan, 7, 3],
        'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}
​
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
```
### pandas数据结构介绍
	Pandas有两个数据结构：Series和DataFrame。

* 	Series是一种类似于以为NumPy数组的对象，它由一组数据（各种NumPy数据类型）和与之相关的一组数据标签（即索引）组成的。可以用index和values分别规定索引和值。如果不规定索引，会自动创建 0 到 N-1 索引。

![图片](https://uploader.shimo.im/f/LQQ819xX650Z6X8Q.png!thumbnail)

* 	DataFrame是一种表格型结构，含有一组有序的列，每一列可以是不同的数据类型。既有行索引，又有列索引。

![图片](https://uploader.shimo.im/f/dEp24H6IQCAhJRu1.png!thumbnail)

	pd.DataFrame:创建pandas矩阵

	pd.Series 创建pandas列表

	1.从具有索引标签的字典数据创建一个DataFrame df.

```
df = pd.DataFrame(data,index = labels)
```
	返回DataFrame的前三行
```
df.iloc[:3]
df.head(3)
```
运行结果如下：
**	**![图片](https://uploader.shimo.im/f/dfxNRwvm5jgfQZvL.png!thumbnail)

    2.从numpy 数组构造DataFrame

```
df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                    columns=['a', 'b', 'c'])
df2
```
运行结果如下
![图片](https://uploader.shimo.im/f/u2K8mbMOMA4HoB0S.png!thumbnail)

    3.通过其他DataFrame来创建DataFrame df3

```
df3 = df2[["a","b","c"]].copy()
df3
```
运行结果如下： 
   ![图片](https://uploader.shimo.im/f/u2K8mbMOMA4HoB0S.png!thumbnail)

   4.从csv文件中每隔n行来创建Dataframe

```
df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv', chunksize=50)
df2 = pd.DataFrame()
      
```
   ![图片](https://uploader.shimo.im/f/8V8Z9POam2oBZST9.png!thumbnail)

    5.用Series创建DataFrame

```
s_1 = pd.Series(data['animal'])
s_2 = pd.Series(data['age'])
s_3 = pd.Series(data['visits'])
s_4 = pd.Series(data['priority'])
pd_2 = pd.DataFrame([s_1,s_2,s_3,s_4])
pd_2
```
运行结果如下：
![图片](https://uploader.shimo.im/f/F267EkZFe9Ib80GF.png!thumbnail)

### **pandas处理NaN值** 
	dropna(axis=, how=)：丢弃NaN数据，{axis：0(按行丢弃)，1(按列丢弃)} {how：'any'(只要含有NaN数据就丢弃)，'all'(所有数据都为NaN时丢弃)}

	fillna(value=)：将NaN值都设置为value的值

    isnull()：对每各元素进行判断是否是NaN，返回结果矩阵

	 np.any(matrix) == value：判断matrix矩阵中是否有value值

	 np.all(matrix) == value：判断matrix矩阵中是否所有元素都是value值

### pandas读取数据、导出数据
	根据数据的格式，pandas提供了多种数据读取和导出的方法，如：

	读取数据：**read_csv、read_table、read_fwf、read_clipboard、read_excel、read_hdf**

    导出数据：to_csv、to_table、to_fwf、to_clipboard、to_excel、to_hdf

```
df = pd.read_csv('Q1.csv')
print(df)
df.to_csv('Q1_pandas.csv')
```
### pandas合并数据
**concat方法是拼接函数，有行拼接和列拼接，默认是行拼接，拼接方法默认是外拼接(并集)，拼接对象是pandas数据类型。**

第一个参数：需要合并的矩阵

axis：合并维度，0：按行合并，1：按列合并

join：处理非公有 列/行 的方式，inner：去除非公有的 列/行，outer：对非公有的 列/行 进行NaN值填充然后合并

ignore_index：是否重排行索引

```
df1 = pd.DataFrame(np.arange(12).reshape(3, 4), columns=['A', 'B', 'C', 'D'], index=[0, 1, 2])
df2 = pd.DataFrame(np.ones((3, 4)), columns=['B', 'C', 'D', 'E'], index=[1, 2, 3])
print(pd.concat([df1, df2], join='outer', ignore_index=True)) # join = {'outer', 'inner'}
print(pd.concat([df1, df2], axis=1, join_axes=[df1.index]))
print(df1.append([df2], ignore_index=True))
```
**append方法在index方向连接两个DataFrame或者对DataFrame进行扩展**

append 方法可以直接用list对DataFrame进行扩展。

```
df = pd.DataFrame([[1, 2], [3, 4]])
df = df.append([[1,2]])
print(df)
```
运行结果：
![图片](https://uploader.shimo.im/f/qqi3Sli9CSAbgKwr.png!thumbnail)

或者也可以将两个DataFrame连接起来。

```
df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
df = df.append(df2)
print(df)
```
运行结果：
![图片](https://uploader.shimo.im/f/uw5iY5MUQPssCJkv.png!thumbnail)

需要注意的是，append方法并不能像list的append方法一样对原来的df继续修改，而是建立了一个新的对象。如果要修改df，那么需要重新对df赋值，所以append的方法执行效率并不是很高。

**Join方法 是基于Index连接DataFrame，连接方法有内连接、外连接****(****左连接和****右****连接****)**

```
caller = pd.DataFrame({'key':['A0','A1','A2','A3','A4','A5'],'B':['B0','B1','B2','B3','B4','B5']})
other = pd.DataFrame({'key':['A0','A1','A2'],'C':['C0','C1','C2']})
caller.join(other,lsuffix='_caller',rsuffix='_other',how='inner')
```
运行结果如下：
![图片](https://uploader.shimo.im/f/lVd9DR4CGFsX2Axm.png!thumbnail)

**另外，还有一种merge方法与Join方法类似，不过语法略有不同。**

**通过on连接两个数据集的相同列，how表示连接的方式也有****内连接、外连接(左连接和右连接)**

使用merge方式要求合并的两个DataFrame需要有两数据集有一个相同列（不要求数值完全相同），继续以上面数据为例，对比下区别

```
df = pd.merge(caller,other,on = ['key'],how = 'inner')
```
运行结果如下：
![图片](https://uploader.shimo.im/f/NFFb7c0V9gU45zba.png!thumbnail)

**正文结束：**

**参考文献：无**

## **相关文章推荐:**
读完这篇文章是不是感觉也有一些pandas的经验想要分享？或者想要更进一步的了解一下数据挖掘算法的技能树么？详见数据分析征稿通知。

**点击****蓝字标题****，即可阅读**** **[数据科学 | 『运筹OR帷幄』数据分析、可视化、爬虫系列教程征稿通知](https://mp.weixin.qq.com/s/fHvE5V7HWwn3t5m1xKy-jg)

**其他**

数据科学|从小白走向算法工程师 [https://mp.weixin.qq.com/s/HmL0ZwEt3vvhhsvjj-GmKw](https://mp.weixin.qq.com/s/HmL0ZwEt3vvhhsvjj-GmKw)

数据科学 | 用大数据带你了解电影行业百年发展历程 [https://mp.weixin.qq.com/s/ZU2fOkYM3uVnhWzRF_FHDA](https://mp.weixin.qq.com/s/ZU2fOkYM3uVnhWzRF_FHDA)

数据科学 | 始于Jupyter Notebooks：一份全面的初学者实用指南 [https://mp.weixin.qq.com/s/QhvKxWp9xR_Ui3YHCKX3gQ](https://mp.weixin.qq.com/s/QhvKxWp9xR_Ui3YHCKX3gQ)

**责编/作者信息小卡片（小头像）：请插入自己的小卡片**

![图片](https://uploader.shimo.im/f/odZ1VMfTnBsE4k47.png!thumbnail)

**板块招聘信息：**

数据科学板块的主要关注数据科学相关的主题文章的创作和分享。主要的兴趣点包括当下热点话题的数据挖掘和分析以及数据科学所需要的基本工具和技能的科普。因此我们所创作的文章除了高质量的数据分析文章外，还包括经验分享，数据科学的研究热点和基本的数据分析基础知识的教程文章。因此，数据科学板块非常欢迎和数据有交集的各专业同学老师加入，在文章的创作中互相学习，开拓视野，获得提升。

1） 有足够的工作时间和热情（每周2-3小时），能积极参与板块内的讨论和创作活动。

2）国内外数据科学，人工智能，机器学习等专业的同学（本科或者硕士及以上），对数据科学有一定的经验或者学习热情；或者在公司从事与数据相关的工作，对数据的分析处理有一定的经验和见解。

3）对发表文章有热情，有一定的写作功底，能够利用业余时间进行创作。

关于我们：[『运筹OR帷幄』团队掠影](http://mp.weixin.qq.com/s?__biz=Mzg2MTA0NzA0Mw==&mid=2247486861&idx=1&sn=af8bc2792660d0a17c8f6364ce370d4a&scene=21#wechat_redirect)

请将简历发送至：operations_r@163.com

欢迎加入我们这个大家庭！


**作者：佘亮**

**责编：佘亮**

**审稿责编：书生，周岩**

**是否原创：是**

