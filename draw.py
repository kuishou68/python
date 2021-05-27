import datetime
import calendar
import matplotlib.pyplot as plt

#统计近7天的说说
statistics=dict()
#今天的日期
today = datetime.datetime.now()
#判断闰年
if (calendar.isleap(today.year)):
    #闰年2月的天数
    Feb = 29
else:
    Feb = 28
#每月的天数
month = (31, Feb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
#格式化日期
s = '{}年{}月{}日'
#初始化statistics
def init_times():
    #如果7天都在同一个月
    if today.day>=7:
        #同一个月中，分别初始化7天的日期
        for i in range(7):
            temp=s.format(str(today.year),str(today.month),str(today.day-6+i))
            #初始化日期为0
            statistics[temp]=0
    #7天不在同一个月中，即夸月，要判断上个月是否是前一年的12月，和确定上个月的总天数
    else:
        mon=today.month
        year=today.year
        #确定前一个月有几天
        last=7-today.day
        #如果当月是1月
        if today.month==1:
            month=12
            #年份减一
            year=today.year-1
        #先确定前一个月的几天日期
        for i in range(last):
            temp=s.format(str(year),str(mon),str(month[mon-1]-last+1+i))
            statistics[temp] = 0
        #当月的几天日期
        for i in range(today.day):
            temp = s.format(str(today.year), str(today.month), str(i+1))
            statistics[temp] = 0

def count(qq_time):
    #如果qq日期中有“昨”的字样
    if '昨' in qq_time:
        # 如果今天是当月的第一天，那么昨天就是前一个月的最后一天
        if today.day==1:
            # 如果当月是1月
            if today.month==1:
                qq_time=s.format(str(today.year-1),str(12),str(31))
            else:
                qq_time = s.format(str(today.year), str(today.month-1), str(month[today.month-2]))
        # 如果今天不是当月的第一天，则年份和月份不用管
        else:
            qq_time = s.format(str(today.year), str(today.month), str(today.day-1))
    # 如果qq日期中有“前”的字样
    elif '前' in qq_time:
        #如果今天是当月的第二天，那么前天就是前一个月的最后一天
        if today.day == 2:
            #如果当月是1月
            if today.month == 1:
                qq_time = s.format(str(today.year - 1), str(12), str(31))
            #如果当月不是1月，那么年份不用管
            else:
                qq_time = s.format(str(today.year), str(today.month - 1), str(month[today.month - 2]))
        # 如果今天是当月的第一天，那么前天就是前一个月的倒数第二天
        elif today.day==1:
            # 如果当月是1月
            if today.month==1:
                qq_time=s.format(str(today.year-1),str(12),str(30))
            # 如果当月不是1月，那么年份不用管
            else:
                qq_time = s.format(str(today.year), str(today.month-1), str(month[today.month-2]-1))
        # 如果今天既不是当月的第一天或者第二天
        else:
            qq_time = s.format(str(today.year), str(today.month), str(today.day - 2))
    # 如果qq日期中直接是时间的字样
    elif '天' not in qq_time and '日' not in qq_time:
        qq_time=s.format(str(today.year),str(today.month),str(today.day))
    #统计近7天qq中说说的条数
    if qq_time in statistics:
        statistics[qq_time]=statistics.get(qq_time)+1
#初始化times
init_times()
#从爬取的时间文件中读取说说的日期
with open('qq_word.txt','r',encoding='utf-8') as lines:
    for line in lines:
        count(line.split('\n')[0])

#绘图
plt.rcParams['font.family'] = 'SimHei'
#x轴数据
x_data = date= statistics.keys()
#y轴数据
y_data = statistics.values()
#饼图的百分比
percent=[]
#饼图的数据
for value in statistics.values():
    percent.append(round(value/sum(statistics.values()),1))
#柱状图
#两个子图1行2列展示
fig,ax = plt.subplots(1,2,figsize=(16,12))
#柱状上面的数据
for x,y in zip(x_data,y_data):
    ax[0].text(x,y,y,fontsize=14,horizontalalignment='center')
#y轴在说说最多的数字上加1
ax[0].set_ylim([0,max(statistics.values())+1])
#喂入数据
ax[0].bar(x_data,y_data)
#x轴label文字显示
ax[0].tick_params(axis='x',rotation=20)
#柱状图标题
ax[0].set_title('近7天好友动态统计',fontsize=12)
#为子图设置横轴标题
ax[0].set_xlabel('日期')
#为子图设置纵轴标题
ax[0].set_ylabel('条')
#饼图
ax[1].pie(percent,labels=date,autopct='%1.1f%%')
#绘画
plt.show()