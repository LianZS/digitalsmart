from django.urls import path, include
from .admin_views import Admin
from .areainfomation_view import AreaInfoDetail
from .peopleflow_view import PeopleFlow
from .comment_view import CommentDetail
from .views import upload_photo, get_photo_url

admin = Admin()

flow = PeopleFlow()
urlpatterns = {
    path("api/", include([
        path("getCitysByProvince", AreaInfoDetail.get_city_queryset),  # 获取省份下所有城市列表
        path("getRegionsByCity", AreaInfoDetail.get_scenic_queryset),  # 2.获取城市下所有地区列表
        path("getLocation_geographic_bounds", AreaInfoDetail.get_scenic_geographic),  # 地区经纬度范围
        path("getScenceInfo", AreaInfoDetail.get_scenic_map),  # 获取景区数据

        path("getLocation_pn_percent_new", flow.get_scenicflow_data_queryset),  # 实时人流接口
        path("getLocation_trend_percent_new", flow.get_scenicflow_trend_queryset),  # 实时人流趋势
        path("getLocation_search_rate", CommentDetail.get_search_heat_queryset),  # 地区全网搜索次数
        path("getLocation_distribution_rate", flow.scence_people_distribution),  # 地区实时人口分布热力图数据
        path("getCommentRate", CommentDetail.get_comment_rate_queryset),  # 获取评价关键词指数
        path("getComment", CommentDetail.get_comment_queryset),  # 获取评价关键词指数
        path("getState", CommentDetail.get_scenic_state_queryset),  # 获取景区状况
        path("upload", upload_photo),  # 上传照片
        path("getImage", get_photo_url),  # 获取图片链接

    ])),

    path("admin/", include([
        path("provinces", admin.get_all_provinces),  # 管理员景区管理的省份界面数据
        path("area_cover", admin.get_cover_pic),  # 管理员景区管理的城市界面图片
        path("uploadCommentRate", admin.up_comment_rate),  # 更新评价指数
        path("uploadComment", admin.up_comment),  # 更新评价

    ])),

}
