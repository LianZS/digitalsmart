from django.urls import path, include
from .views import CityDemo

city = CityDemo()
urlpatterns = {
    path("api/", include([
        path("trafficindex/", include([
            path("city/", include([
                path("list", city.citylist),  # 1.获取城市列表
                path("curve", city.daily_index),  # 2.实时城市交通拥堵指数
                path("road", city.road_list),  # 3.获取道路情况
                path("detailroad", city.detail_road),  # 道路具体情况
                path("year", city.yeartraffic),  # 5.城市季度交通
            ])),

        ])),
        path("getCityInfo", city.get_city_map),  # 获取城市地图数据
        path("airstate", city.get_city_air)  # 获取城市空气状况

    ])),

}
