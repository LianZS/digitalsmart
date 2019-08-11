from django.urls import path,include
from .admin_views import Admin
from .areainfomation import AreaInfo
from .peopleflow import PeopleFlow
from .comment import Comment
from .views import  upload_photo,get_photo_url
admin = Admin()
areainfo = AreaInfo()

flow=PeopleFlow()
comment=Comment()
urlpatterns = {
    path("api/",include([
        path("getCitysByProvince", areainfo.citylist),  # 获取省份下所有城市列表
        path("getRegionsByCity", areainfo.scencelist),  # 2.获取城市下所有地区列表
        path("getLocation_pn_percent_new", flow.scenceflow_data),  # 实时人流接口
        path("getLocation_trend_percent_new", flow.scenceflow_trend),  # 实时人流趋势
        path("getLocation_search_rate", comment.search_heat),  # 地区全网搜索次数
        path("getLocation_distribution_rate", flow.scence_people_distribution),  # 地区实时人口分布热力图数据
        path("getLocation_geographic_bounds", areainfo.scence_geographic),  # 地区经纬度范围
        path("getCommentRate", comment.get_comment_rate),  # 获取评价关键词指数
    ])),


    path("api/upload",upload_photo),#上传照片
    path("api/getImage",get_photo_url),#获取图片链接
    path("admin/provinces", admin.get_all_provinces),
    path("admin/area_cover", admin.get_cover_pic),

}
