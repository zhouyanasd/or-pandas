<div align='center'>
<h1><strong>pandas 实例 3：熊猫爱上篮球，pandas 造福世界</strong></h1>
<p><strong>作者</strong>：征帆&nbsp;&nbsp;&nbsp;&nbsp;<strong>责编</strong>：征帆，邢昱&nbsp;&nbsp;&nbsp;&nbsp;<strong>审稿责编</strong>：书生，周岩</p>
</div>

<br>

11 年前，怀着激动的心情，我跟随着爸爸妈妈来到了新家。第一次住上过百平的房子，第一次有了自己的独立房间，第一次体验宽敞明亮的书房。那一年，对我来说，很特殊；那一年，对我们国家来说，更是如此。

08 年的中国，写满着苦难与辉煌。1 月，中国南方遭遇数十年未遇的雪灾，数 10 万房屋倒塌，直接经济损失 1500 多亿；5 月，汶川发生新中国历史上破坏力最大的地震，全国仅 3 省没有震感，近 7 万鲜活生命离我们远去；8 月，第 29 届夏季奥林匹克运动会在北京成功举办，中国以 51 枚金牌的成绩首次登顶奥运会奖牌榜；9 月，神舟七号载人飞船发射升空，翟志刚走出舱门，迈出中国人在太空的第一步。

<div align='center'>
<img src="https://uploader.shimo.im/f/1dX1uMCMn4kTTrmd.jpeg!thumbnail" width="70%"></img><br><br>
<img src="https://uploader.shimo.im/f/6MYbT25L7FUQAs3S.jpeg!thumbnail" width="70%"></img>
</div>

<br>

下面这张照片，是那一年，我为自己房间选择的床头灯。一只卡通熊猫，咬着一根竹子，怀抱一个篮球，篮球上倒写着三个字母：NBA.  熟悉篮球的朋友都知道， NBA 全称 National Basketball Association（国家篮球协会），是美国的职业篮球联赛。曾经有段时间央视要求改称 NBA 为美职篮，后来应该是取消了这个规定，现在比赛解说叫的都是 NBA。

<br>

<div align='center'>
<img src="https://uploader.shimo.im/f/8YO2d8xZmWM4i4Vv.jpg!thumbnail" width="70%"></img>
</div>

<br>

一个多月前，央视停止转播 NBA 比赛，这一切缘于火箭队总经理莫雷发表的关于香港问题的不当言论。莫雷的言论，加上总裁肖华的补刀，彻底激怒了中国人民，NBA 走向舆论的风口浪尖，一时成为众矢之的。NBA 与中国关系的上空，依然乌云密布，何时散去尚未可知。但我希望，也相信，万里晴空终会到来。

美国，作为篮球运动的诞生地，它的职业联赛，依旧代表着世界篮球发展的最高水平。在 [NBA 官方统计网站](http:// https://stat.nba.com) 上，不仅提供了大量的汇总数据，而且提供了大量的原始数据。在那里，我们可以找到每个球员的详细个人信息，可以找到每场比赛的详细过程，也可以找到每个球员每次出手的文字与视频记录。当拿着中国职业篮球联赛（CBA）的统计网站和 NBA 对比一下，你能感受到，那扑面而来的差距。

选择这款床头灯的初衷并非因为篮球，仅仅因为它是当时店里面唯一的卡通灯饰。那个时候，我仍然害怕有身体对抗的球类运动，尤其害怕篮球，害怕一不小心砸到脑袋。但这种害怕我是不敢说的，担心被人笑话，笑话一个男孩子这都怕，阳刚之气何在。

两年后，一个清晨，初升的太阳，朗朗的书声，清扫着周遭的寒气。教学楼后罚球线上，刚上高一的我，拿着还不怎么会拍的球，投进了人生中的第一个空心。清脆刷网声响起的那一刻，篮球，在我心中，完成了角色的反转。那天夜晚，躺在床上，望着熊猫和他怀抱的篮球，心中满是欢喜与感激。

后来，家里搬去了另一个城市，那座房子也已多年不住，但熊猫与篮球的故事，并未因此结束。

世界无比美妙，她总有这样那样的戏剧性。多年以前的那个夜晚，我不会想到，今天，在我的第一篇公众号文章里，我会选择篮球这个主题，也不会想到，我所用来分析 NBA 球员投篮数据的工具之一 pandas，翻译成中文，就是熊猫。

```python
# 导入所有需要的模块

# 用于数据获取、预处理与分析

import requests
import json
import os

import re
from sklearn import svm

import numpy as np
import pandas as pd

# 用于绘图

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle, Polygon

import pyecharts.options as opts
from pyecharts.faker import Faker
from pyecharts.charts import Line
```

## 1 数据获取
在微信公众号 “法纳斯特” 的文章 [NBA 球员投篮数据可视化](https://mp.weixin.qq.com/s/Qevx7ijb-ymn1YGpBw51Sw) 中，我找到了获取一个 NBA 球员投篮数据的页面地址（URL）。该 URL 的方案（scheme）、主机（host）、路径（path）部分为 https://stats.nba.com/stats/shotchartdetail? ，其查询（query）部分涉及 19 个参数，包括赛季类型（SeasonType）、球员 ID（PlayerID）等。你可能会问方案、主机、路径、查询是什么意思，看看简书的这篇博客 “[快速搞懂URL的构成](https://www.jianshu.com/p/406d19dfabd3)” 或者我的这篇博客 “[计算机科学导论(5):计算机网络](https://www.longzf.com/CS_intro/5/)” 中关于 HTTP 协议的部分，你就知道了。

为了获取全部球员的投篮数据，我需要全部球员的 ID 信息，上哪里找呢？万能的 Github 上，一个名为 [nba_py](https://github.com/seemethere/nba_py) 的项目，为我提供了答案。在这个项目的[文档](https://github.com/seemethere/nba_py/wiki/stats.nba.com-Endpoint-Documentation)中，提供了获取全部球员 ID 信息的 URL。该 URL 的方案、主机、路径部分为 https://stats.nba.com/stats/commonallplayers? ，其查询部分涉及 3 个参数：LeagueID、Season 和 IsOnlyCurrentSeason。这个文档中还提供了许多 URL，不过并没有说明通过请求这些 URL 可以获得什么数据，以后有时间再慢慢研究吧。

至此，获取 NBA 所有球员投篮数据的途径就有了。这份数据的获取，包含上千次网络请求，其中第一次请求获取球员 ID 信息，后面的请求获取所有球员常规赛的详细投篮数据，不同球员对应的 URL 不同，有多少名球员，就有多少次请求。在我的个人电脑上，整个数据的获取花费了近 5 个小时，最终获得的数据量为 400 多万条，文件大小近 900 M。代码如下:

``` python
# 获取球员 ID 信息
url     = 'https://stats.nba.com/stats/commonallplayers?'
params  = {'LeagueID':            '00',
           'Season':              '2019',
           'IsOnlyCurrentSeason': 0}
headers = {'User-Agent':         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/77.0.3865.90 Safari/537.36',
           'Referer':            'https://stats.nba.com/',
           'Accept':             'application/json, text/plain, */*',
           'Accept-Encoding':    'gzip, deflate, br',
           'Accept-Language':    'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
           'Connection':         'keep-alive',
           'Host':               'stats.nba.com',
           'Sec-Fetch-Dest':     'empty',
           'Sec-Fetch-Mode':     'cors',
           'Sec-Fetch-Site':     'same-origin',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token':  'true'}
try:
    idInfo = (requests.get(url, params=params, headers=headers)
                      .json()["resultSets"][0]
             )
except Exception as e:
    print("\n错误：球员 ID 信息获取失败，请确认网络连接正常后重启程序！")
    exit()
else:
    idInfo       = pd.DataFrame(idInfo['rowSet'], 
                                columns=idInfo['headers'])
    playerIDList = idInfo['PERSON_ID'].tolist()
    print('\n成功：球员 ID 信息获取成功\n')


# 获取球员常规赛投篮数据
shotDF, errorList, emptyList = pd.DataFrame(), [], []
# 若要获取所有球员数据，清修改 playerIDList[0:50] 为 playerIDList
for i, playerID in enumerate(playerIDList[0:50]):
    url = 'https://stats.nba.com/stats/shotchartdetail?'
    params = {'SeasonType':     'Regular Season',
              'TeamID':         0,
              'PlayerID':       playerID,
              'PlayerPosition': '',
              'GameID':         '',
              'Outcome':        '',
              'Location':       '',
              'Month':          0,
              'SeasonSegment':  '',
              'DateFrom':       '',
              'DateTo':         '',
              'OpponentTeamID': 0,
              'VsConference':   '',
              'VsDivision':     '',
              'RookieYear':     '',
              'GameSegment':    '',
              'Period':         0,
              'LastNGames':     0,
              'ContextMeasure': 'FGA'}
    try:
        shotDFSec = (requests.get(url, params=params,                             
                                  headers=headers)
                             .json()["resultSets"][0]
                    )
    except Exception:
        errorList.append(playerID)
        print('错误：第{0}个球员（ID:{1}）数据获取失败'
              .format(i + 1, playerID))
    else:
        print('成功：第{0}个球员（ID:{1}）数据获取成功'
              .format(i + 1, playerID))
        if shotDFSec["rowSet"] != []:
            shotDFSec = pd.DataFrame(
                shotDFSec["rowSet"],
                columns=shotDFSec["headers"])
            shotDF = shotDF.append(shotDFSec)
        else:
            emptyList.append(playerID)
            print('警告：第{0}个球员（ID:{1}）数据为空'
                  .format(i + 1, playerID))

if emptyList != []:
    print('警告：以下球员 ID 数据为空\n{0}\n'
          .format(emptyList))

if errorList != []:
    print('错误：以下球员 ID 数据获取失败\n{0}\n'
          .format(errorList))


# 将数据保存到外部文件
# os.getcwd() 用于获取当前工作目录，cwd 是 current work directory 的简称
shotDF.to_csv('shotInfo.csv')
print('数据已输出到外部文件：', os.getcwd() + '/shotInfo.csv')
```

熊猫先森等待数据的 5 个小时里，万分焦急，他数次拿起电话筒，呼叫又会唱跳，又会 rap，又会篮球的坤坤，约他出来打球，坤坤的回复总是寥寥四字，简洁明了。熊猫先森强忍着内心的愤怒，决定分析完他的投篮数据后，再找坤坤算笔总账，熊猫先森心里嘀咕：“不是不报，时候未到。”


<div align='center'>
<img src="https://uploader.shimo.im/f/FFILGqPzEbg7KWon.gif" width="35%"></img>
<img src="https://uploader.shimo.im/f/CzZnLdDbUHQUCix8.jpg!thumbnail" width="35%"></img>
</div>


## 2 数据概览
在代码中，我将这份数据命名为 shotDF，DF 是 pandas 提供的数据结构 DataFrame 的缩写。非常感谢 Unit8 数据科学家 Rudolf Höhn 先生发表在博客平台 Medium 的文章 "From Pandas-wan to Pandas-master"，我在这份数据的处理上用到了先生在这篇文章中自定义的 convert_df 函数，在对 shotDF 应用该函数后，其内存消耗由 3643 M 骤降至 134 M。

仔细看看 convert_df 函数，其实它只做了一件事情：那就是当某列去重后元素个数小于原来元素个数的 50 % 时，转换列类型为 category。老子爷爷的《道德经》说得好：万物之始，大道至简，衍化至繁。

```Python
def convert_df(df):
    dic = {col: 'category' for col in df.columns
           if df[col].nunique() / df[col].shape[0] < 0.5}
    return df.astype(dic)
```

<div align='center'>
<img src="https://uploader.shimo.im/f/UAfRURti4U0hbEaL.jpg!thumbnail" width="35%"></img>
<img src="https://uploader.shimo.im/f/3slxIrM3s6whlBqN.jpg!thumbnail" width="35%"></img>
<img src="https://uploader.shimo.im/f/54R6VPq4y0ID6Mzx.jpg!thumbnail" width="70%"></img>
</div>

<br>

截止到 2018-19 赛季，这份包含 24 个变量的投篮数据，共计 446 万 3258 条（新赛季已经开始，总的数据量会继续增加）。稍有遗憾的是：这只是最近 20 多年的数据，因为 NBA 官方统计网站上只记载了 1996-97 赛季以来球员的详细投篮数据。

```python
# 使数据框在显示时不隐藏部分行列
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 读取外部文件，执行列类型转换，降低内存消耗
# 请将 shotInfo.csv 置于当前目录下
shotDF = (pd.read_csv(os.getcwd() + '/shotInfo.csv')
            .iloc[:,1:]
            .pipe(convert_df)
         )
# 如果需要 2019-20 赛季的数据，去掉这行筛选
shotDF = shotDF[shotDF.GAME_DATE.astype(int)<20190901]
         
# 输出数据框大小，查看数据框前 5 行
print('数据框大小:', shotDF.shape)
shotDF.head
