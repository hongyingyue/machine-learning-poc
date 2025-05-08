# 矢量地图shp文件，注意完整文件包括同名的 shp，shx，dbf三个文件，名字和路径需要相同
# https://tianchi.aliyun.com/notebook-ai/detail?spm=5176.12586969.1002.6.72e87f7doOyHCP&postId=63248

import pandas as pd
import geopandas as gp
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rc('figure', figsize=(14, 7))
matplotlib.rc('font', size=14)
matplotlib.rc('axes', grid=False)
matplotlib.rc('axes', facecolor='white')


def geo_china(df, size_column='size', title='map'):
    china_geod = gp.GeoDataFrame.from_file("../../assets/province.shp", encoding='gb18030')

    ax = china_geod.plot(color='white', edgecolor='black')

    df.plot(ax=ax, color='red', markersize=df[size_column], alpha=0.5)
    # df.plot(ax=ax, column=size_column, cmap='Blues', linewidth=0.8, edgecolor='0.8')
    ax.set_axis_off()
    plt.show()


if __name__ == '__main__':
    data = pd.read_csv("../../data/map_R_province.csv")
    data_agg = data.groupby(['City'])[['City']].size().reset_index(name='size')

    city_name_map = pd.read_csv(open("../../assets/city_geocode_lookup.csv", encoding='gbk'))

    data_agg = data_agg.merge(city_name_map, left_on='City', right_on='City', how='left')

    geo_data_agg = gp.GeoDataFrame(data_agg, geometry=gp.points_from_xy(data_agg.Lon, data_agg.Lat))

    geo_china(geo_data_agg, size_column='size')
