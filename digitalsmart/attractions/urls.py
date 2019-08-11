from django.urls import path
from .admin_views import Admin
from .views import citylist, scencelist, scenceflow_data, scenceflow_trend, \
    search_heat, scence_people_distribution, scence_geographic,upload_photo,get_photo_url
admin = Admin()
urlpatterns = {
    path("api/getCitysByProvince", citylist),  # 获取省份下所有城市列表
    path("api/getRegionsByCity", scencelist),  # 2.获取城市下所有地区列表
    path("api/getLocation_pn_percent_new", scenceflow_data),  # 实时人流接口
    path("api/getLocation_trend_percent_new", scenceflow_trend),  # 实时人流趋势
    path("api/getLocation_search_rate", search_heat),  # 地区全网搜索次数
    path("api/getLocation_distribution_rate", scence_people_distribution),  # 地区实时人口分布热力图数据
    path("api/getLocation_geographic_bounds", scence_geographic),  # 地区经纬度范围
    path("api/upload",upload_photo),#上传照片
    path("api/getImage",get_photo_url),
    path("admin/provinces", admin.get_all_provinces),
    path("admin/area_cover", admin.get_cover_pic),

}
