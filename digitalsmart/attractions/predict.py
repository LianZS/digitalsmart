import datetime
from typing import Dict
from .models import PredictParamer


class Predict():
    """
    人流预测模型
    """

    def __init__(self):
        pass

    def predict(self, pid) -> Dict:

        try:
            # 非节假日
            paramer = PredictParamer.objects.get(pid=pid, flag=0)
        except Exception as e:
            return {
                "future_time": [],  # 未来时间序列
                "future_data": []  # 预测值
            }
        hpower = paramer.hpower
        hconstant = paramer.hconstant
        spower = paramer.spower
        sconstant = paramer.sconstant
        lpower = paramer.lpower
        lconstant = paramer.lconstant
        mconstant = paramer.mconstant
        ddate = datetime.datetime.now()
        ttime = ddate.time()
        # 预测起始时间
        start_future_time = datetime.datetime(ddate.year, ddate.month, ddate.day, ttime.hour, int(ttime.minute / 5) * 5,
                                              0)
        # 时间间隔为5分钟
        time_inv = datetime.timedelta(minutes=5)
        # 预测时间序列
        ttime_range = [str((start_future_time + time_inv * i).time()) for i in
                       range(1, 288 - ttime.hour * 12 - int(ttime.minute / 5))]
        x_pos = [x for x in range(ttime.hour * 12 + int(ttime.minute / 5) + 1, 289)]
        # 流量预测
        y_pos = [int(hconstant * pow(x, hpower) + sconstant * pow(x, spower) + lconstant * pow(x, lpower) + mconstant)
                 for x
                 in
                 x_pos]
        return {
            "future_time": ttime_range,  # 未来时间序列
            "future_data": y_pos  # 预测值
        }
