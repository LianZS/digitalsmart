from django.urls import path
from .views import citylist, daily_index, road_list, detail_road,yeartraffic

urlpatterns = {
    path("api/trafficindex/city/list", citylist),
    path("api/trafficindex/city/curve", daily_index),
    path("api/trafficindex/city/road", road_list),
    path("api/trafficindex/city/detailroad", detail_road),
    path("api/trafficindex/city/year", yeartraffic),

}
