<div align='center'><h1>pandas 教程 5：从 pandas 小白到 pandas 能手</h1><p><strong>作者</strong>：Rudolf Höhn&nbsp;&nbsp;&nbsp;&nbsp;<strong>原译</strong>：机器之心&nbsp;&nbsp;&nbsp;&nbsp;<strong>重译</strong>：运筹OR帷幄&nbsp;&nbsp;&nbsp;&nbsp;<strong>责编</strong>：征帆</p></div>

> 本文译自 Unit8 数据科学家 [Rudolf Höhn](https://medium.com/@rudolfhohn) 先生的文章 "[from pandas-wan to pandas-master](https://medium.com/unit8-machine-learning-publication/from-pandas-wan-to-pandas-master-4860cf0ce442)"，文章发表在博客平台 Medium 上，文章介绍了 pandas 的发展现状、内存优化、索引和方法链等内容，作者在文章中给出了许多提升程序运行性能的建议。[Unit8](https://unit8.co/) 是一家位于瑞士莫尔日，成立于 2017 年的初创公司，致力于利用大数据和人工智能技术解决各行各业问题。2019 年 5 月 21 日，公司加入[数字瑞士](https://digitalswitzerland.com/)（digitalswitzerland）组织，该组织包括 150 多家公司、学术和政府机构，其使命是将瑞士打造为全球领先的数字创新中心。

> "[from pandas-wan to pandas-master](https://medium.com/unit8-machine-learning-publication/from-pandas-wan-to-pandas-master-4860cf0ce442)" 的译文于 2019 年 8 月 15 日首发于[机器之心](https://mp.weixin.qq.com/s/8F8vvhOJgoNDtYf3qOWV9A)微信公众号，由李诗萌、张倩翻译，其译文标题为 “从小白到大师，这里有一份 pandas 入门指南”，[运筹OR帷幄](https://mp.weixin.qq.com/s/U8Y0gVt66PuVhRAPecQwsg)公众号于 2019 年 9 月 7 日转载了这篇翻译。鉴于译文中的一些错误，译文对原文部分内容的删节，以及译文对原文表格处理不当导致部分内容不可见等原因，我们参考机器之心的翻译对原文作了重译，限于水平，翻译可能还有不少问题，欢迎大家批评指正。

> 本文代码：[from_pandas-wan_to_pandas-master.ipynb](https://github.com/unit8co/medium-pandas-wan/blob/master/from_pandas-wan_to_pandas-master.ipynb)

# 目录
* [1 pandas 的定义与现状](#1-pandas-的定义与现状)
* [2 数据](#2-数据)
* [3 内存优化](#3-内存优化)
* [4 索引](#4-索引)
  + [了解更多](##了解更多)
* [5 方法链](#5-方法链)
* [6 最后的（随机给出的）小建议](#6-最后的（随机给出的）小建议)
* [7 总结](#7-总结)

# 正文

在 Unit8，我们为客户提供支持，我们利用数据资源构建有影响的高水平的机器学习模型，这些模型是商业用以产生强大影响力的合适工具。在追寻使命的漫漫征途里，我们使用了许多工具，其中之一就是 Python 库: pandas。

通过这篇文章，你将有望发现一种、两种或更多种新的使用 pandas 编写代码的方式。

这篇博文介绍 pandas 的最佳实践，它适用于所有使用 pandas 的人，无论这种使用是否频繁，它也适用于所有想要使用 pandas 的人。即便你以前从未使用过 pandas，现在开始也不迟，你说对吗？

文章将会涉及以下几个方面：

*   pandas 的发展现状
*   内存优化
*   索引
*   方法链
*   随机给出的一些小建议

在你阅读本文时，我推荐你查阅那些你看不懂的函数的帮助信息（docstrings）。做个简单的谷歌搜索以及花上几秒钟阅读 pandas 文档，将会让你的阅读更加愉快。

> 译者注：docstrings 是紧跟在 def 或 class 后的第一个字符串，这个字符串通常用来记录函数或类的帮助信息，以函数为例，这些信息可能包括函数的功能、参数的数据类型和含义、返回值的类型和含义以及使用示例等内容，这个字符串存储在对象属性 __doc__ 中，可以使用对象名.__doc__ 查看，此外也可以使用 help(对象名) 命令查看。

# 1 pandas 的定义与现状

> 那什么是 pandas ?

[pandas](https://pandas.pydata.org/) 是一个 “开放源代码，使用 BSD 许可证的库，它为 [Python](https://www.python.org/) 编程语言提供高性能、易用的数据结构和数据分析工具”（摘自 pandas 网站）。总的来说，它提供了叫做 DataFrame 和 Series 的数据抽象（[已不推荐使用 Panel](https://pandas.pydata.org/pandas-docs/stable/reference/panel.html)），它管理索引以实现数据的快速存取，它执行分析和转换运算，它甚至能（使用 matplotlib 后端）画图。

截止到本文写作，pandas 的最新发行版本为 v0.24.2.（译者注：截止到我们翻译，pandas 的最新发行版本为 v0.25.0）

<div align='center'><img src='https://www.longzf.com/assets/img/Natural_Science/Computer_Science/Python/Pandas/1.jpeg'></img></div>

是的，pandas 正走在通往 1.0 版本的道路上，而要到达那里，就不得不改变一点点人们已经习惯的用法。这里有一个非常有趣的演讲：pandas 核心贡献者 [Marc Garcia](https://datapythonista.github.io/) 的 “[走向 pandas 1.0](https://www.youtube.com/watch?v=hK6o_TDXXN8)”。

下一个版本 v0.25 的发行定在 2019 年 7 月（v0.25rc0 已于 7 月 4 日发行），它与 v1.0 有相同的代码库，但在使用即将弃用的方法时会显示警告信息（warning messages）。所以，如果你计划使用 v1.0, 那么当你运行你的 v0.25 代码库时，请务必关注所有的弃用警告（deprecation wranings）。

一句话总结，pandas v1.0 主要改善了稳定性（例如：[时间序列](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)）并且移除了未使用过的代码库（例如：SparseDataFrame）.

# 2 数据

让我们开始工作吧，我们选择的数据集是（来自 Kaggle）的玩具数据集 “[1985 到 2016 年国家自杀率](https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016)”。这个数据集虽然简单，但对于你上手 pandas 已经足够了。

在深入研究代码之前，如果你想重现结果，还需要执行这个简短的数据预处理过程，以确保你拥有正确的列名和列类型。

```python
import pandas as pd
import numpy as np
import os


# to download https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016
data_path = 'path/to/folder/'

df = (pd.read_csv(filepath_or_buffer=os.path.join(data_path, 'master.csv'))
      .rename(columns={'suicides/100k pop' : 'suicides_per_100k',
                       ' gdp_for_year ($) ' : 'gdp_year',
                       'gdp_per_capita ($)' : 'gdp_capita',
                       'country-year' : 'country_year'})
      .assign(gdp_year=lambda _df: _df['gdp_year'].str.replace(',','').astype(np.int64))
     )
```


> 小建议：如果你要读入一个大文件，请在 read_csv() 中使用参数 chunksize=N，此时函数将返回一个输出为 DataFrame 对象的迭代器

下面是数据集的部分展示：

<div align='center'>
<table>
<thead>
<tr>
<th>country</th>
<th>year</th>
<th>sex</th>
<th>age</th>
<th>suicides_no</th>
<th>population</th>
<th>suicides_per_100k</th>
<th>country_year</th>
<th>HDI for year</th>
<th>gdp_year</th>
<th>gdp_capita</th>
<th>generation</th>
</tr>
</thead>
<tbody>
<tr>
<td>Albania</td>
<td>1987</td>
<td>male</td>
<td>15-24 years</td>
<td>21</td>
<td>312900</td>
<td>6.71</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Generation X</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>male</td>
<td>35-54 years</td>
<td>16</td>
<td>308000</td>
<td>5.19</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Silent</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>female</td>
<td>15-24 years</td>
<td>14</td>
<td>289700</td>
<td>4.83</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Generation X</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>male</td>
<td>75+ years</td>
<td>1</td>
<td>21800</td>
<td>4.59</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>G.I. Generation</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>male</td>
<td>25-34 years</td>
<td>9</td>
<td>274300</td>
<td>3.28</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Boomers</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>female</td>
<td>75+ years</td>
<td>1</td>
<td>35600</td>
<td>2.81</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>G.I. Generation</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>female</td>
<td>35-54 years</td>
<td>6</td>
<td>278800</td>
<td>2.15</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Silent</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>female</td>
<td>25-34 years</td>
<td>4</td>
<td>257200</td>
<td>1.56</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Boomers</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>male</td>
<td>55-74 years</td>
<td>1</td>
<td>137500</td>
<td>0.73</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>G.I. Generation</td>
</tr>
<tr>
<td>Albania</td>
<td>1987</td>
<td>female</td>
<td>5-14 years</td>
<td>0</td>
<td>311000</td>
<td>0.0</td>
<td>Albania1987</td>
<td></td>
<td>2156624900</td>
<td>796</td>
<td>Generation X</td>
</tr>
</tbody>
</table>
</div>
```python
>>> df.columns
Index(['country', 'year', 'sex', 'age', 'suicides_no', 'population',
       'suicides_per_100k', 'country_year', 'HDI for year', 'gdp_year',
       'gdp_capita', 'generation'],
      dtype='object')
```

这里有 101 个国家，年份从 1985 到 2016，有两种性别，六个世代以及六个年龄段。使用一些简单而有用的方法，我们就可以获得这些信息。

* unique() 和 nunique() 用来获取去除了重复值的列（或去重列中的元素数目）

  ```python
  >>> df['generation'].unique()
  array(['Generation X', 'Silent', 'G.I. Generation', 'Boomers',
         'Millenials', 'Generation Z'], dtype=object)
  >>> df['country'].nunique()
  101
  ```


*   describe() 为每一个数值列输出不同的统计数字（例如：最小值，最大值，均值，个数），如果设置参数 'include=all' 则还会显示每个对象列去重后的元素个数以及顶部元素（即频率最高的元素）的个数。

<div align="center">
<table>
<thead>
<tr>
<th></th>
<th>year</th>
<th>suicides_no</th>
<th>population</th>
<th>suicides_per_100k</th>
<th>HDI for year</th>
<th>gdp_year</th>
<th>gdp_capita</th>
</tr>
</thead>
<tbody>
<tr>
<td>count</td>
<td>27820.0</td>
<td>27820.0</td>
<td>27820.0</td>
<td>27820.0</td>
<td>8364.0</td>
<td>27820.0</td>
<td>27820.0</td>
</tr>
<tr>
<td>mean</td>
<td>2001.2583752695903</td>
<td>242.57440690150972</td>
<td>1844793.6173975556</td>
<td>12.816097411933864</td>
<td>0.7766011477761837</td>
<td>445580969025.7266</td>
<td>16866.464414090584</td>
</tr>
<tr>
<td>std</td>
<td>8.46905502444141</td>
<td>902.0479168336403</td>
<td>3911779.441756363</td>
<td>18.961511014503195</td>
<td>0.09336670859029964</td>
<td>1453609985940.912</td>
<td>18887.576472205572</td>
</tr>
<tr>
<td>min</td>
<td>1985.0</td>
<td>0.0</td>
<td>278.0</td>
<td>0.0</td>
<td>0.483</td>
<td>46919625.0</td>
<td>251.0</td>
</tr>
<tr>
<td>25%</td>
<td>1995.0</td>
<td>3.0</td>
<td>97498.5</td>
<td>0.92</td>
<td>0.713</td>
<td>8985352832.0</td>
<td>3447.0</td>
</tr>
<tr>
<td>50%</td>
<td>2002.0</td>
<td>25.0</td>
<td>430150.0</td>
<td>5.99</td>
<td>0.779</td>
<td>48114688201.0</td>
<td>9372.0</td>
</tr>
<tr>
<td>75%</td>
<td>2008.0</td>
<td>131.0</td>
<td>1486143.25</td>
<td>16.62</td>
<td>0.855</td>
<td>260202429150.0</td>
<td>24874.0</td>
</tr>
<tr>
<td>max</td>
<td>2016.0</td>
<td>22338.0</td>
<td>43805214.0</td>
<td>224.97</td>
<td>0.9440000000000001</td>
<td>18120714000000.0</td>
<td>126352.0</td>
</tr>
</tbody>
</table>
</div>

*   head() 和 tail() 用来显示数据框的一小部分

使用这些方法，你将很快了解你正在分析的表格文件。

# 3 内存优化

理解数据并且为数据框的每一列选择合适的数据类型，是处理数据前的一个重要步骤。

在内部，pandas 将数据框存储为不同类型的 numpy 数组（例如：一个 float64 矩阵，一个 int32 矩阵）。

下面是大幅度降低内存消耗的两种方法：

> 译者注：实际上是一种方法，或许作者指的是这里有两个函数

```python
import pandas as pd


def mem_usage(df: pd.DataFrame) -> str:
    """This method styles the memory usage of a DataFrame to be readable as MB.
    Parameters
    ----------
    df: pd.DataFrame
        Data frame to measure.
    Returns
    -------
    str
        Complete memory usage as a string formatted for MB.
    """
    return f'{df.memory_usage(deep=True).sum() / 1024 ** 2 : 3.2f} MB'


def convert_df(df: pd.DataFrame, deep_copy: bool = True) -> pd.DataFrame:
    """Automatically converts columns that are worth stored as
    ``categorical`` dtype.
    Parameters
    ----------
    df: pd.DataFrame
        Data frame to convert.
    deep_copy: bool
        Whether or not to perform a deep copy of the original data frame.
    Returns
    -------
    pd.DataFrame
        Optimized copy of the input data frame.
    """
    return df.copy(deep=deep_copy).astype({
        col: 'category' for col in df.columns
        if df[col].nunique() / df[col].shape[0] < 0.5})
```

memory_usage() 是 pandas 自带的用来分析数据框内存消耗的方法。上面代码中，deep=True 用来确保将真实的系统消耗考虑在内。

理解列的类型是重要的，做如下两件简单的事情，你就可以减少 90 % 的内存占用：

*   搞清楚你的数据框正在使用的类型
*   搞清楚存在哪些可用类型能够降低你的数据框的内存占用（例如：如果对取值范围在 0 到 59 且只有 1 位小数的 price 列使用 float64，就可能造成不必要的开销）

除了你可能正在使用的减少数值类型大小的方式（用 int32 代替 int64），pandas 还自带有一种[分类](https://pandas.pydata.org/pandas-docs/stable/user_guide/categorical.html)（category）类型来减少内存占用。

> 如果你是一名 R 开发者，你会发现它和 factor 类型是一致的。

这种类别类型使用索引替代重复值，而将真实值存储在其他地方。一个教科书式的例子便是国家，如果要多次存储相同的字符串 “瑞士” 或者 “波兰”，为什么不简洁地用 0 和 1 替代它们并存储一个字典呢？

```python
categorical_dict = {0: 'Switzerland', 1: 'Poland'}
```

pandas 实际上就做着和这个非常类似的事情，它加入所有这些方法让类型得以使用并保证能够显示国家名称。

回到我们的方法 convert_df()，如果去重后元素个数小于原来元素个数的 50 %，该方法会把列类型自动转换为 category. 虽然这个数字可以任意选取，但由于数据框类型的转换意味着在 numpy 数组中移动数据，因此数字的选取应确保这种转换是值得的。

> 译者注：保证转换操作本身带来的开销，小于不转换相较于转换所增加的额外开销

让我们看看我们的数据发生了什么

```python
>>> mem_usage(df)
10.28 MB
>>> mem_usage(df.set_index(['country', 'year', 'sex', 'age']))
5.00 MB
>>> mem_usage(convert_df(df))
1.40 MB
>>> mem_usage(convert_df(df.set_index(['country', 'year', 'sex', 'age'])))
1.40 MB
```

通过使用我们 “机智的” 转换器，数据框的内存占用减少了几乎 10 倍（严格来说是 7.34 倍）。

# 4 索引

pandas 虽然强大，但也要付出一些代价。当你加载一个 DataFrame 时，pandas 会创建索引并在 numpy 数组内部存储数据。所以这意味着什么呢？意味着一旦加载了数据，只要索引管理得当，你就可以快速存取它们。

存取数据的方式主要有两种：索引（index）和查询（query），不同情况下你对这两种方式的选择也会不一样。但在大多数情况中，索引（和多索引）都是最佳选择。我们来看下面的例子：

> 译者注：查询是计算机科学中的术语，它是一个从数据库中获取数据的请求，我们熟知的 SQL 的英文全称就是 Structured Query Language（结构化查询语言）

```python
>>> %%time
>>> df.query('country == "Albania" and year == 1987 and sex == "male" and age == "25-34 years"')
CPU times: user 7.27 ms, sys: 751 µs, total: 8.02 ms
# ==================
>>> %%time
>>> mi_df.loc['Albania', 1987, 'male', '25-34 years']
CPU times: user 459 µs, sys: 1 µs, total: 460 µs
```

> 译者注：请在 IPython 解释器（例如安装  [jupyter](https://jupyter.org/)）下使用 %%time，CPython 解释器不支持此命令

> 什么？20 倍加速？

你可能马上会问自己，创建多索引需要花费多长时间？

```python
%%time
mi_df = df.set_index(['country', 'year', 'sex', 'age'])
CPU times: user 10.8 ms, sys: 2.2 ms, total: 13 ms
```

采用查询花费的时间是这里的 1.5 倍。如果你只需要检索一次数据（这种情况很少见），query 是合适的方法。否则，坚持使用索引吧，你的 CPU 会感谢你的。

> .set_index(drop=False) 保证不会删除作为新索引的列

当你想要查看数据框时，采用 .loc[] / .iloc[] 方法的效果非常好，但当你要修改数据框时，采用它们的效果就没那么好了。如果你需要手动（例如：使用循环）构建数据框，请考虑其他数据结构（例如：字典，列表）并在你准备好了所有数据时创建你的 DataFrame. 否则，对 DataFrame 中的每一个新行，pandas 都会更新索引，而这种更新并不是一次简单的哈希映射。

```python
>>> (pd.DataFrame({'a':range(2), 'b': range(2)}, index=['a', 'a'])
 .loc['a']
)
   a  b
a  0  0
a  1  1
```

正因如此，一个未排序的索引会降低运行效率。为了检查索引是否排序和对索引进行排序，主要采用如下两个方法。

```python
%%time
>>> mi_df.sort_index()
CPU times: user 34.8 ms, sys: 1.63 ms, total: 36.5 ms
>>> mi_df.index.is_monotonic
True
```

## 了解更多

*   [pandas 高级索引用户指南](http://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html)
*   [pandas 索引代码](https://github.com/pandas-dev/pandas/blob/master/pandas/core/indexing.py)

# 5 方法链

DataFrame 中的方法链是一种链接多种方法并返回一个数据框的行为，这些方法来自于 DataFrame 类。pandas 现在的版本中，使用方法链的原因是这样不用存储中间变量，且能避免下述情形的发生：

```python
import numpy as np
import pandas as pd


df = pd.DataFrame({'a_column': [1, -999, -999],
                    'powerless_column': [2, 3, 4],
                    'int_column': [1, 1, -1]})
df['a_column'] = df['a_column'].replace(-999, np.nan)
df['power_column'] = df['powerless_column'] ** 2
df['real_column'] = df['int_column'].astype(np.float64)
df = df.apply(lambda _df: _df.replace(4, np.nan))
df = df.dropna(how='all')
```

我们使用下面的方法链替代上述代码。

```python
df = (pd.DataFrame({'a_column': [1, -999, -999],
                    'powerless_column': [2, 3, 4],
                    'int_column': [1, 1, -1]})
        .assign(a_column=lambda _df: _df['a_column'].replace(-999, np.nan),
                power_column=lambda _df: _df['powerless_column'] ** 2,
                real_column=lambda _df: _df['int_column'].astype(np.float64))
        .apply(lambda _df: _df.replace(4, np.nan))
        .dropna(how='all')
      )
```

老实说，第二段代码要漂亮和简洁得多。

<div align='center'><img src='https://www.longzf.com/assets/img/Natural_Science/Computer_Science/Python/Pandas/2.jpeg'></img></div>

方法链的工具箱中包含许多将 DataFrame 或者 Series (或者 DataFrameGroupBy) 对象作为输出的方法（例如：apply, assign, loc, query, pipe, groupby, agg）。

理解这些方法最好的方式就是实践，让我们从一些简单的例子开始。

```python
(df
 .groupby('age')
 .agg({'generation':'unique'})
 .rename(columns={'generation':'unique_generation'})
#  Recommended from v0.25
#  .agg(unique_generation=('generation', 'unique'))
)
```

<div align='center'>获得每个年龄段世代的简单方法链</div>

<div align='center'>
<table>
<thead>
<tr>
<th>age</th>
<th>unique_generation</th>
</tr>
</thead>
<tbody>
<tr>
<td>15-24 years</td>
<td>['Generation X' 'Millenials']</td>
</tr>
<tr>
<td>25-34 years</td>
<td>['Boomers' 'Generation X' 'Millenials']</td>
</tr>
<tr>
<td>35-54 years</td>
<td>['Silent' 'Boomers' 'Generation X']</td>
</tr>
<tr>
<td>5-14 years</td>
<td>['Generation X' 'Millenials' 'Generation Z']</td>
</tr>
<tr>
<td>55-74 years</td>
<td>['G.I. Generation' 'Silent' 'Boomers']</td>
</tr>
<tr>
<td>75+ years</td>
<td>['G.I. Generation' 'Silent']</td>
</tr>
</tbody>
</table>
</div>
<div align='center'>产生数据框，age 列为索引</div>

从上表我们知道 “世代 X” 覆盖三个年龄段（译者注：作者笔误，实为 4 个），此外让我们来分解一下这条方法链。第一步按年龄段分组，这一方法返回一个 DataFrameGroupBy 对象，在这个对象中，每一组将汇总该组对应的世代标签。

尽管在这个案例中，汇总方法采用 unique，但实际上任何（匿名）函数都是可以的。

> 在最新的发行版本（v0.25）中，pandas 引入了一种[新的使用 agg 的方式](https://dev.pandas.io/whatsnew/v0.25.0.html#groupby-aggregation-with-relabeling)。

```python
(df
 .groupby(['country', 'year'])
 .agg({'suicides_per_100k': 'sum'})
 .rename(columns={'suicides_per_100k':'suicides_sum'})
#  Recommended from v0.25
#  .agg(suicides_sum=('suicides_per_100k', 'sum'))
 .sort_values('suicides_sum', ascending=False)
 .head(10)
)
```

<div align="center">使用 sort_values 和 head 获得自杀率较高的国家和年份</div>

```python
(df
 .groupby(['country', 'year'])
 .agg({'suicides_per_100k': 'sum'})
 .rename(columns={'suicides_per_100k':'suicides_sum'})
#  Recommended from v0.25
#  .agg(suicides_sum=('suicides_per_100k', 'sum'))
 .nlargest(10, columns='suicides_sum')
)
```

<div align="center">使用 nlargest 获得自杀率较高的国家和年份</div>

这两段程序的输出是相同的：拥有二水平（two level）索引的一个 DataFrame 和包含最大 10 个值的一个新列 suicides_sum.

<div align='center'>
<table>
<thead>
<tr>
<th>country</th>
<th>year</th>
<th>suicides_sum</th>
</tr>
</thead>
<tbody>
<tr>
<td>Lithuania</td>
<td>1995</td>
<td>639.3</td>
</tr>
<tr>
<td>Lithuania</td>
<td>1996</td>
<td>595.61</td>
</tr>
<tr>
<td>Hungary</td>
<td>1991</td>
<td>575.0000000000001</td>
</tr>
<tr>
<td>Lithuania</td>
<td>2000</td>
<td>571.8</td>
</tr>
<tr>
<td>Hungary</td>
<td>1992</td>
<td>570.26</td>
</tr>
<tr>
<td>Lithuania</td>
<td>2001</td>
<td>568.9799999999999</td>
</tr>
<tr>
<td>Russian Federation</td>
<td>1994</td>
<td>567.64</td>
</tr>
<tr>
<td>Lithuania</td>
<td>1998</td>
<td>566.36</td>
</tr>
<tr>
<td>Lithuania</td>
<td>1997</td>
<td>565.4400000000002</td>
</tr>
<tr>
<td>Lithuania</td>
<td>1999</td>
<td>561.5300000000001</td>
</tr>
</tbody>
</table>
</div>

列 “国家” 和 “年份” 均是索引

> nlargest(10) 比 sort_values(ascending=False).head(10) 更有效率

另一个有趣的方法是 unstack，它能旋转索引水平。

```python
(mi_df
 .loc[('Switzerland', 2000)]
 .unstack('sex')
 [['suicides_no', 'population']]
)
```

<div align='center'>
<table>
<thead>
<tr>
<th></th>
<th>suicides_no</th>
<th>suicides_no</th>
<th>population</th>
<th>population</th>
</tr>
</thead>
<tbody>
<tr>
<td>sex</td>
<td>female</td>
<td>male</td>
<td>female</td>
<td>male</td>
</tr>
<tr>
<td>age</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>15-24 years</td>
<td>20</td>
<td>79</td>
<td>410136</td>
<td>426957</td>
</tr>
<tr>
<td>25-34 years</td>
<td>47</td>
<td>147</td>
<td>537823</td>
<td>530378</td>
</tr>
<tr>
<td>35-54 years</td>
<td>124</td>
<td>360</td>
<td>1072711</td>
<td>1094229</td>
</tr>
<tr>
<td>5-14 years</td>
<td>1</td>
<td>4</td>
<td>412273</td>
<td>436831</td>
</tr>
<tr>
<td>55-74 years</td>
<td>128</td>
<td>239</td>
<td>723750</td>
<td>649009</td>
</tr>
<tr>
<td>75+ years</td>
<td>79</td>
<td>152</td>
<td>330903</td>
<td>184589</td>
</tr>
</tbody>
</table>
</div>

<div align='center'>“age” 是索引，列 “suicides_no” 和 “population” 有第二个水平列 “sex”</div>

下一个方法 pipe 是用途最广泛的方法之一，就像 shell 脚本一样，pipe 方法执行管道运算，它让方法链可以执行更丰富的运算。

pipe 的一个简单却强大的用法是用来记录不同信息。

```python
def log_head(df, head_count=10):
    print(df.head(head_count))
    return df

def log_columns(df):
    print(df.columns)
    return df

def log_shape(df):
    print(f'shape = {df.shape}')
    return df
```

<div align="center">使用管道的不同记录函数</div>

例如，我们想通过比较列 year 验证列 country_year 是否正确。

```python
(df
 .assign(valid_cy=lambda _serie: _serie.apply(
     lambda _row: re.split(r'(?=\d{4})', _row['country_year'])[1] == str(_row['year']),
     axis=1))
 .query('valid_cy == False')
 .pipe(log_shape)
)
```

<div align="center">验证列 “country_year” 的管道</div>

尽管管道的输出是一个 DataFrame，但它也打印标准输出（console / REPL）。

```python
shape = (0, 13)
```

你也可以将不同的 pipe 放到一个方法链中。

```python
(df
 .pipe(log_shape)
 .query('sex == "female"')
 .groupby(['year', 'country'])
 .agg({'suicides_per_100k':'sum'})
 .pipe(log_shape)
 .rename(columns={'suicides_per_100k':'sum_suicides_per_100k_female'})
#  Recommended from v0.25
#  .agg(sum_suicides_per_100k_female=('suicides_per_100k', 'sum'))
 .nlargest(n=10, columns=['sum_suicides_per_100k_female'])
)
```

<div align='center'>在女性中，自杀率较高的国家和年份</div>

产生的 DataFrame 如下所示：

<div align="center">
<table>
<thead>
<tr>
<th>year</th>
<th>country</th>
<th>sum_suicides_per_100k_female</th>
</tr>
</thead>
<tbody>
<tr>
<td>2009</td>
<td>Republic of Korea</td>
<td>170.89</td>
</tr>
<tr>
<td>1989</td>
<td>Singapore</td>
<td>163.16</td>
</tr>
<tr>
<td>1986</td>
<td>Singapore</td>
<td>161.67</td>
</tr>
<tr>
<td>2010</td>
<td>Republic of Korea</td>
<td>158.52</td>
</tr>
<tr>
<td>2007</td>
<td>Republic of Korea</td>
<td>149.6</td>
</tr>
<tr>
<td>2011</td>
<td>Republic of Korea</td>
<td>147.84</td>
</tr>
<tr>
<td>1991</td>
<td>Hungary</td>
<td>147.35</td>
</tr>
<tr>
<td>2008</td>
<td>Republic of Korea</td>
<td>147.04000000000002</td>
</tr>
<tr>
<td>2000</td>
<td>Aruba</td>
<td>146.22</td>
</tr>
<tr>
<td>2005</td>
<td>Republic of Korea</td>
<td>145.35</td>
</tr>
</tbody>
</table>
</div>

<div align='center'>索引是 “year” 和 “country”</div>

标准输出中的打印结果如下所示：

```python
shape = (27820, 12)
shape = (2321, 1)
```

除了向命令行解释器输出记录，我们还可以使用 pipe 直接将函数作用到数据框列上。

```python
from sklearn.preprocessing import MinMaxScaler


def norm_df(df, columns):
    return df.assign(**{col: MinMaxScaler().fit_transform(df[[col]].values.astype(float))
                        for col in columns})


for sex in ['male', 'female']:
    print(sex)
    print(
        df
        .query(f'sex == "{sex}"')
        .groupby(['country'])
        .agg({'suicides_per_100k': 'sum', 'gdp_year': 'mean'})
        .rename(columns={'suicides_per_100k':'suicides_per_100k_sum',
                         'gdp_year': 'gdp_year_mean'})
#         Recommended in v0.25
#         .agg(suicides_per_100k=('suicides_per_100k_sum', 'sum'),
#              gdp_year=('gdp_year_mean', 'mean'))
        .pipe(norm_df, columns=['suicides_per_100k_sum', 'gdp_year_mean'])
        .corr(method='spearman')
    )
    print('\n')
```

<div align='center'>自杀数的增长与 GDP 的降低有关吗？自杀数与性别相关吗？</div>

在命令行解释器中，上面的代码打印出如下结果：

```python
male
                       suicides_per_100k_sum  gdp_year_mean
suicides_per_100k_sum               1.000000       0.421218
gdp_year_mean                       0.421218       1.000000


female
                       suicides_per_100k_sum  gdp_year_mean
suicides_per_100k_sum               1.000000       0.452343
gdp_year_mean                       0.452343       1.000000
```

让我们深入研究一下代码。norm_df() 将 DataFrame 和数据框列索引构成的列表作为输入，然后使用 MinMaxScaling 对数据作标准化处理。通过使用字典生成式，norm_df() 创建了一个字典 {column_name:method, …}，字典随后被解压为 assign() 的参数 (column_name=method, …)。

> 在这个特别的例子中，最小最大标准化并不会改变相关系数的输出结果，它的引入只是为了论证 pipe 可以将函数直接作用到数据框列上 :)

(不远的？) 将来，惰性求值（lazy evaluation）将会出现在方法链中，所以在方法链上投入时间会是个很好的想法。

# 6 最后的（随机给出的）小建议

下面的小建议非常有用，但并不适合之前任何一部分。

*   itertuples() 比通过数据框行迭代要更有效率

```python
>>> %%time
>>> for row in df.iterrows(): continue
CPU times: user 1.97 s, sys: 17.3 ms, total: 1.99 s
>>> for tup in df.itertuples(): continue
CPU times: user 55.9 ms, sys: 2.85 ms, total: 58.8 ms
```

> 注意：tup 是一个 namedtuple

*   join() 使用了 merge()
*   在 Jupyter 笔记本中，在单元开始部分使用 %%time 计算运行时间是有效的
*   UInt8 数据类型支持整数 NaN
*   从现在开始记住，使用低级方法（尽可能使用 Python 的核心函数）执行密集 I/O （例如：展开大型 CSV 转储）效果更好

> 译者注：I/O 指输入/输出；dump 是计算机科学中的术语，中文译为转储，详情参考[知乎:计算机术语 dump 是什么意思？](https://www.zhihu.com/question/285731828)

下面还有一些本文没有涉及的有用的方法或数据结构，它们是值得花时间去理解的。

*   [透视表](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html#pandas.DataFrame.pivot)
*   [时间序列/日期功能](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)
*   [画图](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html)

# 7 总结

因为这篇短文，你将有望对 pandas 背后的工作原理及其发展现状有更好的理解。你了解了优化数据框内存占用的不同工具，并且知道了如何快速洞察数据。现在索引和查询已不再那么让人费解。最后，你可以尝试使用方法链写更长的链了。

这个[笔记本](https://github.com/unit8co/medium-pandas-wan)是一个支持文档，其中除了包含本文展示的所有代码，还在性能上比较了单数值索引数据框（df）和多索引数据框（mi_df）。

<div align='center'><img src='https://www.longzf.com/assets/img/Natural_Science/Computer_Science/Python/Pandas/3.jpeg' width="70%"></div>

实践出真知，持续提高你的技能并帮助我们建设一个更好的世界吧。

PS: 有时纯粹的 Numpy 实现更快（Julien Herzen;）

> 感谢 Julien Herzen，Gael Grosch 和 Kamil Zalewski.
