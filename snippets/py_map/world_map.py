# 有哪些地图可视化工具或Python库可以绘制出真实比例的散点图？ - 叶山Shan Ye的回答 - 知乎
# https://www.zhihu.com/question/404165841/answer/1310033961

import numpy as np
import geopandas as gp
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.rc('figure', figsize=(14, 7))
matplotlib.rc('font', size=14)
matplotlib.rc('axes', grid=False)
matplotlib.rc('axes', facecolor='white')


def geod_world(df, title, legend=False):
    world_geod = gp.GeoDataFrame.from_file('../../assets/World_countries_shp.shp')

    data_geod = gp.GeoDataFrame(df)  # 转换格式
    da_merge = world_geod.merge(data_geod, on='NAME', how='left')  # 合并
    sum(np.isnan(da_merge['NUM']))
    da_merge['NUM'][np.isnan(da_merge['NUM'])] = 14.0  # 填充缺失数据
    da_merge.plot('NUM', k=20, cmap=plt.cm.Blues, alpha=1, legend=legend)
    plt.title(title, fontsize=15)  # 设置图形标题
    plt.gca().xaxis.set_major_locator(plt.NullLocator())  # 去掉x轴刻度
    plt.gca().yaxis.set_major_locator(plt.NullLocator())  # 去年y轴刻度


country_dict = {'大陆': 'China', '美国': 'United States', '香港': 'Hong Kong'
    , '台湾': 'Taiwan, Province of China'
    , '日本': 'Japan', '韩国': 'Korea, Republic of', '英国': 'United Kingdom'
    , '法国': 'France', '德国': 'Germany'
    , '意大利': 'Italy', '西班牙': 'Spain', '印度': 'India', '泰国': 'Thailand'
    , '俄罗斯': 'Russian Federation'
    , '伊朗': 'Iran', '加拿大': 'Canada', '澳大利亚': 'Australia'
    , '爱尔兰': 'Ireland', '瑞典': 'Sweden'
    , '巴西': 'Brazil', '丹麦': 'Denmark'}

temp0 = temp.reset_index()
df = pd.DataFrame({'NAME': temp0['index'].map(country_dict).tolist()
                      , 'NUM': (np.log1p(temp0['数目']) * 100).tolist()})
geod_world(df, 'The popularity of movie in the world')
