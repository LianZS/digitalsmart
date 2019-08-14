from django.urls import path, include
from .views import citylist, daily_index, road_list, detail_road, yeartraffic,get_city_air

urlpatterns = {
    path("api/", include([
        path("trafficindex/", include([
            path("city/",include([
                path("list", citylist),  # 1.获取城市列表
                path("curve", daily_index),  # 2.实时城市交通拥堵指数
                path("road", road_list),  # 3.获取道路情况
                path("detailroad", detail_road),  # 道路具体情况
                path("year", yeartraffic),  # 5.城市季度交通
            ])),

        ])),
        path("airstate",get_city_air)

    ])),

}
