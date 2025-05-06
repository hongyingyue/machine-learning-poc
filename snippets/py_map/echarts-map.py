
# https://github.com/pyecharts/pyecharts
# you should have Internet connect

from pyecharts.charts import Map, Geo
from pyecharts import options as opts


province_dict = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9,
                 '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7,
                 '内蒙古': 3, '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1,
                 '天津': 1, '其他': 1}

province_char = [[item[0],item[1]] for item in province_dict.items()]
print(province_char)

map = Map(init_opts=opts.InitOpts(width='1200px', height='800px'))
map.set_global_opts(
    title_opts=opts.TitleOpts(title="2019年"),
    visualmap_opts=opts.VisualMapOpts(max_=50))
map.add("China Map Example", data_pair=province_char, maptype='china', is_roam=True)
map.render(path="中国地图.html")
