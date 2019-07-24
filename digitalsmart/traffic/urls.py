from django.urls import path
from .views import citylist, daily_index, road_list, detail_road,yeartraffic

urlpatterns = {
    path("trafficindex/city/list", citylist),
    path("trafficindex/city/curve", daily_index),
    path("trafficindex/city/road", road_list),
    path("trafficindex/city/detailroad", detail_road),
    path("trafficindex/city/year", yeartraffic),

}
