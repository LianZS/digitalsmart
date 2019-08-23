from django.urls import path, include

from .scence_data_view import ScenceData
from .specile_function_view import Crack

scence = ScenceData()
crack = Crack()
urlpatterns = {
    path("api/", include([
        path("getScenceDataByTime", scence.interface_historytime_scence_data),  # 获取景区某时刻人流
        path("getScenceDataByDate", scence.interface_historydate_scence_data),  # 获取景区某天人流
        path("getScenceHeatmapDataByTime", scence.interface_hisroty_scence_distribution_data),  # 获取景区某时刻人流分布情况
        path("getMusic", crack.get_music),  # 获取音乐

        path("downMusic", crack.down_music),  # 下载音乐
        path("validation", crack.identity_authentication),  # 身份认证
        path("baidudoc", crack.down_baidu_doc),  # 百度文档下载
        path("goodsprice", crack.get_goods_price_change),  # 获取商品价格变化
        path("goodsinfo", crack.get_goods_info),  # 获取商品卖家画像

    ])),
}
