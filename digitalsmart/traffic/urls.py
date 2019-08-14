from django.urls import path,include
from .views import citylist, daily_index, road_list, detail_road,yeartraffic

urlpatterns = {
    path("api/",include([
    path("trafficindex/city/list", citylist),#1.获取城市列表
    path("trafficindex/city/curve", daily_index),#2.实时城市交通拥堵指数
    path("trafficindex/city/road", road_list),#3.获取道路情况
    path("trafficindex/city/detailroad", detail_road),#道路具体情况
    path("trafficindex/city/year", yeartraffic),#5.城市季度交通
    ]))


}
