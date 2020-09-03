![图片](https://uploader.shimo.im/f/LwD8GfJrNxA7SmvC.jpg!thumbnail)

# 第四章：索引、汇总和处理缺失数据

## **1. pandas 索引对象**
pandas的索引负责管理轴标签和其他如轴名称等元数据。构建Series或DataFrame时，所用到的任何数组或其他序列的标签都会被转换成一个Index。

Index对象是不可修改的（immutable），因此用户不能对其进行修改。不可修改性非常重要，因为这样才能使Index对象在多个数据结构之间安全共享。

pandas中主要的index对象

* index：最泛化得Index对象，将轴标签为一个由Python对象组成的Numpy数组
* Int64Index：针对整数的特殊Index
* MultiIndex：层次化索引对象，表示单个轴上的多层索引，可以看做由原数组组成的数组
* DatetimeIndex：存储纳秒级时间戳
* PeriodIndex：针对Period数据的特殊Index.

Index的方法和属性

* append：append连接另一个Index对象，产生一个新的Index
* diff：计算差集，并得到一个Index
* intersection：计算交集
* union：计算并集
* delete：删除索引i处的元素，并得到新的Index
* drop：删除传入的值，并得到新的索引值
* insert：将元素插入到索引a处，并得到新的Index
* unique：计算Index中唯一的数组

实例如下：

```
import numpy as np
import pandas as pd
import sys
from pandas import Series, DataFrame, Index
```
首先建立一个Series对象，这里直接对index赋值。
```
print('获取index')
obj = Series(range(3), index = ['a', 'b', 'c'])
index = obj.index
print(index[1:])
try:
    index[1] = 'd'  # index对象read only
except:
    print(sys.exc_info()[0])
print
```
或者可以用Index对象来建立index。

```
print ('使用Index对象')
index = Index(np.arange(3))
obj2 = Series([1.5, -2.5, 0], index = index)
print(obj2)
print(obj2.index is index)
print
```
![图片](https://uploader.shimo.im/f/fUCaZy2slywoSrpe.png!thumbnail)

这里用来判断列和索引是否在DataFrame中存在。

```
print('判断列和索引是否存在')
pop = {'Nevada':{20001:2.4, 2002:2.9},
        'Ohio':{2000:1.5, 2001:1.7, 2002:3.6}}
frame3 = DataFrame(pop)
print('Ohio' in frame3.columns)
print('2003' in frame3.index)
```
![图片](https://uploader.shimo.im/f/xRDNc3yUzmURIHFY.png!thumbnail)


### **1.1 重新索引**
有时我们需要重新对pandas对象进行索引赋值。

* Series的reindex将创建一个适应新索引的新对象并根据新索引进行重排。当某个索引值不存在时，引入缺失值进行填充。
* 对于序列数据（如有时间标签的数据），重新索引时可能需要做一些插值处理。其中可以用method选项即可达到此目的。

reindex函数的参数

* index：用作索引的新序列。即可以是Index实例，也可以是其他序列的python数据结构
* method：插值填充方式，ffill或bfill
* fill_value：在重新索引过程中，需要引入缺失值时使用的替代值
* limit：前向或后向填充时的最大填充量
* level：在MultiIndex的指定级别上匹配简单索引，否则选择其子集

首先是简单的用reindex方法来重新指定索引：

```
print('重新指定索引及顺序')
obj = Series([4.5, 7.2, -5.3, 3.6], index = ['d', 'b', 'a', 'c'])
print(obj)
obj2 = obj.reindex(['a', 'b', 'd', 'c', 'e'])
print(obj2)
print(obj.reindex(['a', 'b', 'd', 'c', 'e'], fill_value = 0))  # 指定不存在元素的默认值
print
```
![图片](https://uploader.shimo.im/f/8zgNMplUIuUX7qcX.png!thumbnail)

```
print('重新指定索引并指定填元素充方法')
obj3 = Series(['blue', 'purple', 'yellow'], index = [0, 2, 4])
print(obj3)
print(obj3.reindex(range(6), method = 'ffill'))
print
```
![图片](https://uploader.shimo.im/f/JXiDrfjMrbsCGPVT.png!thumbnail)

```
print('对DataFrame重新指定索引')
frame = DataFrame(np.arange(9).reshape(3, 3),
                  index = ['a', 'c', 'd'],
                  columns = ['Ohio', 'Texas', 'California'])
print(frame)
frame2 = frame.reindex(['a', 'b', 'c', 'd'])
print(frame2)
print
```
![图片](https://uploader.shimo.im/f/AEEA17r9XsEQpsXz.png!thumbnail)

```
print('重新指定column')
states = ['Texas', 'Utah', 'California']
print(frame.reindex(columns = states))
print
```
![图片](https://uploader.shimo.im/f/DnLNkpWGpGQSM8SF.png!thumbnail)

### **1.2 丢弃指定索引** 

删除某一列或者行上的一个或多个项很容易，只需要这些数据的索引组成的数组或列表即可。由于需要执行一些数据整理和集合逻辑，所以drop方法返回的是一个在指定轴上删除了指定值的新对象：

```
print('Series根据索引删除元素')
obj = Series(np.arange(5.), index = ['a', 'b', 'c', 'd', 'e'])
new_obj = obj.drop('c')
print(new_obj)
print(obj.drop(['d', 'c']))
```
![图片](https://uploader.shimo.im/f/h58qi8JyJxI4VMiy.png!thumbnail)

```
print('DataFrame删除元素，可指定索引或列。')
data = DataFrame(np.arange(16).reshape((4, 4)),
                  index = ['Ohio', 'Colorado', 'Utah', 'New York'],
                  columns = ['one', 'two', 'three', 'four'])
print(data)
print(data.drop(['Colorado', 'Ohio']))
print(data.drop('two', axis = 1))
print(data.drop(['two', 'four'], axis = 1))
```
![图片](https://uploader.shimo.im/f/hDzgIs077cIsbQkl.png!thumbnail)

### **1.3 索引、选取和过滤**
*  Series索引的工作方式和NumPy数组的索引相似，只是Series的索引值不只是整数。
*  利用标签的切片运算与普通的Python切片运算不同，其末端是包含的（inclusive）。
*  对DataFrame进行索引其实就是获取一个或多个列
*  为了在DataFrame的行上进行标签索引，引入了专门的索引字段ix。

DataFrame的索引选项

* obj[val]：选取DataFrame的单个列或一组列。
* obj.ix[val]：选取DataFrame的单个行或一组行
```
print('Series的索引，默认数字索引可以工作。')
obj = Series(np.arange(4.), index = ['a', 'b', 'c', 'd'])
print(obj['b'])
print(obj[3])
print(obj[[1, 3]])
print(obj[obj < 2])
```
![图片](https://uploader.shimo.im/f/FL3rglK6NGAa9Y3o.png!thumbnail)

```
print('Series的数组切片')
print(obj['b':'c'])  # 闭区间
obj['b':'c'] = 5
print(obj)
```
![图片](https://uploader.shimo.im/f/4IDXlZvwBh0jqLJL.png!thumbnail)

```
print('DataFrame的索引')
data = DataFrame(np.arange(16).reshape((4, 4)),
                  index = ['Ohio', 'Colorado', 'Utah', 'New York'],
                  columns = ['one', 'two', 'three', 'four'])
print(data)
print(data['two']) # 打印列
print(data[['three', 'one']])
print(data[:2])
print(data.ix['Colorado', ['two', 'three']]) # 指定索引和列
print(data.ix[['Colorado', 'Utah'], [3, 0, 1]])
print(data.ix[2])  # 打印第2行（从0开始）
print(data.ix[:'Utah', 'two']) # 从开始到Utah，第2列
```
![图片](https://uploader.shimo.im/f/N4EdagRImpont3rj.png!thumbnail)

```
print('根据条件选择')
print(data[data.three > 5])
print(data < 5)  # 打印True或者False
data[data < 5] = 0
print(data)
```
![图片](https://uploader.shimo.im/f/XoFxNj8pxYYLGmEH.png!thumbnail)

### **1.4 算术运算和数据对齐**
* 对不同的索引对象进行算术运算
* 自动数据对齐在不重叠的索引处引入了NA值，缺失值会在算术运算过程中传播。
* 对于DataFrame，对齐操作会同时发生在行和列上。
* fill_value参数
* DataFrame和Series之间的运算
```
print('加法')
s1 = Series([7.3, -2.5, 3.4, 1.5], index = ['a', 'c', 'd', 'e'])
s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index = ['a', 'c', 'e', 'f', 'g'])
print(s1)
print(s2)
print(s1 + s2)
```
![图片](https://uploader.shimo.im/f/6oIE7FknFiUXq1IC.png!thumbnail)

```
print('DataFrame加法，索引和列都必须匹配。')
df1 = DataFrame(np.arange(9.).reshape((3, 3)),
                columns = list('bcd'),
                index = ['Ohio', 'Texas', 'Colorado'])
df2 = DataFrame(np.arange(12).reshape((4, 3)),
                columns = list('bde'),
                index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
print(df1)
print(df2)
print(df1 + df2)
```
![图片](https://uploader.shimo.im/f/QakYejVpqKEmbolk.png!thumbnail)

```
print('数据填充')
df1 = DataFrame(np.arange(12.).reshape((3, 4)), columns = list('abcd'))
df2 = DataFrame(np.arange(20.).reshape((4, 5)), columns = list('abcde'))
print(df1)
print(df2)
print(df1.add(df2, fill_value = 0))
print(df1.reindex(columns = df2.columns, fill_value = 0))
```
![图片](https://uploader.shimo.im/f/Q8TTmFodDZ80uOxD.png!thumbnail)

```
print('DataFrame与Series之间的操作')
arr = np.arange(12.).reshape((3, 4))
print(arr)
print(arr[0])
print(arr - arr[0])
frame = DataFrame(np.arange(12).reshape((4, 3)),
                  columns = list('bde'),
                  index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
series = frame.iloc[0]
print(frame)
print(series)
print(frame - series)
series2 = Series(range(3), index = list('bef'))
print(frame + series2)
series3 = frame['d']
print(frame.sub(series3, axis = 0))  # 按列减
```
![图片](https://uploader.shimo.im/f/cM1K5Y8R8AMQdQyF.png!thumbnail)

### **1.5 函数应用和映射**
* numpy的ufuncs（元素级数组方法）
* DataFrame的apply方法
* 对象的applymap方法（因为Series有一个应用于元素级的map方法）
```
print('函数')
frame = DataFrame(np.random.randn(4, 3),
                  columns = list('bde'),
                  index = ['Utah', 'Ohio', 'Texas', 'Oregon'])
print(frame)
print(np.abs(frame))
```
![图片](https://uploader.shimo.im/f/4qew4KZXpa4kSKTn.png!thumbnail)

```
print('lambda以及应用')
f = lambda x: x.max() - x.min()
print(frame.apply(f))
print(frame.apply(f, axis = 1))
def f(x):
    return Series([x.min(), x.max()], index = ['min', 'max'])
print(frame.apply(f))
```
![图片](https://uploader.shimo.im/f/xhgOFIhYHxMVHy4k.png!thumbnail)

```
print('applymap和map')
_format = lambda x: '%.2f' % x
print(frame.applymap(_format))
print(frame['e'].map(_format))
```
![图片](https://uploader.shimo.im/f/B5BXsb8Z31YnipbP.png!thumbnail)

### **1.6 排序和排名**
* 对行或列索引进行排序
* 对于DataFrame，根据任意一个轴上的索引进行排序
* 可以指定升序降序
* 按值排序
* 对于DataFrame，可以指定按值排序的列
* rank函数
```
print('根据索引排序，对于DataFrame可以指定轴。')
obj = Series(range(4), index = ['d', 'a', 'b', 'c'])
print(obj.sort_index())
frame = DataFrame(np.arange(8).reshape((2, 4)),
                  index = ['three', 'one'],
                  columns = list('dabc'))
print(frame.sort_index())
print(frame.sort_index(axis = 1))
print(frame.sort_index(axis = 1, ascending = False)) # 降序
```
![图片](https://uploader.shimo.im/f/JsRajwzNbpEtEUEV.png!thumbnail)

```
print('根据值排序')
obj = Series([4, 7, -3, 2])
print(obj.sort_values()) # order已淘汰
```
![图片](https://uploader.shimo.im/f/xz4usVr3z5kMFHFP.png!thumbnail)

```
print('DataFrame指定列排序')
frame = DataFrame({'b':[4, 7, -3, 2], 'a':[0, 1, 0, 1]})
print(frame)
print(frame.sort_values(by = 'b')) # sort_index(by = ...)已淘汰
print(frame.sort_values(by = ['a', 'b']))
```
![图片](https://uploader.shimo.im/f/vSM3VOa5yWMKZxhW.png!thumbnail)

```
print('rank，求排名的平均位置(从1开始)')
obj = Series([7, -5, 7, 4, 2, 0, 4])
# 对应排名：-5(1), 0(2), 2(3), 4(4), 4(5), 7(6), 7(7)
print(obj.rank())
print(obj.rank(method = 'first'))  # 去第一次出现，不求平均值。
print(obj.rank(ascending = False, method = 'max')) # 逆序，并取最大值。所以-5的rank是7.
frame = DataFrame({'b':[4.3, 7, -3, 2],
                  'a':[0, 1, 0, 1],
                  'c':[-2, 5, 8, -2.5]})
print(frame)
```
![图片](https://uploader.shimo.im/f/8wnT2k7mW2wnt4HV.png!thumbnail)

### **1.7 带有重复值的索引**
* 对于重复索引，返回Series，对应单个值的索引则返回标量。
```
print('重复的索引')
obj = Series(range(5), index = ['a', 'a', 'b', 'b', 'c'])
print(obj.index.is_unique) # 判断是非有重复索引
#print(obj['a'][0])
#print(obj.a[1])
df = DataFrame(np.random.randn(4, 3), index = ['a', 'a', 'b', 'b'])
print(df)
print(df.ix['b'].ix[0])
print(df.ix['b'].ix[1])
```
![图片](https://uploader.shimo.im/f/Bj1ebTOeHGMkWjLA.png!thumbnail)

## **2. 汇总和计算描述统计**
* 常用方法选项
    * axis：指定轴，DataFrame的行用0，列用1
    * skipna：排除缺失值，默认值为True
    * level：如果轴是层次化索引的，则根据level选取分组

* Pandas 常用描述和汇总统计函数
    * count：非NA值得数量
    * describe：针对Series或者各DataFrame列计算汇总统计
    * min,max：计算最小值和最大值
    * argmin,argmax：计算能够获取到的最小值和最大值的索引位置
    * idxmin,idxmax：计算能够获取到的最小值和最大值的索引值
    * sum：值的总和
    * mean：值的平均数
    * median：值得算术中位数
    * mad：根据平均值计算平均绝对离差

* 数值型和非数值型的区别: 

* NA值被自动排查，除非通过skipna选项
```
print('求和')
df = DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
              index = ['a', 'b', 'c', 'd'],
              columns = ['one', 'two'])
print(df)
print(df.sum())  # 按列求和
print(df.sum(axis = 1))  # 按行求和
```
![图片](https://uploader.shimo.im/f/deDp9s510U4FXVWc.png!thumbnail)

```
print('平均数')
print(df.mean(axis = 1, skipna = False))
print(df.mean(axis = 1))
```
![图片](https://uploader.shimo.im/f/cAI1lIcVWDwE7Rcq.png!thumbnail)

```
print('其它')
print(df.idxmax())
print(df.cumsum())
print(df.describe())
obj = Series(['a', 'a', 'b', 'c'] * 4)
print(obj.describe())
```
![图片](https://uploader.shimo.im/f/jo3jyQHMkuAKgi8g.png!thumbnail)

### **2.1 相关系数与协方差**
* 相关系数：相关系数是用以反映变量之间相关关系密切程度的统计指标。（百度百科）
* 协方差：从直观上来看，协方差表示的是两个变量总体误差的期望。如果两个变量的变化趋势一致，也就是说如果其中一个大于自身的期望值时另外一个也大于自身的期望值，那么两个变量之间的协方差就是正值；如果两个变量的变化趋势相反，即其中一个变量大于自身的期望值时另外一个却小于自身的期望值，那么两个变量之间的协方差就是负值。


### **2.2 唯一值以及成员资格**
常用方法:
* is_in：计算一个表示Series各值是否包含于传入的值序列中的布尔型数组
* unique：计算Series中唯一值数组，按发现的顺序返回
* value_counts：返回一个Series，其索引为唯一值，其值为频率，按计算数值降序排列

```
print('去重')
obj = Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
print(obj.unique())
print(obj.value_counts())
```
![图片](https://uploader.shimo.im/f/azKectt5lkwry33b.png!thumbnail)

```
print('判断元素存在')
mask = obj.isin(['b', 'c'])
print(mask)
print(obj[mask]) #只打印元素b和c
data = DataFrame({'Qu1':[1, 3, 4, 3, 4],
                  'Qu2':[2, 3, 1, 2, 3],
                  'Qu3':[1, 5, 2, 4, 4]})
print(data)
print(data.apply(pd.value_counts).fillna(0))
print(data.apply(pd.value_counts, axis = 1).fillna(0))
```
![图片](https://uploader.shimo.im/f/H6xsNdNgvWo2TvWE.png!thumbnail)

## **3. 处理缺失数据**
* NA处理方法
  *  dropna：根据各标签的值中是否存在缺少数据du
  *  fillba：样本值的标准差
  *  isnull：样本值的偏度
* NaN（Not a Number）表示浮点数和非浮点数组中的缺失数据
* None也被当作NA处理
```
print('作为null处理的值')
string_data = Series(['aardvark', 'artichoke', np.nan, 'avocado'])
print(string_data)
print(string_data.isnull())
string_data[0] = None
print(string_data.isnull())
```
![图片](https://uploader.shimo.im/f/BRH6NlhWJuMNmqag.png!thumbnail)

### **3.1 滤除缺失数据**
* dropna
* 布尔索引
* DatFrame默认丢弃任何含有缺失值的行
* how参数控制行为，axis参数选择轴，thresh参数控制留下的数量
```
print('丢弃NA')
data = Series([1, np.nan, 3.5, np.nan, 7])
print(data.dropna())
print(data[data.notnull()])
print
```
![图片](https://uploader.shimo.im/f/RtaJU9bKPjA2SCGg.png!thumbnail)

```
print('DataFrame对丢弃NA的处理')
data = DataFrame([[1., 6.5, 3.], [1., np.nan, np.nan],
                  [np.nan, np.nan, np.nan], [np.nan, 6.5, 3.]])
print(data.dropna()) # 默认只要某行有NA就全部删除
print(data.dropna(how = 'all'))  # 全部为NA才删除
data[4] = np.nan  # 新增一列
print(data.dropna(axis = 1, how = 'all'))
data = DataFrame(np.random.randn(7, 3))
data.iloc[:4, 1] = np.nan
data.iloc[:2, 2] = np.nan
print(data)
print(data.dropna(thresh = 2)) # 每行至少要有2个非NA元素
```
![图片](https://uploader.shimo.im/f/vpEZ3lV0IdE5pGw5.png!thumbnail)

### **3.2 填充缺失数据**
* fillna
* inplace参数控制返回新对象还是就地修改
```
print('填充0')
df = DataFrame(np.random.randn(7, 3))
df.iloc[:4, 1] = np.nan
df.iloc[:2, 2] = np.nan
print(df.fillna(0))
df.fillna(0, inplace = True)
print(df)
```
![图片](https://uploader.shimo.im/f/valloBw77eYuLULC.png!thumbnail)

```
print('不同行列填充不同的值')
print(df.fillna({1:0.5, 3:-1}))  # 第3列不存在
```
![图片](https://uploader.shimo.im/f/DKAu9MyN6uoNstnN.png!thumbnail)

```
print('不同的填充方式')
df = DataFrame(np.random.randn(6, 3))
df.iloc[2:, 1] = np.nan
df.iloc[4:, 2] = np.nan
print(df)
print(df.fillna(method = 'ffill'))
print(df.fillna(method = 'ffill', limit = 2))
```
![图片](https://uploader.shimo.im/f/Z3DSekihsxEnKRCa.png!thumbnail)

```
print('用统计数据填充')
data = Series([1., np.nan, 3.5, np.nan, 7])
print(data.fillna(data.mean()))
```
![图片](https://uploader.shimo.im/f/Og3rlZHXsVghrxh6.png!thumbnail)

## **4. 层次化索引**
* 使你能在一个轴上拥有多个（两个以上）索引级别。抽象的说，它使你能以低纬度形式处理高维度数据。
* 通过stack与unstack变换DataFrame
```
print('Series的层次索引')
data = Series(np.random.randn(10),
              index = [['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
                       [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
print(data)
print(data.index)
print(data.b)
print(data['b':'c'])
print(data[:2])
print(data.unstack())
print(data.unstack().stack())
```
![图片](https://uploader.shimo.im/f/nkoqt0nPFIkaJxtG.png!thumbnail)

```
print('DataFrame的层次索引')
frame = DataFrame(np.arange(12).reshape((4, 3)),
                  index = [['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                  columns = [['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
print(frame)
frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
print(frame)
print(frame.loc['a', 1])
print(frame.loc['a', 2]['Colorado'])
print(frame.loc['a', 2]['Ohio']['Red'])
```
![图片](https://uploader.shimo.im/f/h9qxgnYzzgk6Qdr5.png!thumbnail)

```
print('直接用MultiIndex创建层次索引结构')
print(MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Gree', 'Red', 'Green']],
                             names = ['state', 'color'])
                             )
```
![图片](https://uploader.shimo.im/f/kIbwj16C4b45nPl0.png!thumbnail)

### **4.1 重新分级顺序**
* 索引交换
* 索引重新排序
```
print('索引层级交换')
frame = DataFrame(np.arange(12).reshape((4, 3)),
                  index = [['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                  columns = [['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
frame.index.names = ['key1', 'key2']
frame_swapped = frame.swaplevel('key1', 'key2')
print(frame_swapped)
print(frame_swapped.swaplevel(0, 1))
```
![图片](https://uploader.shimo.im/f/sP8EBNtwz88ZL2ED.png!thumbnail)

### **4.2 根据级别汇总统计**
* 指定索引级别和轴
```
print('根据指定的key计算统计信息')
frame = DataFrame(np.arange(12).reshape((4, 3)),
                  index = [['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                  columns = [['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
frame.index.names = ['key1', 'key2']
print(frame)
print(frame.sum(level = 'key2'))
```
![图片](https://uploader.shimo.im/f/51au0IweyRwEjtcQ.png!thumbnail)

### **4.3 使用DataFrame的列**
* 将指定列变为索引
* 移除或保留对象
* reset_index恢复
```
print('使用列生成层次索引')
frame = DataFrame({'a':range(7),
                   'b':range(7, 0, -1),
                   'c':['one', 'one', 'one', 'two', 'two', 'two', 'two'],
                   'd':[0, 1, 2, 0, 1, 2, 3]})
print(frame)
print(frame.set_index(['c', 'd']))  # 把c/d列变成索引
print(frame.set_index(['c', 'd'], drop = False)) # 列依然保留
frame2 = frame.set_index(['c', 'd'])
print(frame2.reset_index())
```
![图片](https://uploader.shimo.im/f/im3Hzd9VFw8Endhv.png!thumbnail)

### **4.4 整数索引**
* 歧义的产生
* 可靠的，不考虑索引类型的，基于位置的索引。
```
print('整数索引')
ser = Series(np.arange(3.))
print(ser)
try:
    print(ser[-1]) # 这里会有歧义
except:
    print(sys.exc_info()[0])
ser2 = Series(np.arange(3.), index = ['a', 'b', 'c'])
print(ser2[-1])
ser3 = Series(range(3), index = [-5, 1, 3])
print(ser3.iloc[2])  # 避免直接用[2]产生的歧义
```
![图片](https://uploader.shimo.im/f/oFoOp4qWof4ao2V9.png!thumbnail)

```
print('对DataFrame使用整数索引')
frame = DataFrame(np.arange(6).reshape((3, 2)), index = [2, 0, 1])
print(frame)
print(frame.iloc[0])
print(frame.iloc[:, 1])
```
![图片](https://uploader.shimo.im/f/cACa4c3zIlEnTjgv.png!thumbnail)

### **4.5 面板(Pannel)数据**
通过三维ndarray创建pannel对象

* 通过ix[...]选取需要的数据
* 访问顺序：item -> major -> minor
* 通过stack展现面板数据
```
data = np.random.rand(2,4,5)
p = pd.Panel(data)
print(p)
```



**参考文献：**

* pandas toolkit
* pandas官方文档：[https://pandas.pydata.org/pandas-docs/stable/index.html](https://pandas.pydata.org/pandas-docs/stable/index.html)

**作者：**Paul

**责编：**Paul，周岩

