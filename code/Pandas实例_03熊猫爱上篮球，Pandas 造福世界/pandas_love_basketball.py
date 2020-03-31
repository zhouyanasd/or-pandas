#!/usr/bin/env python
# coding: utf-8

from matplotlib.patches import Arc, Circle, Rectangle, Polygon
from pyecharts.faker import Faker
from pyecharts.charts import Line
import pyecharts.options as opts
import matplotlib.pyplot as plt
from sklearn import svm
import pandas as pd
import numpy as np
import requests
import json
import os
import re


# ---------
# 1 获取数据
# ---------

# 获取球员 ID 信息
url     = "https://stats.nba.com/stats/commonallplayers?"
params  = {
           "LeagueID":            '00',
           "Season":              '2019',
           "IsOnlyCurrentSeason": 0
          }
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/77.0.3865.90 Safari/537.36',
           'Referer': 'https://stats.nba.com/',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
           'Connection': 'keep-alive',
           'Host': 'stats.nba.com',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'same-origin',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token': 'true'
           }
try:
    idInfo = (requests.get(url, params=params, headers=headers)
                      .json()["resultSets"][0]
             )
except Exception as e:
    print("\n错误：球员 ID 信息获取失败，请确认网络连接正常后重启程序！")
    exit()
else:
    idInfo       = pd.DataFrame(idInfo["rowSet"], 
                                columns=idInfo["headers"])
    playerIDList = idInfo["PERSON_ID"].tolist()
    print("\n成功：球员 ID 信息获取成功\n")


# 获取球员常规赛投篮数据
shotDF, errorList, emptyList = pd.DataFrame(), [], []
for i, playerID in enumerate(playerIDList):
    url    = "https://stats.nba.com/stats/shotchartdetail?"
    params = {
              "SeasonType":     'Regular Season',
              "TeamID":         0,
              "PlayerID":       playerID,
              "PlayerPosition": '',
              "GameID":         '',
              "Outcome":        '',
              "Location":       '',
              "Month":          0,
              "SeasonSegment":  '',
              "DateFrom":       '',
              "DateTo":         '',
              "OpponentTeamID": 0,
              "VsConference":   '',
              "VsDivision":     '',
              "RookieYear":     '',
              "GameSegment":    '',
              "Period":         0,
              "LastNGames":     0,
              "ContextMeasure": 'FGA',
             }
    try:
        shotDFSec = (requests.get(url, params=params,                             
                                  headers=headers)
                             .json()["resultSets"][0]
                    )
    except Exception as e:
        errorList.append(playerID)
        print('错误：第{0}个球员（ID:{1}）数据获取失败'
              .format(i + 1, playerID))
    else:
        print('成功：第{0}个球员（ID:{1}）数据获取成功'
              .format(i + 1, playerID))
        if shotDFSec["rowSet"] != []:
            shotDFSec = pd.DataFrame(shotDFSec["rowSet"], 
                                     columns=shotDFSec["headers"])
            shotDF    = shotDF.append(shotDFSec)
        else:
            emptyList.append(playerID)
            print('警告：第{0}个球员（ID:{1}）数据为空'
                  .format(i + 1, playerID))

if emptyList != []:
    print('警告：以下球员 ID 数据为空\n{0}\n'.format(emptyList))

if errorList != []:
    print('错误：以下球员 ID 数据获取失败\n{0}\n'.format(errorList))

# 将数据保存到外部文件
# os.getcwd() 用于获取当前工作目录，cwd 是 current work directory 的简称
shotDF.to_csv('shotInfo.csv')
print('数据已输出到外部文件：', os.getcwd() + '/shotInfo.csv')


# ---------
# 2 数据概览
# ---------

# 使数据框在显示时不隐藏部分行列
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',    None)

# 转换数据框列类型的函数
def convert_df(df, deep_copy=True):
    """Automatically converts columns that are worth stored as
    ``categorical`` dtype.

    Parameters
    ----------
    df: pd.DataFrame
        Data frame to convert.
    deep_copy: bool
        Whether or not to perform a deep copy of the original data 
        frame.
        
    Returns
    -------
    pd.DataFrame
        Optimized copy of the input data frame.
    """
    return df.copy(deep=deep_copy).astype({
        col: 'category' for col in df.columns
        if df[col].nunique() / df[col].shape[0] < 0.5})

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

# 自定义查看各列取值情况的函数 exam_col_value
def exam_col_value(df, col):
    '''
    Examing unique values of specific columns of DataFrame

    Parameters
    ----------
    df: pd.DataFrame
        Data frame to exam.
    col: int or str
        Index or name of columns
        
    Returns
    -------
    examResult: dict
        col_index, col_name, unique_values_count, unique_values,
        null_index of specific columns of Datarame
    '''
     
    if isinstance(col, int):
        colName  = df.columns[col]
        colIndex = col
    else:
        colName  = col
        colIndex = df.columns.get_indexer([col])[0]
        
    dfCol        = df[colName]
    uniqueValues = np.array(dfCol.drop_duplicates()
                                 .sort_values().tolist())
    uniqueValuesCount = uniqueValues.size

    nullMark = dfCol.isnull()
    if any(nullMark):
        nullIndex = dfCol[nullMark].index.values
    else:
        nullIndex = None

    examResult = {
                  'col_index':           colIndex, 
                  'col_name':            colName,
                  'unique_values_count': uniqueValuesCount,  
                  'unique_values':       uniqueValues, 
                  'null_index':          nullIndex
                 }
                 
    return examResult

# 检查所有列的取值情况，取值情况将会以 csv 文件的形式保存在当前目录下
examDfResultL = []
for col in shotDF.columns:
    examDfResultL.append(exam_col_value(shotDF, col))

examDF = pd.DataFrame(examDfResultL)
examDF.to_csv('shotDF_exam_result.csv')
examDF


# -----------
# 3 数据预处理
# -----------

# 3.1 前 4 个问题的处理

# 解决 PLAYER_NAME 列存在缺失的问题。
con = shotDF.PLAYER_NAME.isnull()
col = ['PLAYER_ID', 'PLAYER_NAME']
shotDF[con][col]

col = 'PLAYER_NAME'
new = ['Bimbo Coles'] + ['Lionel Simmons'] * 4      
shotDF.loc[con, col] = new

exam_col_value(shotDF, 'PLAYER_NAME')

# 解决 SHOT_TYPE 列存在的问题
con = shotDF.SHOT_TYPE.isnull()
shotDF[con].index.tolist()

con = shotDF.SHOT_TYPE == '3PT Field Goal'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()

def zone_to_type(x):
    if x in ['Mid-Range', 'In The Paint (Non-RA)', 'Restricted Area']:
        return '2PT Field Goal'
    else:
        return '3PT Field Goal'

shotDF = shotDF.assign(SHOT_TYPE=lambda df:df.SHOT_ZONE_BASIC
                       .apply(zone_to_type))

exam_col_value(shotDF, 'SHOT_TYPE')
con = shotDF.SHOT_TYPE == '3PT Field Goal'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()

# 解决 ACTION_TYPE 列存在的问题
def type_to_detail(x):
    import re
    L = re.split(' ', x)
    return L[-2] + ' ' + L[-1]

shotDF = shotDF.assign(ACTION_TYPE_BASIC=lambda df:
                       df.ACTION_TYPE.apply(type_to_detail))
shotDF.ACTION_TYPE_BASIC.sort_values().unique()

shotDF = shotDF.assign(ACTION_TYPE = shotDF.ACTION_TYPE
                       .apply(lambda str_: str_.lower()))

# 解决 TEAM_NAME 列存在的问题
col1, col2 = 'TEAM_ID', 'TEAM_NAME'
(shotDF[[col1, col2]]
 .drop_duplicates(subset=col2)
 .sort_values(by=col1)
)

con = shotDF.TEAM_NAME == 'LA Clippers'
col = 'TEAM_NAME'
new = 'Los Angeles Clippers'
shotDF.loc[con, col] = new

# 3.2 第 5 个问题的处理

# 检查 SHOT_ZONE_AREA 和 SHOT_ZONE_RANGE 列
con = shotDF.SHOT_ZONE_AREA == 'Back Court(BC)'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()

con = shotDF.SHOT_ZONE_RANGE == 'Back Court Shot'
col = 'SHOT_ZONE_BASIC'
shotDF[con][col].unique().tolist()

# SHOT_ZONE_BASIC == Above the Break 3 的数据可视化
con  = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
data = shotDF[con]

conLC = data.SHOT_ZONE_AREA == 'Left Side Center(LC)'
conC  = data.SHOT_ZONE_AREA == 'Center(C)'
conRC = data.SHOT_ZONE_AREA == 'Right Side Center(RC)'
conBC = data.SHOT_ZONE_AREA == 'Back Court(BC)'

dataLC, dataC  = data[conLC], data[conC]
dataRC, dataBC = data[conRC], data[conBC]

xLC, yLC = dataLC['LOC_X'].values, dataLC['LOC_Y'].values
xC , yC  = dataC ['LOC_X'].values, dataC ['LOC_Y'].values
xRC, yRC = dataRC['LOC_X'].values, dataRC['LOC_Y'].values
xBC, yBC = dataBC['LOC_X'].values, dataBC['LOC_Y'].values

plt.figure()
plt.scatter(xLC, yLC, s=1, alpha=0.3, color='green')
plt.scatter(xC,  yC,  s=1, alpha=0.3, color='red')
plt.scatter(xRC, yRC, s=1, alpha=0.3, color='blue')
plt.scatter(xBC, yBC, s=1, alpha=0.3, color='black')
plt.show()

# 确定划分 SHOT_ZONE_AREA 的直线方程
def area_to_num(x):
    if x == 'Center(C)':
        return 1
    else:
        return 0


con1    = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
con2    = shotDF.SHOT_ZONE_AREA  != 'Back Court(BC)'    
dataSvm = (shotDF[(con1) & (con2)]
           .assign(
                   SHOT_ZONE_MARK=lambda df:
                       df.SHOT_ZONE_AREA.apply(area_to_num),
                   LOC_X_ABS     =lambda df:
                       df.LOC_X.apply(abs)
                  )
          )

col1 = ['LOC_X_ABS', 'LOC_Y']
col2 = 'SHOT_ZONE_MARK'
xSvm = dataSvm[col1].values
ySvm = dataSvm[col2].values

lin_clf = svm.SVC(kernel='linear')
lin_clf.fit(xSvm, ySvm)

omega1 = lin_clf.coef_[0,0]
omega2 = lin_clf.coef_[0,1]
b      = lin_clf.intercept_[0]

if omega2 > 0:
    print('右侧直线方程：{0:.4f}x + {1:.4f}y = {2:.4f}'
          .format( omega1, omega2, -b))
    print('左侧直线方程：{0:.4f}x + {1:.4f}y = {2:.4f}'
          .format(-omega1, omega2, -b))
else:
    print('右侧直线方程：{0}x - {1}y = {2}'
          .format( omega1, -omega2, -b))
    print('左侧直线方程：{0}x - {1}y = {2}'
          .format(-omega1, -omega2, -b))

# 对 SHOT_ZONE_AREA，SHOT_ZONE_RANGE 重新赋值

# 对 LOC_Y 大于 417 的数据，为后场投篮，SHOT_ZONE_BASIC 应取 Backcourt
con1 = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
con2 = shotDF.LOC_Y.astype(int) > 417
col  = 'SHOT_ZONE_BASIC'
new  = 'Backcourt'
shotDF.loc[(con1) & (con2), col] = new

# 对三分，SHOT_ZONE_RANGE 均为 24+ ft，即大于 24 英尺
# 严格来说，底角三分应为 22+ ft，这是官方数据的问题，但这个问题不大，未作处理      
col = 'SHOT_ZONE_RANGE'
new = '24+ ft.'      
shotDF.loc[con1, col] = new

# 根据直线方程对 SHOT_ZONE_AREA 进行修改
def modify_area(df):
    if df.SHOT_ZONE_BASIC == 'Above the Break 3' 
    and df.SHOT_ZONE_AREA == 'Back Court(BC)':
        if df.LOC_X >= 0:
            if -34 * df.LOC_X + 11 * df.LOC_Y + 12 >= 0:
                return 'Center(C)'
            else:
                return 'Right Side Center(RC)'
        else:
            if 34 * df.LOC_X + 11 * df.LOC_Y + 12 >= 0:
                return 'Center(C)'
            else:
                return 'Left Side Center(LC)'
    else:
        return df.SHOT_ZONE_AREA


shotDF = shotDF.assign(SHOT_ZONE_AREA=lambda df: 
                       df.apply(modify_area, axis=1))


# SHOT_ZONE_BASIC == Above the Break 3 的数据（已重新赋值）可视化
con  = shotDF.SHOT_ZONE_BASIC == 'Above the Break 3'
data = shotDF[con]

conLC = data.SHOT_ZONE_AREA == 'Left Side Center(LC)'
conC  = data.SHOT_ZONE_AREA == 'Center(C)'
conRC = data.SHOT_ZONE_AREA == 'Right Side Center(RC)'
conBC = data.SHOT_ZONE_AREA == 'Back Court(BC)'

dataLC, dataC  = data[conLC], data[conC]
dataRC, dataBC = data[conRC], data[conBC]

xLC, yLC = dataLC['LOC_X'].values, dataLC['LOC_Y'].values
xC , yC  = dataC ['LOC_X'].values, dataC ['LOC_Y'].values
xRC, yRC = dataRC['LOC_X'].values, dataRC['LOC_Y'].values
#xBC, yBC = dataBC['LOC_X'].values, dataBC['LOC_Y'].values

plt.figure()
plt.scatter(xLC, yLC, s=1, alpha=0.3, color='green')
plt.scatter(xC,  yC,  s=1, alpha=0.3, color='red')
plt.scatter(xRC, yRC, s=1, alpha=0.3, color='blue')
#plt.scatter(xBC, yBC, s=1, alpha=0.3, color='black')
plt.show()


# ---------
# 4 数据分析
# ---------

# 4.1 NBA 球员投篮选择分析

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

shotDF = (shotDF.assign(SEASON=lambda df: 
                            df.GAME_DATE.apply(proc_date),
                        SHOT_TYPE_DETAIL=lambda df: 
                            df.SHOT_ZONE_BASIC.apply(proc_zone)
                       )
                .pipe(convert_df)
         )

shotDF_crosstab = (pd.crosstab(shotDF.SEASON, shotDF.SHOT_TYPE_DETAIL)
                     .apply(lambda _row: _row/sum(_row), 1)
                  )
shotDF_crosstab

roundV = np.vectorize(round)
datax  = list(map(lambda x: str(x)[2:7], shotDF_crosstab.index.tolist()))
datay  = roundV(shotDF_crosstab.values.T, 4)

c = (
     Line()
     .add_xaxis(datax)
     .add_yaxis("2 分 (中投)", datay[0].tolist())
     .add_yaxis("2 分 (油漆区)", datay[1].tolist())
     .add_yaxis("3 分", datay[2].tolist())
     .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
     )
     .set_global_opts(
         title_opts=opts.TitleOpts(title="NBA 球员投篮选择的变化"),
         xaxis_opts=opts.AxisOpts(
                                  axistick_opts=opts.AxisTickOpts(
                                      is_align_with_label=True
                                  ),
                                  axislabel_opts=opts.LabelOpts(
                                      rotate=45, font_size=12, margin=14
                                  )
         ),
     )
)

c.render_notebook()

# 4.2 NBA 球员投篮命中率分析

def rate(x):
    x = x.astype(int)
    return x.sum() / x.size

shotDF_pivtab = shotDF.pivot_table(values='SHOT_MADE_FLAG', 
                                   index='SEASON',
                                   columns='SHOT_TYPE_DETAIL', 
                                   aggfunc={'SHOT_MADE_FLAG': rate}
                                  )
shotDF_pivtab

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
                                  axistick_opts=opts.AxisTickOpts(
                                      is_align_with_label=True
                                  ),
                                  axislabel_opts=opts.LabelOpts(
                                      rotate=45, font_size=12, margin=14
                                  )
         )
     )
)

c.render_notebook()

# 4.3 NBA 4 加时比赛

(shotDF[shotDF.PERIOD==8].drop_duplicates(subset='GAME_ID')
                         .sort_values(by='SEASON')
)

# 4.4 球员投篮图绘制

def Arc_fill(center, radius, theta1, theta2, resolution=50, **kwargs):
    # generate the points
    theta  = np.linspace(np.radians(theta1), np.radians(theta2), resolution)
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1]))
    # build the polygon and add it to the axes
    poly = Polygon(points.T, closed=True, **kwargs)
    return poly


def shot_plot(playerName = 'Kobe Bryant', season = '2005-06', 
              color='#003370', lw=2):

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
                               linewidth=lw, color="#fefefe", 
                               fill=True, zorder=2)
    outer_rec = Rectangle(xy=(-80, -53), width=160, height=190,
                          linewidth=lw, color=color, fill=False, zorder=4)
    ax.add_patch(outer_rec_fill)
    ax.add_patch(outer_rec)

    # 罚球站位点，距底线 7.1 ft, 8.3 ft, 11.5 ft, 14.7 ft
    lane_space_left1  = Rectangle(xy=(-90, 18), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_left2  = Rectangle(xy=(-90, 30), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_left3  = Rectangle(xy=(-90, 62), width=10, height=0,
                                 linewidth=lw, color=color,
                                 fill=False, zorder=4)
    lane_space_left4  = Rectangle(xy=(-90, 94), width=10, height=0,
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
    hash_marks_left1  = Rectangle(xy=(-110, -53), width=0, height=5,
                                  linewidth=lw, color=color,
                                  fill=False, zorder=4)
    hash_marks_right1 = Rectangle(xy=(110, -53), width=0, height=5,
                                  linewidth=lw, color=color,
                                  fill=False, zorder=4)
    hash_marks_left2  = Rectangle(xy=(-50, 77), width=5, height=0,
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
                               linewidth=lw, color=color, 
                               fill=False, zorder=4)
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
                              ec="#dfdfdf", fc="#dfdfdf", 
                              fill=True, zorder=1)
    three_arc = Arc(xy=(0, 0), width=478, height=478, theta1=23,
                    theta2=157, linewidth=lw, color=color,
                    fill=False, zorder=4)
    ax.add_patch(three_arc_fill)
    ax.add_patch(three_arc)

    # 教练席标记线
    midcourt_area_marker_left  = Rectangle(xy=(-250, 227), width=30, height=0,
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
    lines_outer_rec  = Rectangle(xy=(-250, -53), width=500, height=470,
                                linewidth=lw, color=color,
                                fill=False, zorder=4)
    ax.add_patch(lines_outer_rec)

    con1 = shotDF.PLAYER_NAME==playerName
    con2 = shotDF.SHOT_MADE_FLAG==1
    con3 = shotDF.SEASON==season
    shotMade = shotDF[(con1) & (con2) & (con3)][['LOC_X', 'LOC_Y']]
    x_shotMade, y_shotMade = shotMade['LOC_X'], shotMade['LOC_Y']
    
    con2 = shotDF.SHOT_MADE_FLAG==0
    shotMiss = shotDF[(con1) & (con2) & (con3)][['LOC_X', 'LOC_Y']]
    x_shotMiss, y_shotMiss = shotMiss['LOC_X'], shotMiss['LOC_Y']

    plt.scatter(x_shotMiss, y_shotMiss, alpha=0.8, 
                s=30, marker='x', c='#B02020', zorder=3)
    plt.scatter(x_shotMade, y_shotMade, alpha=0.6, 
                s=30, marker='o', c='#208020', zorder=3)
    plt.show()
    

shot_plot('Stephen Curry', '2009-10')
shot_plot('Stephen Curry', '2018-19')
shot_plot()
