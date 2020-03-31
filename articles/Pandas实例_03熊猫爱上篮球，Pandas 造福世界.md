<div align='center'>
<h1><strong>数据科学 | 熊猫爱上篮球，Pandas 造福世界</strong></h1>
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
url = "https://stats.nba.com/js/data/ptsd/stats_ptsd.js"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
           'Win64; x64) AppleWebKit/537.36 (KHTML, like '
           'Gecko) Chrome/77.0.3865.90 Safari/537.36',
           'Referer': 'https://stats.nba.com/',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.9,zh-CN;'
           'q=0.8,zh;q=0.7',
           'Connection': 'keep-alive',
           'Host': 'stats.nba.com',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'same-origin',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token': 'true'
           }
colName = ['PERSON_ID','DISPLAY_LAST_COMMA_FIRST',
           'ROSTERSTATUS','FROM_YEAR','TO_YEAR',
           'TEAM_ID','GAMES_PLAYED_FLAG']
try:
    idInfo = (requests.get(url, params=params, 
                           headers=headers)
                      .json()["resultSets"][0]
             )
except Exception:
    print("\n错误：球员 ID 信息获取失败，"
          "请确认网络连接正常后重启程序！")
    exit()
else:
    print("\n成功：球员 ID 信息获取成功\n")
    idInfo = pd.DataFrame(idInfo["rowSet"], 
                          columns=idInfo["headers"])
    playerIDList = idInfo["PERSON_ID"].tolist()


# 获取球员常规赛投篮数据
shotDF, errorList, emptyList = pd.DataFrame(), [], []
# 若要获取所有球员数据，清修改 playerIDList[0:50] 为 playerIDList
for i, playerID in enumerate(playerIDList[0:50]):
    url = 'https://stats.nba.com/stats/shotchartdetail?'
    params = {
        "SeasonType": "Regular Season",
        "TeamID": 0,
        "PlayerID": playerID,
        "PlayerPosition": '',
        "GameID": '',
        "Outcome": '',
        "Location": '',
        "Month": 0,
        "SeasonSegment": '',
        "DateFrom": '',
        "DateTo": '',
        "OpponentTeamID": 0,
        "VsConference": '',
        "VsDivision": '',
        "RookieYear": '',
        "GameSegment": '',
        "Period": 0,
        "LastNGames": 0,
        "ContextMeasure": "FGA",
    }
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
shotDF.head()
```


<div align='center'>
<img src="https://uploader.shimo.im/f/Haxrq0LXCOUKuGG6.png!thumbnail"></img><br><br>
<img src="https://uploader.shimo.im/f/cab7st8SR04E3MEC.png!thumbnail"></img><br><br>
<img src="https://uploader.shimo.im/f/LyjWRzyNPSQYEhrK.png!thumbnail"></img><br><br>
<img src="https://uploader.shimo.im/f/6B7CbJcLx0EQhllw.png!thumbnail"></img>
</div>

<br>

进一步，我自定义了一个函数 exam_col_value 来查看各列的取值情况

```python
def exam_col_value(df, col):
    if isinstance(col, int):
        colName = df.columns[col]
        colIndex = col
    else:
        colName = col
        colIndex = df.columns.get_indexer([col])[0]
        
    dfCol = df[colName]
    uniqueValues = (dfCol.drop_duplicates()
                    .sort_values().values)
    uniqueValuesCount = uniqueValues.size
    
    nullMark = dfCol.isnull()
    if any(nullMark):
        nullIndex = dfCol[nullMark].index.values
    else:
        nullIndex = None

    examResult = {
        'col_index': colIndex, 
        'col_name':  colName,
        'unique_values_count': 
            uniqueValuesCount,  
        'unique_values':         
            uniqueValues, 
        'null_index': nullIndex
    }
                 
    return examResult
```

执行函数 exam_col_value(shotDF, 7) 或 exam_col_value(shotDF, 'PERIOD') 得到如下输出结果

>{'col_index': 7,
> 'col_name': 'PERIOD',
> 'unique_values_count': 8,
> 'unique_values': array([1, 2, 3, 4, 5, 6, 7, 8]),
> 'null_index': None}

从中我们知道 shotDF 的第 8 列（PERIOD 列）去重后元素个数为 8，取 1-8 不等的整数，并且该列不存在空值。

通过对 shotDF 每一列使用自定义函数 exam_col_value，并结合篮球背景知识，我们可以获知这 24 个变量的取值情况及含义：

* **刻画比赛信息的变量**
  + GAME_ID：标识比赛，共 27257 场，取 8 位整数。第 1 位均为 2，第 4 位均为 0，第 2-3 位标识赛季，第 5-8 位标识比赛场次。例如，20000054 表示 2000-01 赛季的第 54 场比赛
  + GAME_DATE：比赛日期，共 3646 天，取 8 位整数
  + HTM：主队简称，因球队更名等历史原因，共 36 个
  + VTM：客队简称，因球队更名等历史原因，共 36 个
* **刻画球员信息的变量**
  + PLAYER_ID：标识球员，共 2114 名，取 1-6 位整数，比较杂乱，目前未找到规律
  + PLAYER_NAME：球员姓名，因 11 个姓名拥有两名球员，共 2103 个
  + TEAM_ID：标识球队，共 30 个，取 10 位整数，第 1-8 位均为 16106127，第 9-10 位从 37 取到 66
  + TEAM_NAME：球队名称，因球队更名等原因，共 38 个。其中，鹈鹕有 3 个（新奥尔良黄蜂、新奥尔良/俄克拉荷马城黄蜂、新奥尔良鹈鹕）；篮网（新泽西篮网、布鲁克林篮网）、雷霆（西雅图超音速、俄克拉荷马雷霆）、灰熊（温哥华灰熊、孟菲斯灰熊）、奇才（华盛顿子弹、华盛顿奇才）、黄蜂（夏洛特山猫、夏洛特黄蜂）有 2 个；另外洛杉矶快船的 2 个名称实际上是 1 个，其中 1 个名称中洛杉矶 Los Angeles 用的是其简称 LA
* **刻画投篮基本信息的变量**
  + GAME_EVENT_ID：标识比赛事件，取 1-4 位整数，比赛事件除投篮外，还有助攻、盖帽、篮板、抢断、失误等，依据事件出现先后顺序从 1 开始标号。在 NBA 官方统计网站上可以找到 96-97 赛季以来所有比赛的详细事件记录。例如：通过访问页面 https://stats.nba.com/game/0020000054/playbyplay/ 我们可以看到 2000-01 赛季第 54 场比赛的详细事件记录
  + SHOT_MADE_FLAG：标识是否投进，投进为 1，否则为 0
  + EVENT_TYPE：球是否投进，投进为 Made Shot，否则为 Missed Shot
  + SHOT_TYPE：投篮类型，两分为 2PT Field Goal，三分为 3PT Field Goal
  + ACTION_TYPE：投篮动作类型，共 70 类，依据最后两个单词可分为 8 个大类， 包括扣篮（dunk shot）、补篮（tip shot）、上篮（layup shot）、勾手投篮（hook shot）、挑篮（roll shot）、跳投（jump shot）、后仰投篮（fadeaway shot）和擦板投篮（bank shot）。常见的抛投（floating shot）、空接（alley oop）包含在这些大类中，抛投均属于跳投，空接则属于上篮或扣篮
* **刻画投篮时间信息的变量**
  + PERIOD：投篮时比赛的节数，取 1-8 不等的整数，常规时间取 1, 2, 3 或 4，若加时，第 1 个加时记为 5，第 2 个记为 6，以此类推
  + MINUTES_REMAINING：投篮时距该节比赛结束的时间的分钟数，取 0-12 不等的整数
  + SECONDS_REMAINING：投篮时距该节比赛结束的时间的秒数，取 0-59 不等的整数
* **刻画投篮位置信息的变量**
  + SHOT_ZONE_BASIC：投篮基本区域，共 6 个，包括后场（Backcourt）、非底角三分（Above the Break 3）、左侧底角三分（Left Corner 3）、右侧底角三分（Right Corner 3）、中距离（Mid-Range）、油漆区(非限制性区域)（In the Paint (Non-RA)） 和限制性区域（Restricted Area）
  + SHOT_ZONE_AREA：投篮具体区域，共 6 个，包括左侧（Left Side(L)）、左侧中心（Left Side Center(LC)）、中心（Center(C)）、右侧中心（Right Side Center(RC)）、右侧（Right Side(R)）和后场（Back Court(BC)），它与 SHOT_ZONE_RANGE 组合构成投篮高级（advanced）区域，所谓高级指的就是比基本区域分得更细
  + SHOT_ZONE_RANGE：投篮距离区间，共 5 个，包括小于 8 英尺（Less Than 8 ft.），8-16 英尺（8-16 ft.），16-24 英尺（16-24 ft.），大于 24 英尺（24+ ft.）和后场投篮（Back Court Shot）
  + SHOT_DISTANCE：投篮点与篮筐中心的直线距离，取 0-92 不等的整数，单位为英尺
  + LOC_X：投篮点 X 轴坐标，取 -250-250 不等的整数，单位为 0.1 英尺
  + LOC_Y：投篮点 Y 轴坐标，取 -53-887 不等的整数，单位为 0.1 英尺
* **其他变量**
  + GRID_TYPE:  代表数据的含义，均为 Shot Chart Detail，即投篮图细节
  + SHOT_ATTEMPTED_FLAG：标识是否投篮，均为 1

## 3 数据预处理
如果你觉得这是官方数据，已经很规整很干净，不需要做预处理，可以直接拿来分析的话，那就错了。这份数据，其实并不干净，它至少存在以下几点问题：

1. PLAYER_NAME 列存在缺失
2. SHOT_TYPE 列存在缺失，且其对 2 分、3 分的标识存在部分错误，错把 2 分记为 3 分，3 分记为 2 分
3. ACTION_TYPE 列存在缺失和大小写不统一问题，导致同一投篮动作大类有多个名称
4. TEAM_NAME 列洛杉矶快船队有两个名称，但其中一个名称是多余的，它仅仅把洛杉矶改为洛杉矶的首字母缩写
5. SHOT_ZONE_AREA、SHOT_ZONE_RANGE 列将部分 SHOT_ZONE_BASIC 取 Above the Break 3 的数据标识为后场，与常识相悖

这些问题需要得到处理，一方面，当我们的分析需要用到这些存在问题的列时，进行预处理将有利于提高我们分析结果的准确性，另一方面，预处理后的干净数据可以存储起来，等将来有了相关的新数据，需要结合起来分析时，这部分已经预处理过的数据就无需处理了，这就省了不少事。可以说，**数据预处理，是功在当代，利在千秋的好事情**，所以啊，不要嫌麻烦，要做，一定要做，加班加点也要做。


<div align='center'>
<img src="https://uploader.shimo.im/f/8DgjNQTFhfUT4u5d.jpg!thumbnail" width="70%"></img><br><br>
<img src="https://uploader.shimo.im/f/MTc4cQkBY7U2lROt.jpeg!thumbnail"></img>
<img src="https://uploader.shimo.im/f/Utr3Mj76ed4G0uUs.jpeg!thumbnail"></img>
</div>

<br>

**接下来的 “扫黑除恶” 工作可能冗长而乏味，虽然它很重要，但如果你对此缺乏兴趣，不要硬着头皮上，使劲儿滑屏幕，滑到后面看数据分析部分吧，常言道：画条曲线，也可以拯救一个国家。**


<div align='center'>
<img src="https://uploader.shimo.im/f/mruEBqdOqFkXoAd1.jpg!thumbnail"></img>
</div>


### 3.1 前 4 个问题的处理
**我们首先来看 PLAYER_NAME 列的缺失情况**

```Python
con = shotDF.PLAYER_NAME.isnull()
col = ['PLAYER_ID', 'PLAYER_NAME']
shotDF[con][col]
```

![图片](https://uploader.shimo.im/f/XL1ZKlh54dkuv0gn.png!thumbnail)


可以看到，缺失的 PLAYER_NAME 对应的 PLAYER_ID 只有两个：902 和 1489. 因此我们只要查一下 902 和 1489 对应的球员姓名就好了，902 对应的球员姓名为 Bimbo Coles，1489 对应的球员姓名为 Lionel Simmons，于是通过以下代码就解决了 PLAYER_NAME 列存在缺失的问题。

```Python
col = 'PLAYER_NAME'
new = ['Bimbo Coles'] + ['Lionel Simmons'] * 4
shotDF.loc[con, col] = new
```

**接下来看 SHOT_TYPE 列存在的问题**

```Python
con = shotDF.SHOT_TYPE.isnull()
shotDF[con].index.tolist()
```
>[2870012]

```Python
con = shotDF.SHOT_TYPE == '3PT Field Goal'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()
```
>['Right Corner 3',<br>
> 'Above the Break 3',<br>
> 'Mid-Range',<br>
> 'Left Corner 3',<br>
> 'Backcourt',<br>
> 'Restricted Area',<br>
> 'In The Paint (Non-RA)']

SHOT_TYPE 列存在一个缺失值，这个问题并不严重，严重的是：SHOT_TYPE 列标识为 3 分的投篮，居然覆盖了 SHOT_ZONE_BASIC 的所有取值，**在油漆区和限制区投篮也被标记为 3 分，哦天哪，我以后也是可以随便投 3 分的人了！**下面的代码将依据 SHOT_ZONE_BASIC 的取值对 SHOT_TYPE 列重新赋值，这样也一并解决了 SHOT_TYPE 存在缺失的问题。

```Python
def zone_to_type(x):
    if x in [
        'Mid-Range', 
        'In The Paint (Non-RA)', 
        'Restricted Area'
    ]:
        return '2PT Field Goal'
    else:
        return '3PT Field Goal'

shotDF = shotDF.assign(SHOT_TYPE=lambda df:
                       df.SHOT_ZONE_BASIC
                       .apply(zone_to_type))
```

**接下来看一下 ACTION_TYPE 列存在的问题**

```Python
def type_to_detail(x):
    L = re.split(' ', x)
    return L[-2] + ' ' + L[-1]


shotDF = shotDF.assign(
             ACTION_TYPE_BASIC=lambda df: 
             df.ACTION_TYPE.apply(type_to_detail)
         )

shotDF.ACTION_TYPE_BASIC.sort_values().unique()
```
>array(['Bank Shot', 'Bank shot', 'Dunk Shot', <br>   
>           'Fadeaway shot', 'Hook Shot', <br>
>           'Jump Shot', 'Jump shot', 'Layup Shot', <br> 
>           'Layup shot', 'No Shot', 'Roll Shot', <br>
>           'Tip Shot'], dtype=object)

这里我新增了 1 列 ACTION_TYPE_BASIC，它对应 ACTION_TYPE 列的最后两个单词，代表投篮动作类型的大类，查看去重后这列的取值情况，Bank Shot、Jump Shot 和 Layup Shot 都有两个，难道去重童鞋罢工了？并没有，仔细看发现，两个名称一个是 Shot，一个是 shot，这怎么可以，两个明明代表的是同一类事物，于是我们需要对 ACTION_TYPE 列统一大小写，这里使用字符串类型的 lower 方法，它能使字符串中所有单词变成小写字母。

```Python
shotDF = shotDF.assign(
  shotDF.ACTION_TYPE.apply(lambda str_: str_.lower())
)
```

ACTION_TYPE 列还存在缺失，这个缺失不是空值，而是 ‘No Shot’，这个缺失如何处理呢？使用机器学习方法或许可以，但我们需要找到与投篮类型的判断高度相关的变量，这份数据似乎缺乏这样的变量，因此对这个问题暂时不做处理。

**最后我们来看一下 TEAM_NAME 列存在的问题**

```python
col1, col2 = 'TEAM_ID', 'TEAM_NAME'
(shotDF[[col1, col2]]
 .drop_duplicates(subset=col2)
 .sort_values(by=col1)
)
```

下面是截取的部分输出结果，在这张截图的最后两行，可以看到 LA Clippers 与 Los Angeles Clippers，这不是同一个名称吗，查询相关资料进一步确定了这个判断，因此这里需要将 LA 替换为 Los Angeles.


<div align='center'>
<img src="https://uploader.shimo.im/f/0GuFkL1NOqAbhiB9.png!thumbnail"></img>
</div>

<br>

类似地，执行以下代码即可完成替换

```Python
con = shotDF.TEAM_NAME =='LA Clippers'
col = 'TEAM_NAME'
new = 'Los Angeles Clippers'
shotDF.loc[con, col] = new
```

### 3.2 第 5 个问题的处理
第 5 个问题的处理相比前面 4 个问题的处理要复杂很多，首先来看 SHOT_ZONE_AREA 和 SHOT_ZONE_RANGE 列存在的问题

```Python
con = shotDF.SHOT_ZONE_AREA =='Back Court(BC)'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()
```
>['Backcourt', 'Above the Break 3']

```Python
con = shotDF.SHOT_ZONE_RANGE =='Back Court Shot'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()
```
>['Backcourt', 'Above the Break 3']

后场投篮（SHOT_ZONE_AREA='Back Court(BC)'，SHOT_ZONE_RANGE='Back Court Shot'）对应的 SHOT_ZONE_BASIC 应该是 Backcourt，怎么会出现 Above the Break 3 （前场非底角三分，或称前场正面三分）呢？

接下来我们筛选出 SHOT_ZONE_BASIC 取 Above the Break 3 的数据，选择投篮点坐标列 LOC_X,  LOC_Y 画个二维散点图，并对 SHOT_ZONE_AREA 的不同取值 （Left Side Center(LC)、Center(C) 、Right Side Center(RC) 、Back Court(BC)） 分别标绿色、红色、蓝色和黑色。

```Python
import matplotlib.pyplot as plt


con  = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
data = shotDF[con]

conLC = data.SHOT_ZONE_AREA == 'Left Side Center(LC)'
conC  = data.SHOT_ZONE_AREA == 'Center(C)'
conRC = data.SHOT_ZONE_AREA == 'Right Side Center(RC)'
conBC = data.SHOT_ZONE_AREA == 'Back Court(BC)'
dataLC = data[conLC]
dataC  = data[conC]
dataRC = data[conRC]
dataBC = data[conBC]
xLC = dataLC['LOC_X'].values
xC  = dataC ['LOC_X'].values
xRC = dataRC['LOC_X'].values
xBC = dataBC['LOC_X'].values
yLC = dataLC['LOC_Y'].values
yC  = dataC ['LOC_Y'].values
yRC = dataRC['LOC_Y'].values
yBC = dataBC['LOC_Y'].values

# 若不是使用的 jupyter notebook
# 请删除下面一行
%matplotlib notebook
plt.figure()
plt.scatter(xLC, yLC, s=1, alpha=0.3, color='green')
plt.scatter(xC,  yC,  s=1, alpha=0.3, color='red')
plt.scatter(xRC, yRC, s=1, alpha=0.3, color='blue')
plt.scatter(xBC, yBC, s=1, alpha=0.3, color='black')
plt.show()
```

<div align='center'>
<img src="https://uploader.shimo.im/f/5BT6wXnReUQKuaw9.png!thumbnail" width="90%"></img>
</div>

<br>

NBA 篮球场全长 94 英尺，半场长 47.5 英尺，数据中的 LOC_X=0, LOC_Y=0 指代篮筐中心，这一中心距离底线 5.3 英尺，因此 LOC_Y 的取值范围为 -53-887，单位取 0.1 英尺，所以当 LOC_Y > 417 时，该投篮才是后场投篮。

从上图中可以看出，这些黑色散点（SHOT_ZONE_BASIC = ‘Above the Break 3‘ 且 SHOT_ZONE_AREA = ’Back Court(BC)‘  的点）中的绝大部分，它们的 LOC_Y 都小于 417，并不属于后场投篮，其 SHOT_ZONE_AREA 不应该等于 Back Court(BC)。而这些黑色散点中真正属于后场投篮的小部分，其 SHOT_ZONE_BASIC 不应该等于 Above the Break 3，而应该等于 Backcourt。

因此我们有必要对这些黑色散点的 SHOT_ZONE_BASIC，SHOT_ZONE_AREA 以及与它们相关的 SHOT_ZONE_RANGE 重新赋值。具体怎么做呢？

黑色散点的 SHOT_ZONE_BASIC 只可能是 Above the Break 3 和 Backcourt，到底是哪一个，依据 LOC_Y 与 417 的大小关系即可确定，如果  LOC_Y <= 417，SHOT_ZONE_BASIC=‘Above the Break 3’，否则 SHOT_ZONE_BASIC='Backcourt'。

当 SHOT_ZONE_BASIC='Backcourt' 时，SHOT_ZONE_AREA  和 SHOT_ZONE_RANGE 的赋值非常简单，因为此时它们分别取确定的值 Back Court(BC) 和 Back Court Shot. 

当 SHOT_ZONE_BASIC=‘Above the Break 3’ 时，SHOT_ZONE_RANGE 取确定的值 24+ ft. ，其赋值也非常简单。困难在于 SHOT_ZONE_AREA 有三种可能取值（Left Side Center(LC)、Center(C) 或 Right Side Center(RC)），而 NBA 官方并没有告诉我们划分的标准，因此我们需要自己从数据中找出这个标准来。

从上图中可以看到，使用两条直线可以将  SHOT_ZONE_AREA 划分为三个，从 NBA 官方统计网站上的球员投篮区域图可以确认这一点，因此我们只需要确定这两条直线的方程，就可以依据 LOC_X、LOC_Y 顺利得到 SHOT_ZONE_AREA 的取值了。

我们能从这份数据中得到这两条直线的精确方程吗？答案是不能的，因为数据是不完美的。如果将图片放大仔细观察，你会发现，绿色、红色、蓝色的边界线并不笔直，怎么会不笔直呢？造成这种不笔直的原因可能有两个：一是 LOC_X、LOC_Y 只取整数而直线是实数域下的，二是部分数据本身存在错误。


<div align='center'>
<img src="https://uploader.shimo.im/f/QGMZRs2WvCIXwwur.png!thumbnail" width="29%"></img>
<img src="https://uploader.shimo.im/f/3EeNWzCOpq4kR0GW.png!thumbnail" width="21%"></img> 
</div>

<br>

虽然并不完美，但并不影响我们获得两个近似的直线方程。由于篮球场的对称性，我们只需要获得其中一条直线的方程，便可以得到另一条直线的方程。

下面使用**支持向量机**技术，利用 **scikit-learn** 包里的 **svm** 模块获得划分蓝色和红色区域直线的方程（右侧直线的方程）。为了充分利用数据，我们将红色左半区域以及绿色区域的数据依 y 轴做个对称变换（新增 1 列 LOC_X_ABS，取 LOC_X 的绝对值），并新增 1 列 SHOT_ZONE_MARK，绿色、蓝色散点的 SHOT_ZONE_MARK 记为 0，红色散点的 SHOT_ZONE_MARK 记为 1。下面是相关代码，代码输出两条直线的近似方程。

```Python
def area_to_num(x):
    return 1 if x == 'Center(C)' else 0
  

con1 = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
con2 = shotDF.SHOT_ZONE_AREA  != 'Back Court(BC)'    
dataSvm = (shotDF[(con1) & (con2)]
           .assign(
               SHOT_ZONE_MARK=lambda df: 
                   df.SHOT_ZONE_AREA.apply(area_to_num),
               LOC_X_ABS=lambda df: 
                   df.LOC_X.apply(abs)
            )
          )
col1 = ['LOC_X_ABS', 'LOC_Y']
col2 = 'SHOT_ZONE_MARK'
xSvm = dataSvm[col1].values
ySvm = dataSvm[col2].values

lin_clf = svm.SVC(kernel='linear')
lin_clf.fit(xSvm, ySvm)
omega1 = lin_clf.coef_[0, 0]
omega2 = lin_clf.coef_[0, 1]
b = lin_clf.intercept_[0]
if omega2 > 0:
    print(('右侧直线方程：{0:.4f}x + {1:.4f}y = {2:.4f}')
          .format( omega1, omega2, -b))
    print(('左侧直线方程：{0:.4f}x + {1:.4f}y = {2:.4f}')
          .format(-omega1, omega2, -b))
else:
    print(('右侧直线方程：{0:.4f}x - {1:.4f}y = {2:.4f}')
          .format( omega1, omega2, -b))
    print(('左侧直线方程：{0:.4f}x - {1:.4f}y = {2:.4f}')
          .format(-omega1, omega2, -b))
```
>右侧直线方程：-11.3333x + 3.6667y = -4.0000
>左侧直线方程：11.3333x + 3.6667y = -4.0000

对上述方程左右两边同乘 3 得到：右侧直线方程为 -34x + 11y + 12 = 0，左侧直线方程为 34x + 11y + 12 = 0. 这样依据 LOC_X，LOC_Y 确定前场非底角三分的 SHOT_ZONE_AREA 取值的规则就有了，下面对 SHOT_ZONE_BASIC=‘Above the Break 3’ 的数据的 SHOT_ZONE_BASIC、SHOT_ZONE_AREA 和 SHOT_ZONE_RANGE 列重新赋值，由于整个数据集较大，重新赋值需要一定时间。

```Python
# 对 LOC_Y 大于 417 的数据
# 为后场投篮
# SHOT_ZONE_BASIC 应取 Backcourt
con1 = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
con2 = shotDF.LOC_Y.astype(int) > 417
col  = 'SHOT_ZONE_BASIC'
new  = 'Backcourt'
shotDF.loc[(con1) & (con2), col] = new

# 对三分，SHOT_ZONE_RANGE 
# 均为 24+ ft，即大于 24 英尺
# 严格来说，底角三分应为 22+ ft
# 这是官方数据的问题
# 但这个问题不大，未作处理
col = 'SHOT_ZONE_RANGE'
new = '24+ ft.'      
shotDF.loc[con1, col] = new

# 根据直线方程修改 SHOT_ZONE_AREA
def modify_area(df):
    con1  = df.SHOT_ZONE_BASIC == 'Above the Break 3'
    con2  = df.SHOT_ZONE_AREA == 'Back Court(BC)'
    equaL =   34 * df.LOC_X + 11 * df.LOC_Y + 12
    equaR = - 34 * df.LOC_X + 11 * df.LOC_Y + 12
    areaL = ['Left Side Center(LC)',
             'Center(C)',
             'Right Side Center(RC)'
            ]       
    if con1 and con2:
        if df.LOC_X >= 0:
            return areaL[1] if equaR >= 0 else areaL[2]
        else:
            return areaL[1] if equaL >= 0 else areaL[0]
    else:
        return df.SHOT_ZONE_AREA


shotDF = shotDF.assign(
             SHOT_ZONE_AREA=lambda df: 
             df.apply(modify_area, axis=1)
         )
```

对修改以后的数据，再来画一下散点图，看看对上图中大部分黑色散点（注：本为前场非底角三分却被标记为后场投篮的部分，不包括 LOC_Y>417 即实际为后场投篮的部分）区域的分配是否合理。将上面画散点图的代码中定义 dataBC，xBC，yBC 的部分以及 plt.scatter(xBC, yBC...) 注释后，运行得到如下所示的图形


<div align='center'>
<img src="https://uploader.shimo.im/f/YfTjhl4wpREbCJEp.png!thumbnail" width="90%"></img>
</div>

<br>

对比两张散点图，可以清晰地看到，对黑色散点所作的处理是成功的。至此，数据预处理工作就结束了。


<div align='center'>
<img src="https://uploader.shimo.im/f/eUiZFkMi4KggnMMk.png!thumbnail"></img>
<img src="https://uploader.shimo.im/f/9aZysvzow50SwWR6.gif" width="26%"></img>
</div>

<br>

## 4 数据分析
熊猫先森左顾右盼，终于从我这里盼来了梦寐以求的干净数据，现在，可以大干一场了。

“什么，高度有 400 多万，宽度只有 24，又是个经不起风吹雨打，一刮就倒的小瘦子，有啥用，能不能给她增加点宽度，啊啊啊，我不要这样的对象，我要又高又胖的，不行不行，又高又胖非得给我压死不成，啊，我到底需要什么，啊啊啊，熊猫，你说你啥时候才能知道自己需要什么呢，你这个幼稚鬼。啊，气死我了，我还是好好分析一下我亲爱的数据（对象）吧。”

做事之前，熊猫先森总要自言自语一番。熊猫先森今年 36 岁，阳刚而开朗，软弱而忧郁。按理说，这是两种完全对立的性格，但它们却在熊猫先森身上以一种常人难以理解而又近乎完美的状态交融着。

进化生物学家们曾经预言：熊猫先森将引领人类的第二次进化，自现代人类从猿进化以来，人类这一地球最高智慧物种，一直在积蓄着进化的动能，而量变到质变的飞跃，恐怕离我们很近了。

熊猫先森从来瞧不起那些进化生物学家，但那些进化生物学家们并不知道，他们觉得熊猫先森为人和善、心胸宽广，他们不仅这么觉得，还经常当面这么夸他。熊猫先森瞧不起他们，倒不因为别的，只因为觉得他们不像他那般，胸无大志，苟且偷生。

熊猫先森一边吃着他的**八角炒竹笋**，一边分析着他的数据。


<div align='center'>
<img src="https://uploader.shimo.im/f/sRMBX35OZXkBE3KC.jpeg!thumbnail" width="35%"></img>
<img src="https://uploader.shimo.im/f/FhcdUr1V7mUeGuhh.jpg!thumbnail" width="35%"></img>
</div>

<br>

坊间流传着这样的话：**在 NBA，球员们越来越多地选择三分或油漆区，中距离投篮越来越少。果真如此吗**？ 熊猫先森拿来数据，依据 GAME_ID 生成新列 SEASON，代表赛季，依据 SHOT_ZONE_BASIC 生成新列 SHOT_TYPE_DETAIL，代表详细投篮类型，包括 2 分（油漆区）、2 分（中投）和 3 分。而后熊猫先森根据这两列构建一个列联表（交叉表），统计各赛季不同投篮类型的占比情况，使用 pyecharts 包画了如下的折线图。

```python
def proc_date(x):
    strx = str(x)
    year, month = strx[0:4], strx[4:6]
    if int(month) < 9:
        return str(int(year) - 1) + '-' + year[2:]
    else:
        return year + '-' + str(int(year) + 1)[2:]

def proc_zone(x):
    if x == 'Mid-Range':
        return '2 PT (Mid-Range)'
    elif x == 'In The Paint (Non-RA)' or x == 'Restricted Area':
        return '2 PT (Paint)'
    else:
        return '3 PT'

shotDF = (shotDF.assign(SEASON=lambda df: df.GAME_DATE.apply(proc_date),
                        SHOT_TYPE_DETAIL=lambda df: df.SHOT_ZONE_BASIC.apply(proc_zone)
                       )
                .pipe(convert_df))

shotDF_crosstab = pd.crosstab(shotDF.SEASON, shotDF.SHOT_TYPE_DETAIL).apply(lambda _row: _row/sum(_row), 1)
print(shotDF_crosstab)

roundV = np.vectorize(round)
datax = list(map(lambda x: str(x)[2:7], shotDF_crosstab.index.tolist()))
datay = roundV(shotDF_crosstab.values.T, 4)

c = (
     Line()
     .add_xaxis(datax)
     .add_yaxis("2 分（中投）", datay[0].tolist())
     .add_yaxis("2 分（油漆区）", datay[1].tolist())
     .add_yaxis("3 分", datay[2].tolist())
     .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
     )
     .set_global_opts(
         title_opts=opts.TitleOpts(title="NBA 球员投篮选择的变化"),
         xaxis_opts=opts.AxisOpts(
             axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
             axislabel_opts=opts.LabelOpts(rotate=45, font_size=12, margin=14)
         ),
     )
)

c.render_notebook()
```


<div align='center'>
<img src="https://uploader.shimo.im/f/dtqHlkGTHM06Yrt2.png!thumbnail" width="90%"></img>
</div>

<br>

自 1999-00 赛季以来，NBA 球员选择中投的比例一直在下降，特别是从 2012-13 赛季开始，降幅进一步加大。与之相对应的是：除了在 2009-10 赛季以及 2010-11 赛季有少许回落外，自 1999-00 赛季以来，NBA 球员选择三分的比例一直在上升，同样地从 2012-13 赛季开始，增幅进一步加大。

**到 2018-19 赛季，NBA 球员投篮时选择三分的比例从 1996-97 赛季的 10.8% 增加到了 35.8%，与之相对应的是中投的比例从 1996-97 赛季的 39.9% 下降到 15.2%，而且从图中，我们看不到这种趋势停止的任何迹象**，可以预见的是，2019-20 赛季，三分出手的比例将进一步增加，中投比例将进一步减少。

从图中，我们还可以看到：自 1996-97 赛季至今，NBA 球员选择油漆区投篮的比例稳定在 44%-50% 这个区间，对比 1996-97 赛季和 2018-19 赛季，1996-97 赛季选择油漆区投篮的比例为 49.3%，2018-19 赛季为 49.0%，并无多少显著变化。

2012-13 赛季，或许是一个在当时看起来并不那么起眼的赛季，伤愈归来的库里，在他的第 4 个赛季里，投进了 272 记 3 分球，一举打破了尘封 7 年的常规赛 3 分球纪录：雷阿伦的 269 记 3 分球。那个赛季，库里以场均 22.9 分，4 个篮板，6.9 次助攻，1.6 次抢断的成绩单，成功带领勇士以西部第 6 的身份杀入季后赛。


<div align='center'>
<img src="https://uploader.shimo.im/f/sIY3NfsElsoh3RyQ.jpeg!thumbnail" width="70%"></img>
</div>

<br>

那时，人们不会想到，两个赛季后的 2014-15 赛季，库里以 286 记 3 分球再次打破自己所保持的 3 分球纪录，带领勇士时隔 40 年后再次捧起 NBA 总冠军奖杯，并以 98 记 3 分球打破季后赛三分球纪录。人们更不会想到，紧接着的 2015-16 赛季，库里以 402 记 3 分球第三次刷新常规赛 3 分球纪录，并带领勇士豪取 73 胜，打破了 1995-96 赛季公牛 72 胜纪录的同时成为史上第一支常规赛没有连败的球队。


<div align='center'>
<img src="https://uploader.shimo.im/f/NDYD21ZLu0wgbklH.jpeg!thumbnail" width="70%"></img>
</div>

<br>

今天，在野球场上，远距离进攻正在得到大家的认同，我们能看到越来越多的人选择 3 分这样的进攻方式，人们不再固执地认为一定要往里打，一定要离篮筐越近越好，一定是得内线（油漆区）者才能得天下。

2015-16 赛季的库里是恐怖的，当一个球员运球过中场线后就可以出手投篮，将离着 3 分线两三米的区域视作常规投篮区域时，如何防守呢？那个赛季过后，我以为库里将成为下一个篮球之神，遗憾的是，他没有成为。NBA 历史上首个全票当选常规赛最有价值球员的库里，带着 73 胜光环的勇士，在 3-1 领先的情况下被骑士连扳 3 局，惨遭逆转，输掉了当年的总决赛。随后，在一片谩骂声中，杜兰特加盟勇士，在拥有杜兰特的三个赛季里，他们三次杀入总决赛，两夺总冠军。


<div align='center'>
<img src="https://uploader.shimo.im/f/5Wph2AyppTornkcc.jpeg!thumbnail" width="70%"></img>
</div>

<br>

随着杜兰特的离开，新赛季开局阶段的勇士战绩惨淡，西部垫底。库里掌骨骨折，更是雪上加霜。属于勇士的时代，或许还会以一种新的方式出现，或许就这样土崩瓦解一去不复返了。究竟如何，已经不重要了，勇士将篮球运动带入了崭新的时代，在这个全新的时代里，篮球不再是内线巨人的天下，篮球的各个位置开始变得模糊，3 分从篮球比赛的边缘成长为比赛的常规武器。而塑造这个时代的灵魂人物，库里，早已无需成为篮球之神了，因为他就是这个新时代的代名词。

熊猫先森娴熟地写着分析报告，八角的清香让他欲罢不能。

**三分占比的大幅提升有没有带来三分命中率的提升**？熊猫先森想到了这个问题。于是他使用 pandas 中的 pivot_table 函数得到了各赛季各投篮类型的命中率，同样地，他使用 pyecharts 包画了如下的折线图

```python
def rate(x):
    x = x.astype(int)
    return x.sum() / x.size

shotDF_pivtab = shotDF.pivot_table(values='SHOT_MADE_FLAG', index='SEASON', columns='SHOT_TYPE_DETAIL', aggfunc={'SHOT_MADE_FLAG': rate})
print(shotDF_pivtab)

roundV = np.vectorize(round)
datax = list(map(lambda x: str(x)[2:7], shotDF_pivtab.index.tolist()))
datay = roundV(shotDF_pivtab.values.T, 4)

c = (
     Line()
     .add_xaxis(datax)
     .add_yaxis("2 分（中投）", datay[0].tolist())
     .add_yaxis("2 分（油漆区）", datay[1].tolist())
     .add_yaxis("3 分", datay[2].tolist())
     .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
     )
     .set_global_opts(
         title_opts=opts.TitleOpts(title="NBA 球员投篮命中率的变化"),
         xaxis_opts=opts.AxisOpts(
                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                                  axislabel_opts=opts.LabelOpts(rotate=45, font_size=12, margin=14)
         ),
     )
)

c.render_notebook()
```


<div align='center'>
<img src="https://uploader.shimo.im/f/wyptYY4WVsIp2oRA.png!thumbnail" width="90%"></img>
</div>

<br>

**与投篮选择形成鲜明对比的是，NBA 球员各赛季油漆区、中投、三分的命中率无比平稳，三分出手比例的持续上升并没有带来三分命中率的提升**。曾记得很久以前看过一段话，命中率不断提升是篮球运动发展的趋势，而从 96-97 赛季至今的 NBA 常规赛投篮数据，显然否定了这种说法，虽然存在以偏概全的风险，但这种说法至少是值得怀疑的。

透过这张图，我们或许能从一个侧面理解为什么球员们会纷纷减少中投而增加三分的出手。中投命中率 40% 左右，只比三分命中率高出约 5 个百分点，相差并不大，按这样的命中率，投 100 个 3 分能得 105 分，而投 100 个中投只能得到 80 分，所以就像那句 “人生苦短，我用 Python” 一样，对于球员们而言，生涯苦短，我投三分！ 

**自 1996-97 赛季以来，NBA 常规赛发生了多少 4 加时比赛**？熊猫先森想到了他的第 3 个问题，他对这些异常值们，总有着饱满的热情与浓厚的兴趣。熊猫先森熟练地敲击着键盘，系统为他返回了五场比赛，它们依次是：

```python
(shotDF[shotDF.PERIOD==8]
.drop_duplicates(subset='GAME_ID')
.sort_values(by='SEASON')
)
```

* 1997 年 11 月 14 日，菲尼克斯太阳 vs 波特兰开拓者

<div align='center'>
<img src="https://uploader.shimo.im/f/HB8NeB4yey427BaJ.png!thumbnail" width="70%"></img>
</div>

* 2012 年 3 月 25 日，犹他爵士 vs 亚特兰大老鹰 

<div align='center'>
<img src="https://uploader.shimo.im/f/Lg6wOAk1aZwBZZc5.png!thumbnail" width="70%"></img>
</div>

* 2015 年 12 月 18 日，底特律活塞 vs 芝加哥公牛

<div align='center'>
<img src="https://uploader.shimo.im/f/xbdwYiP6gVAVelvL.png!thumbnail" width="70%"></img>
</div>

* 2017 年 1 月 29 日，纽约尼克斯 vs 亚特兰大老鹰 

<div align='center'>
<img src="https://uploader.shimo.im/f/s1ycvIK4NYMDU1af.png!thumbnail" width="70%"></img>
</div>

* 2019 年 3 月 1 日，芝加哥公牛 vs 亚特兰大老鹰 

<div align='center'>
<img src="https://uploader.shimo.im/f/NLx4E1UBdwMBAp3c.png!thumbnail" width="70%"></img>
</div>


**进入 21 世纪之后，亚特兰大老鹰如有神助，在仅有的四场 4 加时比赛中豪取三场，同时拿下其中两场的胜利，更加出色的是这三场比赛都是老鹰的主场，嗯，体验 4 加时，我选择定居亚特兰大**！老鹰加入 NBA 70 年了，自 1957-58 赛季拿到 NBA 总冠军后，球队再也没有收获过总冠军奖杯，2015 年老鹰更换了队徽，新的老鹰还能展翅翱翔，再现辉煌吗？亚特兰大，这座在南北战争废墟里成长起来的城市，这座拥有美国三大理工学院之一的城市，一直在静静等待着。


<div align='center'>
<img src="https://uploader.shimo.im/f/PyR4bCWog7g8rPg3.jpeg!thumbnail" width="70%"></img>
</div>

<br>

夜深了，菜碟里只剩下三只八角，熊猫先森用纸巾擦拭着嘴角的口水，意犹未尽。它准备画一下**球员的投篮图**，而后心满意足地进入梦乡。熊猫先森首先完成了半个 NBA 篮球场的绘制，别看这篮球场小小的，把熊猫先森折腾得嗷嗷叫。

>NBA 篮球场与我们平常所见的篮球场有不少差异，最典型的就是 3 分线更远。此外，NBA 篮球场有自己独有的标记线，例如底线和罚球圈附近的 4 个用来标识低位防守区域的标记。低位防守区域的一个作用是：从该区域开始进攻的进攻球员若在限制区内冲撞事先占据合法防守位置的防守球员，可以吹罚进攻球员进攻犯规，也就是说限制区原本允许的合理冲撞在这种情况下失效了。法纳斯特公众号，乃至 NBA 官方统计网站，对 NBA 半个篮球场各标记线的绘制都是不完整的，此外它们还绘制了多余的两条标记线，这两条标记线标识以前的油漆区（12 英尺宽），在现今 NBA 比赛中已没有作用了（现在的油漆区是 16 英尺宽），当然 全美大学生篮球联赛仍旧使用 12 英尺宽的油漆区。


<div align='center'>
<img src="https://uploader.shimo.im/f/gd8BjuZ1z8U5lHCU.png!thumbnail" width="70%"></img>
</div>


```python
def Arc_fill(center, radius, theta1, theta2, resolution=50, **kwargs):
    # generate the points
    theta = np.linspace(np.radians(theta1), np.radians(theta2), resolution)
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1]))
    # build the polygon and add it to the axes
    poly = Polygon(points.T, closed=True, **kwargs)
    return poly


def shot_plot(playerName = 'Kobe Bryant', season = '2005-06', color='#003370', lw=2):

    %matplotlib notebook

    # 新建一个大小为(6,6)的绘图窗口
    plt.figure(figsize=(5.36, 5.06), frameon=False)

    # 获得当前的Axes对象ax,进行绘图
    ax = plt.gca(frame_on=False)

    # 设置坐标轴范围
    ax.set_xlim(-268, 268)
    ax.set_ylim(435, -71)

    # 消除坐标轴刻度
    ax.set_xticks([])
    ax.set_yticks([])

    # 添加备注信息
    plt.title(playerName+' '+season+' SEASON')

    # 对篮球场进行底色填充
    lines_outer_rec = Rectangle(xy=(-268, -65.5), width=536, height=506,
                                color='#f1f1f1', fill=True, zorder=0)
    ax.add_patch(lines_outer_rec)

    # 篮板，距底线 4 ft，宽 6 ft
    plate = Rectangle(xy=(-30, -13), width=60, height=0, linewidth=lw,
                      color=color, fill=False, zorder=4)
    ax.add_patch(plate)

    # 篮筐，半径 0.75 ft
    circle_ball = Circle(xy=(0, 0), radius=7.5, linewidth=lw, color=color,
                         fill=False, zorder=4)
    ax.add_patch(circle_ball)

    # 限制区，半径 4 ft
    restricted_arc = Arc(xy=(0, 0), width=80, height=80, theta1=0,
                         theta2=180, linewidth=lw, color=color, 
                         fill=False, zorder=4)
    ax.add_patch(restricted_arc)

    # 油漆区，宽 16 ft，高 19 ft
    outer_rec_fill = Rectangle(xy=(-80, -53), width=160, height=190,
                               linewidth=lw, color="#fefefe", fill=True, zorder=2)
    outer_rec = Rectangle(xy=(-80, -53), width=160, height=190,
                          linewidth=lw, color=color, fill=False, zorder=4)
    ax.add_patch(outer_rec_fill)
    ax.add_patch(outer_rec)

    # 罚球站位点，距底线 7.1 ft, 8.3 ft, 11.5 ft, 14.7 ft
    lane_space_left1 = Rectangle(xy=(-90, 18), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_left2 = Rectangle(xy=(-90, 30), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_left3 = Rectangle(xy=(-90, 62), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_left4 = Rectangle(xy=(-90, 94), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_right1 = Rectangle(xy=(80, 18), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_right2 = Rectangle(xy=(80, 30), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_right3 = Rectangle(xy=(80, 62), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_right4 = Rectangle(xy=(80, 94), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    ax.add_patch(lane_space_left1)
    ax.add_patch(lane_space_left2)
    ax.add_patch(lane_space_left3)
    ax.add_patch(lane_space_left4)
    ax.add_patch(lane_space_right1)
    ax.add_patch(lane_space_right2)
    ax.add_patch(lane_space_right3)
    ax.add_patch(lane_space_right4)

    # 罚球区与争球区, 罚球线距篮筐中心 13.7 ft
    circle_punish1 = Arc(xy=(0, 137), width=120, height=120, theta1=0,
                         theta2=180, linewidth=lw, color=color, 
                         fill=False, zorder=4)
    circle_punish2 = Arc(xy=(0, 137), width=120, height=120, theta1=180,
                         theta2=360, linewidth=lw, linestyle='--', 
                         color=color, fill=False, zorder=4)
    ax.add_patch(circle_punish1)
    ax.add_patch(circle_punish2)

    # 低位防守区域标志线
    hash_marks_left1 = Rectangle(xy=(-110, -53), width=0, height=5,
                                linewidth=lw, color=color,
                                fill=False, zorder=4)
    hash_marks_right1 = Rectangle(xy=(110, -53), width=0, height=5,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    hash_marks_left2 = Rectangle(xy=(-50, 77), width=5, height=0,
                                linewidth=lw, color=color,
                                fill=False, zorder=4)
    hash_marks_right2 = Rectangle(xy=(45, 77), width=5, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    ax.add_patch(hash_marks_left1)
    ax.add_patch(hash_marks_right1)
    ax.add_patch(hash_marks_left2)
    ax.add_patch(hash_marks_right2)

    # 三分线左边线
    three_left_rec_fill = Rectangle(xy=(-220, -53), width=440, height=146,
                                    ec="#dfdfdf", fc="#dfdfdf", 
                                    fill=True, zorder=1)
    three_left_rec = Rectangle(xy=(-220, -53), width=0, height=146,
                               linewidth=lw, color=color, fill=False, zorder=4)
    ax.add_patch(three_left_rec_fill)
    ax.add_patch(three_left_rec)

    # 三分线右边线
    three_right_rec = Rectangle(xy=(220, -53), width=0, height=146,
                                linewidth=lw, color=color, 
                                fill=False, zorder=4)
    ax.add_patch(three_right_rec)

    # 三分线圆弧, 圆心为 (0,0),半径为 238.66,起始角度为 22.8,结束角度为 157.2
    three_arc_fill = Arc_fill(center=(0, 0), radius=239, theta1=23, 
                              theta2=157, resolution=50, linewidth=0,
                              ec="#dfdfdf", fc="#dfdfdf", fill=True, zorder=1)
    three_arc = Arc(xy=(0, 0), width=478, height=478, theta1=23,
                    theta2=157, linewidth=lw, color=color,
                    fill=False, zorder=4)
    ax.add_patch(three_arc_fill)
    ax.add_patch(three_arc)

    # 教练席标记线
    midcourt_area_marker_left = Rectangle(xy=(-250, 227), width=30, height=0,
                                          color=color, linewidth=lw, 
                                          fill=False, zorder=4)
    midcourt_area_marker_right = Rectangle(xy=(220, 227), width=30, height=0,
                                           color=color, linewidth=lw,
                                           fill=False, zorder=4)
    ax.add_patch(midcourt_area_marker_left)
    ax.add_patch(midcourt_area_marker_right)

    # 中场外半圆, 半径 6 ft
    center_outer_arc = Arc(xy=(0, 417), width=120, height=120, theta1=180,
                           theta2=0, linewidth=lw, color=color,
                           fill=False, zorder=4)
    ax.add_patch(center_outer_arc)

    # 中场处内半圆,半径 6 ft
    center_inner_arc = Arc(xy=(0, 417), width=40, height=40, theta1=180,
                           theta2=0, linewidth=lw, color=color,
                           fill=False, zorder=4)
    ax.add_patch(center_inner_arc)

    # 半场边线框, 长 47 ft, 宽 50 ft
    lines_outer_rec = Rectangle(xy=(-250, -53), width=500, height=470,
                                linewidth=lw, color=color,
                                fill=False, zorder=4)
    ax.add_patch(lines_outer_rec)

    shotMade = shotDF[(shotDF.PLAYER_NAME==playerName) & (shotDF.SHOT_MADE_FLAG==1) & (shotDF.SEASON==season)][['LOC_X', 'LOC_Y']]
    x_shotMade, y_shotMade = shotMade['LOC_X'], shotMade['LOC_Y']
    shotMiss = shotDF[(shotDF.PLAYER_NAME==playerName) & (shotDF.SHOT_MADE_FLAG==0) & (shotDF.SEASON==season)][['LOC_X', 'LOC_Y']]
    x_shotMiss, y_shotMiss = shotMiss['LOC_X'], shotMiss['LOC_Y']

    plt.scatter(x_shotMiss, y_shotMiss, alpha=0.8, s=30, marker='x', c='#B02020', zorder=3)
    plt.scatter(x_shotMade, y_shotMade, alpha=0.6, s=30, marker='o', c='#208020', zorder=3)
    # plt.savefig('/home/xiaozhou/Pictures/'+playerName+'_'+season+'.png')
    plt.show()
```

接下来，熊猫先森依据 LOC_X、LOC_Y、SHOT_MADE_FLAG、SEASON 四列对比了一下库里的新秀赛季和巅峰赛季的投篮点分布情况，**从中我们可以看到这位划时代的三分投手在投篮选择上的巨大变化，以及巅峰赛季令人胆寒的出手距离**。

```python
shot_plot('Stephen Curry', '2009-10')
shot_plot('Stephen Curry', '2015-16')
```


<div align='center'>
<img src="https://uploader.shimo.im/f/AWEZmuxmjZIEokre.png!thumbnail" width="70%"></img>
<img src="https://uploader.shimo.im/f/Bni2xL9wcIsf7ywf.png!thumbnail" width="70%"></img>
</div>


最后的最后，熊猫先森从一堆堆的球员投篮图中抓出一幅，贴在了自己的办公桌前，他要向他致敬，向伟大致敬！熊猫先森想：**要是在这位球员的身上，注入库里划时代的三分球能力，会是怎样一番场景呢？**他知道，他不能这样想下去，但他控制不了自己，他睡着了，在他的梦中，他操控着这个世界，向着进化生物学家预言的方向，分毫不差地前进着。

```python
shot_plot()
```

<div align='center'>
<img src="https://uploader.shimo.im/f/otvFn2elIyEqeydF.png!thumbnail" width="70%"></img>
</div>


这个方向是什么，今时今日的普罗大众还无从得知。

**多年以后，醒来的熊猫先森会看到，那时的世界，娱乐主宰着一切**，因为科学历史性地消失了，不是娱乐吞噬了科学，而是科学失去了存在的必要。

**2089 年，生命科学最后的难关攻破，人们终于理解了自己，理解了大脑的工作原理，理解了我们的身体决定了我们的喜怒哀乐。**

在那个全新的时代里，所有人都学会了如何驾驭自己的身体，所有人也历史性地获得了理解他人的能力，嫉妒消失了，仇恨消失了，娱乐成为人们一生的追求，世界被史无前例地连为一体，欢声笑语笼罩着这颗年轻而美丽的星球。

**这一年，联合国更换徽章。**

竹叶替代了橄榄。

篮球取代了地图。

**这一年，史称 “嘻哈熊猫”。**


<div align='center'>
<img src="https://uploader.shimo.im/f/fH4rfQrYgrgBIPNr.jpeg!thumbnail" width="70%"></img>
<img src="https://uploader.shimo.im/f/FqhAhE4BScIk6UDb.jpg!thumbnail" width="70%"></img>
</div>

<br>

## 5 尾声
2090 年 8 月 2 日，37 岁的熊猫先森，接到了他的“仇人”，92 岁高龄的坤坤的电话，电话接通的一刹那，他们异口同声：

**熊坤，祝你生日快乐！**

这时，人们才知道，1983 年出生的熊猫先森，名叫熊坤。在他 15 岁那年，利用自行研发的技术创造了自己的复制体：坤坤。废寝忘食的投入，耗费了熊猫先森太多的精力，他的发育从此停止了。

2019 年，熊猫先森的复制体，21 岁的坤坤成长为全球顶尖进化生物学家，正是这一年，坤坤意外发现：停止发育的熊猫先森身上，蕴藏着革新整个人类的巨大能量，而激发这种能量的唯一方式，是让熊猫先森爱上篮球，而后进入休眠状态。

2091 年 5 月，醒来两年的熊猫先森与 93 岁的坤坤一同来到中国四川省雅安市宝兴县**戴维新村**，在装饰一新的戴维雕塑面前放上了两个篮球，篮球上是法国球星帕克先生和中国球星姚明先生的签名。雕塑一旁的文字展板，向过往的游客，讲述着熊猫这个物种被人类发现的历史：

>1869 年 3 月，在四川宝兴活动的法国传教士兼动植物学家戴维先生在日记中写道：“我见到一张漂亮的著名的黑白熊皮，个体相当大，非常独特……我很兴奋，它可能成为科学界一个有趣的新种！”。5 月，戴维计划将捕捉到的一只“白熊”带回巴黎，不幸的是，途中“白熊”病逝，戴维只好将其制成标本，寄送给法国国家博物馆，博物馆的专家研究认为，它既不是熊，也不是猫，便正式给它定名为 “猫熊”。这个拉丁学名传回中国后，因当时从右往左的阅读习惯，其译文被误读为 “熊猫” 并沿用至今 —— 中国科学院进化生物学家 坤坤 2019 年 11 月

**从戴维新村离开后，他们驱车 1300 多公里，来到新时代世界的中心—中国湖南省长沙市，彼时的芒果台，汇聚着全世界人民的目光。**

橘子洲头，他们见到了我，自将处理好的数据交给熊猫先森分析后，我就再没见过他。

熊猫先森热情地向我介绍他 1998 年创造的坤坤，向我讲述他的故事，讲述他在梦中的所见所闻、所思所想。

那一年，95 岁高龄的我，回到那所老房子，将床头的熊猫篮球灯饰取下，抱在怀中，而后，带着微笑进入了长长的梦乡，梦中，我幻想着：1000 年后醒来时，世界的样子。

进入梦乡前，我第一次得知了自己的身份：熊猫先森 1996 年 2 月阅读《物种起源》时意外创造的复制体。

>以上摘自熊坤本人今年写于火星的散文集《我与我的复制体》，文中以熊猫先森指代熊坤本人，以我指代熊坤的第一个显式复制体熊熊，以坤坤指代熊坤的第二个显式复制体。熊坤先生还有另外四个隐式复制体：能能、点点、土土和申申，在熊熊沉睡的千年里，他们先后以不同方式推动人类完成了四次进化。
>
>今天的史学家将人类自 21 世纪以来先后经历的六个时代命名为：科学时代、娱乐时代、长人时代、矮人时代、巨长时代、巨矮时代。
>公元 3091 年 1 月 1 日，人均身高 0.33 米的人类正式开启大规模移民系外行星的浪潮。多名身高低于 0.11 米的时代楷模联名发文，将人类即将迈入的这个新时代称为黄金时代，以纪念一千多年前中国大陆著名社会学家李银河女士和她的丈夫著名作家王小波先生。
>
>运筹OR帷幄火星总部
>3091 年 12 月 5 日

## 6 参考资料

1. [库里 2018-19 赛季常规赛投篮图](https://stats.nba.com/events/?flag=3&CFID=33&CFPARAMS=2018-19&PlayerID=201939&ContextMeasure=FGA&Season=2018-19&section=player&sct=plot)，NBA 官方统计网站
2. [NBA 球员投篮数据可视化](https://mp.weixin.qq.com/s/Qevx7ijb-ymn1YGpBw51Sw)， 法纳斯特
3. [18-19 赛季球员出手位置统计图 - 湿乎乎的话题 - 虎扑社区](https://bbs.hupu.com/27991975.html)，crossin先生
4. [虎扑热帖|Python数据分析|NBA的球星们喜欢在哪个位置出手](https://mp.weixin.qq.com/s/pumsu5IVpb3P5BSycBC1mA)，Crossin的编程教室
5. [Github 项目 nba_py 的文档](https://github.com/seemethere/nba_py)
6. [Python3 网络爬虫开发实战](https://book.douban.com/subject/30175598/)，崔庆才 著，人民邮电出版社
7. [从小白到大师，这里有一份 Pandas 入门指南](https://mp.weixin.qq.com/s/8F8vvhOJgoNDtYf3qOWV9A)，Rudolf Höhn 著，机器之心 译
8. [pandas 文档](https://pandas.pydata.org/pandas-docs/stable/)
9. [scikit-learn 中关于 svm 的文档](https://scikit-learn.org/stable/modules/svm.html#svm-classification)
10. [pyecharts 文档](https://pyecharts.org/#/zh-cn/intro)
11. [Basketball court](https://en.wikipedia.org/wiki/Basketball_court)，维基百科
12. [限制区不适用的情况](https://videorulebook.nba.com/rule/restricted-area-does-not-apply/)，NBA 规则视频手册
13. [1869 年，戴维发现并命名大熊猫](http://mini.eastday.com/mobile/180223085752227.html)，凤凰网四川综合
14. [走进神秘的宝兴的戴维新村](http://www.mafengwo.cn/i/12323830.html)，马蜂窝
15. [大熊猫](https://baike.baidu.com/item/%E5%A4%A7%E7%86%8A%E7%8C%AB/34935?fromtitle=%E7%86%8A%E7%8C%AB&fromid=162918)，百度百科


