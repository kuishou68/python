import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import pyecharts.options as opts
from pyecharts.charts import Line

import re

df_excel = pd.read_excel('qq_excel.xlsx')  # 默认读取sheet=0 Pandas DataFrame'

def getTimeStr(row):
    item = row['时间']
    if pd.isnull(item) | pd.isna(item):
        return

    data = item.split('年')[0]
    return data

# 按年统计说说数量
def readCount(result, row):
    timeData = getTimeStr(row)
    if timeData == None: return
    if timeData in result.keys():
        result[timeData] += 1
    else:
        result[timeData] = 1

# 按年统计说说点赞数
def readThumb(result, row):
    item = row['赞']
    if pd.isnull(item):
        return
    # data = re.match(r'赞\((\d+).*', item, re.M | re.I)
    if len(item.split("(")) <= 1:
        return
    data = item.split("(")[1].split(")")[0]

    timeData = getTimeStr(row)
    if timeData == None: return
    if timeData in result.keys():
        result[timeData] += int(data)
    else:
        result[timeData] = int(data)

# 按年统计说说评论数
def readComment(result, row):
    item = row['评论']
    if pd.isnull(item):
        return
    # data = re.match(r'赞\((\d+).*', item, re.M | re.I)
    if len(item.split("(")) <= 1:
        return
    data = item.split("(")[1].split(")")[0]

    timeData = getTimeStr(row)
    if timeData == None: return
    if timeData in result.keys():
        result[timeData] += int(data)
    else:
        result[timeData] = int(data)


def readExcel(df_excel):
    count = {}
    result = {}
    thumb = {}
    comment = {}
    for index, row in df_excel.iterrows():
        readCount(count, row)
        readThumb(thumb, row)
        readComment(comment, row)

    result['count'] = count
    result['thumb'] = thumb
    result['comment'] = comment
    return result

def getKeyAndVal(keyWord):
    data = readExcel(df_excel).get(keyWord)
    key = []
    value = []
    for item in data.keys():
        key.append(item)
        value.append(data[item])
    key.reverse()
    value.reverse()
    return [key, value]

# 统计每年发表说说次数柱状图
def paintBar():
    count = readExcel(df_excel).get('count')
    # V1 版本开始支持链式调用
    data = getKeyAndVal('count')
    print(data[0])
    d = (
        Bar()
            .add_xaxis(data[0])
            .add_yaxis("每年发表说说总数", data[1])
            .render("每年发表说说总数柱状图.html")
    )
paintBar()

# 统计点赞和评论折线图
def paintLine():
    commentData = getKeyAndVal('comment')
    thumbData = getKeyAndVal('thumb')

    xaxis_data = commentData[0]
    commentValue = commentData[1]
    thumbValue = thumbData[1]
    d = (
        Line()
            .add_xaxis(xaxis_data=xaxis_data)
            .add_yaxis("每年评论数", y_axis=commentValue)
            .add_yaxis("每年点赞数", y_axis=thumbValue)
            .render("每年点赞和评论折现图.html")  # 输出图形
    )
paintLine()


